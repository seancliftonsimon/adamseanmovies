import streamlit as st
from styles import inject_css, section_header, POSTER_PLACEHOLDER
from tmdb_api import search_movies, get_movie_details, small_poster_url
from database import add_movie, movie_exists


LIST_OPTIONS = ["Adam's Pick", "Mutual Discovery", "Sean's Pick"]
LIST_MAP = {
    "Adam's Pick": "adam_pick",
    "Mutual Discovery": "mutual",
    "Sean's Pick": "sean_pick",
}
LIST_LABELS = {
    "adam_pick": "Adam's Picks",
    "sean_pick": "Sean's Picks",
    "mutual": "Mutual Discoveries",
}


def _sync_user_to_sidebar():
    val = st.session_state.page_user_select
    st.session_state.current_user = val
    if "user_select" in st.session_state:
        st.session_state.user_select = val


def _quick_add(tmdb_id, list_type, added_by):
    existing = movie_exists(tmdb_id)
    if existing:
        label = LIST_LABELS.get(existing["list_type"], existing["list_type"])
        status = "watched" if existing["watched"] else "unwatched"
        st.toast(
            f"{existing['title']} is already in {label} ({status})",
            icon="\u26a0\ufe0f",
        )
        return

    try:
        details = get_movie_details(tmdb_id)
    except Exception as e:
        st.toast(f"Could not load details: {e}", icon="\u274c")
        return

    success = add_movie(
        tmdb_id=details["tmdb_id"],
        title=details["title"],
        year=details["year"],
        poster_path=details["poster_path"],
        director=details["director"],
        genres=details["genres"],
        runtime=details["runtime"],
        overview=details["overview"],
        list_type=list_type,
        added_by=added_by,
    )

    if success:
        st.toast(
            f"Added **{details['title']}** to {LIST_LABELS[list_type]}!",
            icon="\U0001F37F",
        )
        st.balloons()
        st.rerun()
    else:
        st.toast("This movie is already in your collection!", icon="\u26a0\ufe0f")


def render():
    inject_css()
    section_header("\U0001F3AC Add a Movie")

    if "page_user_select" not in st.session_state:
        st.session_state.page_user_select = st.session_state.get(
            "current_user", "Adam"
        )

    who = st.radio(
        "Who's adding?",
        ["Adam", "Sean"],
        horizontal=True,
        key="page_user_select",
        on_change=_sync_user_to_sidebar,
    )
    st.session_state.current_user = who

    default_list = "Adam's Pick" if who == "Adam" else "Sean's Pick"
    if "add_list_type" not in st.session_state:
        st.session_state.add_list_type = default_list

    list_label = st.select_slider(
        "Add to list",
        options=LIST_OPTIONS,
        key="add_list_type",
    )
    list_type = LIST_MAP[list_label]

    query = st.text_input(
        "Search for a movie",
        placeholder="e.g. Eternal Sunshine, The Grand Budapest Hotel...",
        key="add_search_query",
    )

    if not query:
        return

    with st.spinner("Searching TMDb..."):
        try:
            results, total = search_movies(query.strip())
        except Exception as e:
            st.error(f"Search failed: {e}")
            return

    if not results:
        st.info("No movies found. Try a different search term.")
        return

    st.caption(f"Showing {min(len(results), 12)} of {total} results")

    for movie in results[:12]:
        tmdb_id = movie["id"]
        title = movie.get("title", "Unknown")
        rd = movie.get("release_date", "")
        year = rd[:4] if rd else "?"
        overview_raw = movie.get("overview", "") or ""
        overview_short = (
            overview_raw[:100] + "..." if len(overview_raw) > 100
            else overview_raw
        )
        img = small_poster_url(movie.get("poster_path"))

        with st.container(border=True):
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(img or POSTER_PLACEHOLDER, width=80)
            with cols[1]:
                st.markdown(f"**{title}** ({year})")
                if overview_short:
                    st.caption(overview_short)
                if st.button(
                    f"\u2795 Add to {list_label}",
                    key=f"add_{tmdb_id}",
                    type="primary",
                    width="stretch",
                ):
                    _quick_add(tmdb_id, list_type, who)
