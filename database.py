import json
import logging
import os
import sqlite3
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

try:
    import streamlit as st
except Exception:
    st = None

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:
    psycopg = None
    dict_row = None

DB_PATH = Path(__file__).parent / "movies.db"
LOGGER = logging.getLogger(__name__)
_DB_STATUS = {"backend": "unknown", "connected": False, "detail": ""}


def _startup_log(message):
    print(f"[database] {message}", flush=True)
    LOGGER.info(message)


def _get_config_value(key, default=""):
    val = os.getenv(key)
    if val:
        return val.strip()

    if st is not None:
        try:
            return str(st.secrets.get(key, default)).strip()
        except Exception:
            return default

    return default


def _database_url():
    url = _get_config_value("DATABASE_URL", "")
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


def _using_postgres():
    return bool(_database_url())


def get_db_status():
    return dict(_DB_STATUS)


def _postgres_host():
    try:
        parsed = urlparse(_database_url())
        return parsed.hostname or "unknown-host"
    except Exception:
        return "unknown-host"


def get_connection():
    if _using_postgres():
        if psycopg is None:
            raise RuntimeError(
                "DATABASE_URL is set but psycopg is not installed. "
                "Run: pip install 'psycopg[binary]'"
            )
        return psycopg.connect(_database_url(), row_factory=dict_row)

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def _run_query(sql, params=(), fetch=None, commit=False):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, params)
        result = None
        if fetch == "one":
            result = cur.fetchone()
        elif fetch == "all":
            result = cur.fetchall()
        if commit:
            conn.commit()
        return result
    finally:
        cur.close()
        conn.close()


def init_db():
    if _using_postgres():
        try:
            host = _postgres_host()
            _startup_log(f"Attempting Postgres connection to {host}")
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS movies (
                    id BIGSERIAL PRIMARY KEY,
                    tmdb_id BIGINT UNIQUE,
                    title TEXT NOT NULL,
                    year INTEGER,
                    poster_path TEXT,
                    director TEXT,
                    genres TEXT,
                    runtime INTEGER,
                    overview TEXT,
                    list_type TEXT NOT NULL,
                    added_by TEXT NOT NULL,
                    added_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    watched BOOLEAN DEFAULT FALSE,
                    watched_date DATE,
                    adam_rating DOUBLE PRECISION,
                    sean_rating DOUBLE PRECISION,
                    notes TEXT
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_movies_watched_list_added_date
                ON movies (watched, list_type, added_date DESC)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_movies_watched_watched_date
                ON movies (watched, watched_date DESC)
            """)
            conn.commit()
            _DB_STATUS.update(
                {"backend": "postgres", "connected": True, "detail": f"connected:{host}"}
            )
            _startup_log(f"Postgres connection OK; schema ready on {host}")
        except Exception as exc:
            _DB_STATUS.update(
                {"backend": "postgres", "connected": False, "detail": str(exc)}
            )
            _startup_log(
                f"Postgres init FAILED: {exc.__class__.__name__}: {exc}"
            )
            raise
        finally:
            if "cur" in locals():
                cur.close()
            if "conn" in locals():
                conn.close()
        return

    try:
        _run_query(
            """
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tmdb_id INTEGER UNIQUE,
                title TEXT NOT NULL,
                year INTEGER,
                poster_path TEXT,
                director TEXT,
                genres TEXT,
                runtime INTEGER,
                overview TEXT,
                list_type TEXT NOT NULL,
                added_by TEXT NOT NULL,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                watched INTEGER DEFAULT 0,
                watched_date TEXT,
                adam_rating REAL,
                sean_rating REAL,
                notes TEXT
            )
            """,
            commit=True,
        )
        _DB_STATUS.update(
            {"backend": "sqlite", "connected": True, "detail": str(DB_PATH)}
        )
        _startup_log(f"SQLite fallback active at {DB_PATH}")
    except Exception as exc:
        _DB_STATUS.update(
            {"backend": "sqlite", "connected": False, "detail": str(exc)}
        )
        _startup_log(f"SQLite init FAILED: {exc.__class__.__name__}: {exc}")
        raise


def add_movie(tmdb_id, title, year, poster_path, director, genres, runtime,
              overview, list_type, added_by):
    sql = """
        INSERT INTO movies (tmdb_id, title, year, poster_path, director,
                            genres, runtime, overview, list_type, added_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """ if _using_postgres() else """
        INSERT INTO movies (tmdb_id, title, year, poster_path, director,
                            genres, runtime, overview, list_type, added_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            sql,
            (tmdb_id, title, year, poster_path, director,
             json.dumps(genres) if isinstance(genres, list) else genres,
             runtime, overview, list_type, added_by),
        )
        conn.commit()
        return True
    except Exception as exc:
        if isinstance(exc, sqlite3.IntegrityError):
            return False
        if psycopg is not None and isinstance(exc, psycopg.IntegrityError):
            return False
        raise
    finally:
        cur.close()
        conn.close()


def get_unwatched_movies(list_type=None):
    if _using_postgres():
        if list_type:
            rows = _run_query(
                "SELECT * FROM movies WHERE watched = FALSE AND list_type = %s ORDER BY added_date DESC",
                (list_type,),
                fetch="all",
            )
        else:
            rows = _run_query(
                "SELECT * FROM movies WHERE watched = FALSE ORDER BY added_date DESC",
                fetch="all",
            )
    else:
        if list_type:
            rows = _run_query(
                "SELECT * FROM movies WHERE watched = 0 AND list_type = ? ORDER BY added_date DESC",
                (list_type,),
                fetch="all",
            )
        else:
            rows = _run_query(
                "SELECT * FROM movies WHERE watched = 0 ORDER BY added_date DESC",
                fetch="all",
            )
    return [_row_to_dict(r) for r in rows]


def get_watched_movies():
    sql = (
        "SELECT * FROM movies WHERE watched = TRUE ORDER BY watched_date DESC"
        if _using_postgres()
        else "SELECT * FROM movies WHERE watched = 1 ORDER BY watched_date DESC"
    )
    rows = _run_query(sql, fetch="all")
    return [_row_to_dict(r) for r in rows]


def mark_watched(movie_id, adam_rating=None, sean_rating=None, notes=None,
                 watched_date=None):
    if watched_date is None:
        watched_date = date.today().isoformat()
    elif isinstance(watched_date, date):
        watched_date = watched_date.isoformat()

    if _using_postgres():
        _run_query(
            """
            UPDATE movies
            SET watched = TRUE, watched_date = %s, adam_rating = %s, sean_rating = %s, notes = %s
            WHERE id = %s
            """,
            (watched_date, adam_rating, sean_rating, notes, movie_id),
            commit=True,
        )
    else:
        _run_query(
            """
            UPDATE movies
            SET watched = 1, watched_date = ?, adam_rating = ?, sean_rating = ?, notes = ?
            WHERE id = ?
            """,
            (watched_date, adam_rating, sean_rating, notes, movie_id),
            commit=True,
        )


def remove_movie(movie_id):
    sql = "DELETE FROM movies WHERE id = %s" if _using_postgres() else "DELETE FROM movies WHERE id = ?"
    _run_query(sql, (movie_id,), commit=True)


def movie_exists(tmdb_id):
    sql = (
        "SELECT id, title, list_type, watched FROM movies WHERE tmdb_id = %s"
        if _using_postgres()
        else "SELECT id, title, list_type, watched FROM movies WHERE tmdb_id = ?"
    )
    row = _run_query(sql, (tmdb_id,), fetch="one")
    return _row_to_dict(row) if row else None


def get_all_genres():
    sql = (
        "SELECT genres FROM movies WHERE watched = FALSE"
        if _using_postgres()
        else "SELECT genres FROM movies WHERE watched = 0"
    )
    rows = _run_query(sql, fetch="all")
    all_genres = set()
    for row in rows:
        row_dict = _row_to_dict(row)
        try:
            genres = json.loads(row_dict["genres"]) if isinstance(row_dict.get("genres"), str) else []
            all_genres.update(genres)
        except (json.JSONDecodeError, TypeError):
            pass
    return sorted(all_genres)


def get_watch_stats():
    sql = (
        "SELECT * FROM movies WHERE watched = TRUE"
        if _using_postgres()
        else "SELECT * FROM movies WHERE watched = 1"
    )
    watched = _run_query(sql, fetch="all")
    watched = [_row_to_dict(r) for r in watched]
    total = len(watched)
    if total == 0:
        return {
            "total": 0,
            "avg_adam": 0,
            "avg_sean": 0,
            "total_hours": 0,
            "top_genre": "N/A",
            "adam_suggested_watched": 0,
            "sean_suggested_watched": 0,
        }

    adam_ratings = [m["adam_rating"] for m in watched if m["adam_rating"]]
    sean_ratings = [m["sean_rating"] for m in watched if m["sean_rating"]]
    total_minutes = sum(m["runtime"] or 0 for m in watched)

    genre_counts = {}
    for m in watched:
        try:
            genres = json.loads(m["genres"]) if isinstance(m["genres"], str) else []
        except (json.JSONDecodeError, TypeError):
            genres = []
        for g in genres:
            genre_counts[g] = genre_counts.get(g, 0) + 1

    top_genre = max(genre_counts, key=genre_counts.get) if genre_counts else "N/A"

    return {
        "total": total,
        "avg_adam": round(sum(adam_ratings) / len(adam_ratings), 1) if adam_ratings else 0,
        "avg_sean": round(sum(sean_ratings) / len(sean_ratings), 1) if sean_ratings else 0,
        "total_hours": round(total_minutes / 60, 1),
        "top_genre": top_genre,
        "adam_suggested_watched": sum(1 for m in watched if m["list_type"] == "adam_pick"),
        "sean_suggested_watched": sum(1 for m in watched if m["list_type"] == "sean_pick"),
    }


def _row_to_dict(row):
    if row is None:
        return None

    if isinstance(row, dict):
        d = dict(row)
    else:
        d = dict(row)

    for dt_field in ("added_date", "watched_date"):
        if dt_field in d and isinstance(d[dt_field], (datetime, date)):
            d[dt_field] = d[dt_field].isoformat()

    if "watched" in d:
        d["watched"] = bool(d["watched"])

    if "genres" in d and isinstance(d["genres"], str):
        try:
            d["genres_list"] = json.loads(d["genres"])
        except (json.JSONDecodeError, TypeError):
            d["genres_list"] = []
    else:
        d["genres_list"] = []
    return d


SEED_MOVIES = [
    (12614, "Victor/Victoria", 1982, "/mCjXcPRM3Rc7gOCGeVrBdPvF2bk.jpg", "Blake Edwards", ["Music", "Comedy", "Romance"], 134, "A struggling female soprano finds work playing a male female impersonator, but it complicates her personal life.", "adam_pick", "Adam"),
    (7300, "One Fine Day", 1996, "/5NiRRR7JDNHOr21JNoGRxPWh9vb.jpg", "Michael Hoffman", ["Romance", "Comedy"], 108, "Melanie Parker, an architect and mother of Sammy, and Jack Taylor, a newspaper columnist and father of Maggie, are two single parents. They meet one morning when overwhelmed Jack accidentally brings Melanie's son to his daughter's school.", "adam_pick", "Adam"),
    (49806, "The Daytrippers", 1997, "/bDmconT9Fj0dnXdV5LaGAxXrVFN.jpg", "Greg Mottola", ["Comedy", "Drama"], 87, "Eliza D'Amico thinks her marriage to Louis is going great until she finds a mysterious love letter in his things.", "adam_pick", "Adam"),
    (19366, "Josie and the Pussycats", 2001, "/jZDTbsLCufLShWJBTScuGf8T8Rw.jpg", "Deborah Kaplan", ["Comedy", "Music"], 98, "Josie, Melody and Val are three small-town girl musicians determined to take their band out of their garage and straight to the top.", "adam_pick", "Adam"),
    (791177, "Bones and All", 2022, "/dBQuk2LkHjrDsSjueirPQg96GCc.jpg", "Luca Guadagnino", ["Horror", "Romance", "Drama"], 131, "Abandoned by her father, a young woman embarks on a thousand-mile odyssey through the backroads of America.", "adam_pick", "Adam"),
    (785542, "The Outrun", 2024, "/zfRR2CkbvYrLuOPQFm8vBaENyMy.jpg", "Nora Fingscheidt", ["Drama"], 118, "Fresh out of rehab, Rona returns to the Orkney Islands\u2014a place both wild and beautiful.", "adam_pick", "Adam"),
    (18087, "Pride and Prejudice", 2003, "/3oAub2opFoDhepSoNW3Tlcmems7.jpg", "Andrew Black", ["Romance", "Comedy"], 104, "In this contemporary LDS twist on Jane Austen's iconic novel, Elizabeth Bennet is a smart, independent college student in Provo, Utah.", "adam_pick", "Adam"),
    (970948, "What Happens Later", 2023, "/oSAdS03j8zbjv35gKdjrIL5snw1.jpg", "Meg Ryan", ["Romance", "Comedy"], 104, "Two ex-lovers get snowed in at a regional airport overnight. Indefinitely delayed, they are forced to confront what went wrong.", "adam_pick", "Adam"),
    (25167, "Bye Bye Birdie", 1963, "/u3m2kU5aFj6V6cNYOd9a22Iia7O.jpg", "George Sidney", ["Comedy", "Music"], 112, "A singer goes to a small town for a performance before he is drafted.", "adam_pick", "Adam"),
    (27686, "State Fair", 1945, "/cmy55K7Qs1WQeGPksHBphjyjh3b.jpg", "Walter Lang", ["Music", "Comedy", "Romance"], 100, "During their annual visit to the Iowa State Fair, the Frake family enjoy many adventures.", "adam_pick", "Adam"),
    (37233, "The Firm", 1993, "/kFexXCzidkm4LwlgZqxsJsDQB5v.jpg", "Sydney Pollack", ["Drama", "Mystery", "Thriller"], 154, "Mitch McDeere is a young man with a promising future in Law. About to sit his Bar Exam, he is approached by The Firm with an offer he can't refuse.", "sean_pick", "Sean"),
    (16869, "Inglourious Basterds", 2009, "/7sfbEnaARXDDhKm0CZ7D7uc2sbo.jpg", "Quentin Tarantino", ["Drama", "Thriller", "War"], 153, "In Nazi-occupied France during World War II, a group of Jewish-American soldiers known as 'The Basterds' are chosen to spread fear throughout the Third Reich.", "sean_pick", "Sean"),
    (9471, "Charlie's Angels: Full Throttle", 2003, "/n4cdJ0Wqxb7C0HmZbcaC4eYnkIf.jpg", "McG", ["Action", "Adventure", "Comedy"], 106, "The Angels are charged with finding a pair of missing rings that are encoded with the personal information of members of the Witness Protection Program.", "sean_pick", "Sean"),
    (290098, "The Handmaiden", 2016, "/dLlH4aNHdnmf62umnInL8xPlPzw.jpg", "Park Chan-wook", ["Thriller", "Drama", "Romance"], 145, "1930s Korea, in the period of Japanese occupation, a new girl, Sookee, is hired as a handmaiden to a Japanese heiress.", "sean_pick", "Sean"),
    (593691, "HOMECOMING: A film by Beyonc\u00e9", 2019, "/nKdP4K3Bj3qnjtDCq9lTg7UOHVy.jpg", "Beyonc\u00e9", ["Documentary", "Music"], 137, "This intimate, in-depth look at Beyonc\u00e9's celebrated 2018 Coachella performance reveals the emotional road from creative concept to cultural movement.", "sean_pick", "Sean"),
    (758866, "Drive My Car", 2021, "/3cOsf5HBjPK2QCz9ebQlGHNnE7y.jpg", "Ryusuke Hamaguchi", ["Drama"], 179, "Yusuke Kafuku, a stage actor and director, still unable, after two years, to cope with the loss of his beloved wife, accepts to direct a production of Uncle Vanya.", "sean_pick", "Sean"),
    (630240, "Titane", 2021, "/mBlpouG3gqB8WLdP65LCOXb3jFb.jpg", "Julia Ducournau", ["Drama", "Thriller", "Horror"], 108, "A woman with a metal plate in her head from a childhood car accident embarks on a bizarre journey that brings her to an aging firefighter.", "sean_pick", "Sean"),
    (375262, "The Favourite", 2018, "/cwBq0onfmeilU5xgqNNjJAMPfpw.jpg", "Yorgos Lanthimos", ["History", "Comedy", "Drama"], 120, "England, early 18th century. The close relationship between Queen Anne and Sarah Churchill is threatened by the arrival of Sarah's cousin, Abigail.", "sean_pick", "Sean"),
    (398818, "Call Me by Your Name", 2017, "/mZ4gBdfkhP9tvLH1DO4m4HYtiyi.jpg", "Luca Guadagnino", ["Romance", "Drama"], 132, "In the summer of 1983, a 17-year-old Elio spends his days in his family's villa in Lombardy, Italy.", "sean_pick", "Sean"),
    (80, "Before Sunset", 2004, "/4sW5XH9ZfYXpvFzev00S1IGAEbg.jpg", "Richard Linklater", ["Drama", "Romance"], 80, "Nine years later, Jesse travels across Europe giving readings from a book he wrote about the night he spent in Vienna with Celine.", "sean_pick", "Sean"),
    (76, "Before Sunrise", 1995, "/kf1Jb1c2JAOqjuzA3H4oDM263uB.jpg", "Richard Linklater", ["Drama", "Romance"], 101, "An unexpected meeting on a train leads two travelers to spend an evening wandering the streets of Vienna.", "sean_pick", "Sean"),
    (132344, "Before Midnight", 2013, "/qbGKJmNUroDz75kh5Oafoall89e.jpg", "Richard Linklater", ["Romance", "Drama"], 109, "It has been nine years since we last met Jesse and Celine, the French-American couple who once spent a night walking and talking in Vienna.", "sean_pick", "Sean"),
    (194, "Am\u00e9lie", 2001, "/nSxDa3M9aMvGVLoItzWTepQ5h5d.jpg", "Jean-Pierre Jeunet", ["Comedy", "Romance"], 122, "At a tiny Parisian caf\u00e9, the adorable yet painfully shy Am\u00e9lie accidentally discovers a gift for helping others.", "sean_pick", "Sean"),
    (660120, "The Worst Person in the World", 2021, "/1NxGNQchGBTHXJ6RShLY1IlZqWn.jpg", "Joachim Trier", ["Drama", "Romance", "Comedy"], 128, "The chronicles of four years in the life of Julie, a young woman who navigates the troubled waters of her love life and struggles to find her career path.", "sean_pick", "Sean"),
    (378, "Raising Arizona", 1987, "/niKyjOqiB4XVl0BqgKTHIlHOCeF.jpg", "Joel Coen", ["Comedy", "Crime"], 94, "When a childless couple\u2014an ex-con and an ex-cop\u2014take one of a wealthy family's quintuplets, they must dodge the law and two bounty hunters.", "mutual", "Both"),
    (279, "Amadeus", 1984, "/gQRfiyfGvr1az0quaYyMram3Aqt.jpg", "Milo\u0161 Forman", ["History", "Music", "Drama"], 160, "Disciplined Italian composer Antonio Salieri becomes consumed by jealousy and resentment towards the youthful and brash musical genius Wolfgang Amadeus Mozart.", "mutual", "Both"),
]


def _seed_if_empty():
    count_row = _run_query("SELECT COUNT(*) AS total FROM movies", fetch="one")
    count = count_row["total"] if isinstance(count_row, dict) else count_row[0]

    if count == 0:
        _startup_log("Database is empty; seeding starter movies")
        for (tmdb_id, title, year, poster_path, director, genres,
             runtime, overview, list_type, added_by) in SEED_MOVIES:
            add_movie(
                tmdb_id=tmdb_id,
                title=title,
                year=year,
                poster_path=poster_path,
                director=director,
                genres=genres,
                runtime=runtime,
                overview=overview,
                list_type=list_type,
                added_by=added_by,
            )
        _startup_log("Seed complete")
    else:
        _startup_log(f"Seed skipped; movies already present ({count})")


init_db()
_seed_if_empty()
