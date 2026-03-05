import requests
import streamlit as st

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p"


def _auth_kwargs():
    token = st.secrets.get("TMDB_READ_TOKEN", "").strip()
    api_key = st.secrets.get("TMDB_API_KEY", "").strip()

    if token:
        return {
            "headers": {
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
            },
            "base_params": {},
        }

    if api_key:
        return {
            "headers": {"accept": "application/json"},
            "base_params": {"api_key": api_key},
        }

    raise RuntimeError(
        "TMDB credentials are missing. Add TMDB_READ_TOKEN or TMDB_API_KEY to Streamlit secrets."
    )


def _request_tmdb(path, params=None):
    auth = _auth_kwargs()
    merged_params = dict(auth["base_params"])
    if params:
        merged_params.update(params)

    resp = requests.get(
        f"{BASE_URL}{path}",
        headers=auth["headers"],
        params=merged_params,
        timeout=10,
    )
    try:
        resp.raise_for_status()
    except requests.HTTPError as exc:
        if resp.status_code == 401:
            raise RuntimeError(
                "TMDB auth failed (401). Verify TMDB_READ_TOKEN or TMDB_API_KEY in Streamlit secrets."
            ) from exc
        raise
    return resp.json()


@st.cache_data(ttl=86400, show_spinner=False)
def search_movies(query, page=1):
    data = _request_tmdb(
        "/search/movie",
        params={"query": query, "page": page, "include_adult": False},
    )
    return data.get("results", []), data.get("total_results", 0)


@st.cache_data(ttl=86400, show_spinner=False)
def get_movie_details(tmdb_id):
    data = _request_tmdb(
        f"/movie/{tmdb_id}",
        params={"append_to_response": "credits"},
    )

    director = ""
    credits = data.get("credits", {})
    for member in credits.get("crew", []):
        if member.get("job") == "Director":
            director = member.get("name", "")
            break

    genres = [g["name"] for g in data.get("genres", [])]

    release_year = None
    rd = data.get("release_date", "")
    if rd and len(rd) >= 4:
        try:
            release_year = int(rd[:4])
        except ValueError:
            pass

    return {
        "tmdb_id": data["id"],
        "title": data.get("title", "Unknown"),
        "year": release_year,
        "poster_path": data.get("poster_path"),
        "director": director,
        "genres": genres,
        "runtime": data.get("runtime"),
        "overview": data.get("overview", ""),
        "vote_average": data.get("vote_average", 0),
    }


def poster_url(poster_path, size="w500"):
    if not poster_path:
        return None
    return f"{IMAGE_BASE}/{size}{poster_path}"


def small_poster_url(poster_path):
    return poster_url(poster_path, size="w185")
