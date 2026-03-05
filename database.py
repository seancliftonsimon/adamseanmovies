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


init_db()
