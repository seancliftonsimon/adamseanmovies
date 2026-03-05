import sqlite3
import json
from datetime import datetime, date
from pathlib import Path

DB_PATH = Path(__file__).parent / "movies.db"


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
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
    """)
    conn.commit()
    conn.close()


def add_movie(tmdb_id, title, year, poster_path, director, genres, runtime,
              overview, list_type, added_by):
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO movies (tmdb_id, title, year, poster_path, director,
                                genres, runtime, overview, list_type, added_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tmdb_id, title, year, poster_path, director,
              json.dumps(genres) if isinstance(genres, list) else genres,
              runtime, overview, list_type, added_by))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_unwatched_movies(list_type=None):
    conn = get_connection()
    if list_type:
        rows = conn.execute(
            "SELECT * FROM movies WHERE watched = 0 AND list_type = ? ORDER BY added_date DESC",
            (list_type,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM movies WHERE watched = 0 ORDER BY added_date DESC"
        ).fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def get_watched_movies():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM movies WHERE watched = 1 ORDER BY watched_date DESC"
    ).fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def mark_watched(movie_id, adam_rating=None, sean_rating=None, notes=None,
                 watched_date=None):
    conn = get_connection()
    if watched_date is None:
        watched_date = date.today().isoformat()
    elif isinstance(watched_date, date):
        watched_date = watched_date.isoformat()
    conn.execute("""
        UPDATE movies
        SET watched = 1, watched_date = ?, adam_rating = ?, sean_rating = ?, notes = ?
        WHERE id = ?
    """, (watched_date, adam_rating, sean_rating, notes, movie_id))
    conn.commit()
    conn.close()


def remove_movie(movie_id):
    conn = get_connection()
    conn.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    conn.commit()
    conn.close()


def movie_exists(tmdb_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, title, list_type, watched FROM movies WHERE tmdb_id = ?",
        (tmdb_id,)
    ).fetchone()
    conn.close()
    return _row_to_dict(row) if row else None


def get_all_genres():
    conn = get_connection()
    rows = conn.execute(
        "SELECT genres FROM movies WHERE watched = 0"
    ).fetchall()
    conn.close()
    all_genres = set()
    for row in rows:
        try:
            genres = json.loads(row["genres"])
            all_genres.update(genres)
        except (json.JSONDecodeError, TypeError):
            pass
    return sorted(all_genres)


def get_watch_stats():
    conn = get_connection()
    watched = conn.execute(
        "SELECT * FROM movies WHERE watched = 1"
    ).fetchall()
    conn.close()

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
    d = dict(row)
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
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
    if count == 0:
        for (tmdb_id, title, year, poster_path, director, genres,
             runtime, overview, list_type, added_by) in SEED_MOVIES:
            conn.execute("""
                INSERT OR IGNORE INTO movies
                    (tmdb_id, title, year, poster_path, director, genres,
                     runtime, overview, list_type, added_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (tmdb_id, title, year, poster_path, director,
                  json.dumps(genres), runtime, overview, list_type, added_by))
        conn.commit()
    conn.close()


init_db()
_seed_if_empty()
