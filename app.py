import re
import streamlit as st

st.set_page_config(
    page_title="Adam & Sean Movie Night",
    page_icon="\U0001F4FC",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from pages import add_movie, pick_for_us, our_lists, watch_log
from styles import inject_css
from database import get_db_status, get_movies_missing_posters, update_movie_metadata
from tmdb_api import search_movies, get_movie_details

_YEAR_RE = re.compile(r"\s*\((\d{4})\)\s*$")


def _backfill_posters():
    if st.session_state.get("_posters_backfilled"):
        return
    st.session_state["_posters_backfilled"] = True

    missing = get_movies_missing_posters()
    if not missing:
        return

    for movie in missing:
        title = movie["title"]
        m = _YEAR_RE.search(title)
        search_title = title[: m.start()].strip() if m else title
        year = int(m.group(1)) if m else None
        try:
            results, _ = search_movies(search_title, year=year)
            if not results and year:
                results, _ = search_movies(search_title)
            if not results:
                continue
            if year:
                year_filtered = [r for r in results if r.get("release_date", "")[:4] == str(year)]
                top = year_filtered[0] if year_filtered else results[0]
            else:
                top = results[0]
            details = get_movie_details(top["id"])
            update_movie_metadata(movie["id"], details)
        except Exception:
            pass

NAV_ITEMS = [
    ("\U0001F3AC Add", add_movie.render),
    ("\U0001F3B0 Pick", pick_for_us.render),
    ("\U0001F4CB Lists", our_lists.render),
    ("\U0001F4FC Log", watch_log.render),
]


def _render_top_menu():
    labels = [label for label, _ in NAV_ITEMS]
    selected = st.pills(
        "Menu",
        labels,
        default=labels[0],
        key="top_nav_menu",
    )
    return selected or labels[0]


def main():
    inject_css()
    _backfill_posters()

    db_status = get_db_status()
    if db_status.get("fallback"):
        st.warning(
            "**Database connection failed** — running on local SQLite. "
            "Data won't persist across app restarts or be shared between users. "
            "Check the DATABASE_URL in your Streamlit secrets and review the "
            "app logs for details.",
            icon="\u26a0\ufe0f",
        )

    selected_menu = _render_top_menu()
    render_map = dict(NAV_ITEMS)
    render_map[selected_menu]()


if __name__ == "__main__":
    main()
