import re
import streamlit as st

st.set_page_config(
    page_title="Adam & Sean Movie Night",
    page_icon="\U0001F4FC",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from pages import add_movie, pick_for_us, our_lists, watch_log
from styles import inject_css, app_header_html
from database import get_db_status, get_movies_missing_posters, update_movie_metadata
from tmdb_api import search_movies, get_movie_details

_YEAR_RE = re.compile(r"\s*\((\d{4})\)\s*$")

NAV_ITEMS = [
    ("\U0001F3AC Add",  "🎬\nADD",  add_movie.render),
    ("\U0001F3B0 Pick", "🎰\nPICK", pick_for_us.render),
    ("\U0001F4CB Lists","📋\nLISTS", our_lists.render),
    ("\U0001F4FC Log",  "📼\nLOG",  watch_log.render),
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
    if "current_page" not in st.session_state:
        st.session_state.current_page = "\U0001F3AC Add"
    return st.session_state.current_page


def _render_bottom_nav(current_page):
    """Four real Streamlit buttons — active one is primary (yellow)."""
    st.markdown('<div class="bnav-anchor"></div>', unsafe_allow_html=True)
    cols = st.columns(4, gap="small")
    for i, (page_key, btn_label, _) in enumerate(NAV_ITEMS):
        with cols[i]:
            if st.button(
                btn_label,
                key=f"bnav_{i}",
                type="primary" if page_key == current_page else "secondary",
                use_container_width=True,
            ):
                st.session_state.current_page = page_key
                st.rerun()


def main():
    inject_css()
    _backfill_posters()

    st.markdown(app_header_html(), unsafe_allow_html=True)

    db_status = get_db_status()
    if db_status.get("fallback"):
        st.warning(
            "**Database connection failed** — running on local SQLite. "
            "Data won't persist across app restarts or be shared between users.",
            icon="\u26a0\ufe0f",
        )

    page = _current_page()
    render_map = {key: fn for key, _, fn in NAV_ITEMS}
    render_map[page]()

    _render_bottom_nav(page)


if __name__ == "__main__":
    main()
