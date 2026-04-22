import re
import streamlit as st

st.set_page_config(
    page_title="Adam & Sean Movie Night",
    page_icon="\U0001F4FC",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from pages import add_movie, pick_for_us, our_lists, watch_log
from styles import inject_css, app_header_html
from database import (
    get_db_status,
    get_movies_missing_posters,
    get_storage_guardrail_status,
    update_movie_metadata,
)
from tmdb_api import search_movies, get_movie_details

_YEAR_RE = re.compile(r"\s*\((\d{4})\)\s*$")

NAV_ITEMS = [
    {"key": "\U0001F3AC Add", "label": "🎬\nADD", "slug": "add", "fn": add_movie.render},
    {"key": "\U0001F3B0 Pick", "label": "🎰\nPICK", "slug": "pick", "fn": pick_for_us.render},
    {"key": "\U0001F4CB Lists", "label": "📋\nLISTS", "slug": "lists", "fn": our_lists.render},
    {"key": "\U0001F4FC Log", "label": "📼\nLOG", "slug": "log", "fn": watch_log.render},
]


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


def _current_page():
    slug_to_key = {item["slug"]: item["key"] for item in NAV_ITEMS}

    requested_slug = st.query_params.get("page")
    if requested_slug in slug_to_key:
        st.session_state.current_page = slug_to_key[requested_slug]
    elif "current_page" not in st.session_state:
        st.session_state.current_page = "\U0001F3AC Add"

    current_page = st.session_state.current_page
    current_slug = next(item["slug"] for item in NAV_ITEMS if item["key"] == current_page)
    if st.query_params.get("page") != current_slug:
        st.query_params["page"] = current_slug

    return current_page


def _render_top_nav(current_page):
    with st.container():
        st.markdown('<div class="top-nav-widget-anchor"></div>', unsafe_allow_html=True)
        st.markdown('<div class="workflow-label">Navigate</div>', unsafe_allow_html=True)
        choice = st.segmented_control(
            "Navigate",
            [item["key"] for item in NAV_ITEMS],
            default=current_page,
            key="top_nav_choice",
            label_visibility="collapsed",
        )
    if choice and choice != current_page:
        st.session_state.current_page = choice
        target_slug = next(item["slug"] for item in NAV_ITEMS if item["key"] == choice)
        st.query_params["page"] = target_slug
        st.rerun()


def main():
    inject_css()
    _backfill_posters()

    st.markdown(app_header_html(), unsafe_allow_html=True)

    page = _current_page()
    _render_top_nav(page)

    db_status = get_db_status()
    if db_status.get("fallback"):
        st.warning(
            "**Database connection failed** — running on local SQLite. "
            "Data won't persist across app restarts or be shared between users.",
            icon="\u26a0\ufe0f",
        )
    else:
        guardrail = get_storage_guardrail_status()
        if guardrail["percent_used"] >= 90:
            st.warning(
                (
                    "Movie storage guardrail is nearly full "
                    f"({guardrail['count']}/{guardrail['max_movies']}). "
                    "Consider removing older entries."
                ),
                icon="⚠️",
            )

    render_map = {item["key"]: item["fn"] for item in NAV_ITEMS}
    render_map[page]()


if __name__ == "__main__":
    main()
