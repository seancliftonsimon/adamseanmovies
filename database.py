import json
import os
import sqlite3
from datetime import date, datetime
from pathlib import Path

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
        conn = get_connection()
        cur = conn.cursor()
        try:
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
        finally:
            cur.close()
            conn.close()
        return

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


init_db()
