import requests
import streamlit as st

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p"


def _get_headers():
    token = st.secrets.get("TMDB_READ_TOKEN", "")
    return {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
    }


def _get_api_key():
    return st.secrets.get("TMDB_API_KEY", "")


@st.cache_data(ttl=86400, show_spinner=False)
def search_movies(query, page=1):
    resp = requests.get(
        f"{BASE_URL}/search/movie",
        headers=_get_headers(),
        params={"query": query, "page": page, "include_adult": False},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("results", []), data.get("total_results", 0)


@st.cache_data(ttl=86400, show_spinner=False)
def get_movie_details(tmdb_id):
    resp = requests.get(
        f"{BASE_URL}/movie/{tmdb_id}",
        headers=_get_headers(),
        params={"append_to_response": "credits"},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()

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
