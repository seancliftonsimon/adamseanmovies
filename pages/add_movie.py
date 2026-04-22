import streamlit as st
from styles import (
    inject_css,
    POSTER_PLACEHOLDER,
    page_intro_html,
    panel_start_html,
    panel_end_html,
    workflow_label_html,
    empty_state_html,
    result_summary_html,
)
from tmdb_api import search_movies, get_movie_details, small_poster_url
from database import add_movie, movie_exists


LIST_OPTIONS = ["Adam", "Shared", "Sean"]
LIST_MAP = {
    "Adam": ("adam_pick", "Adam"),
    "Shared": ("mutual", "Both"),
    "Sean": ("sean_pick", "Sean"),
}
LIST_LABELS = {
    "adam_pick": "Adam's Picks",
    "sean_pick": "Sean's Picks",
    "mutual": "Mutual Discoveries",
}


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

    try:
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
    except RuntimeError as exc:
        st.toast(str(exc), icon="⚠️")
        return

    if success:
        if "added_movies" not in st.session_state:
            st.session_state.added_movies = set()
        st.session_state.added_movies.add(tmdb_id)
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
    st.markdown(
        page_intro_html(
            "Add a Movie",
            "Stock the Shelves",
            "Pick a shelf, search TMDb, and add the right tape in one flow.",
        ),
        unsafe_allow_html=True,
    )

    st.markdown(panel_start_html("Workflow"), unsafe_allow_html=True)
    st.markdown(workflow_label_html("1. Choose a shelf"), unsafe_allow_html=True)
    selection = st.pills(
        "Add to",
        LIST_OPTIONS,
        default="Adam",
        key="add_list_selection",
    )

    if not selection:
        st.markdown(
            empty_state_html(
                "Choose a shelf to continue",
                "Tap a name above to choose which list to add to.",
            ),
            unsafe_allow_html=True,
        )
        st.markdown(panel_end_html(), unsafe_allow_html=True)
        return

    list_type, added_by = LIST_MAP[selection]
    btn_label = LIST_LABELS[list_type]

    st.markdown(workflow_label_html("2. Search for a movie"), unsafe_allow_html=True)
    query = st.text_input(
        "Search for a movie",
        placeholder="e.g. Eternal Sunshine, The Grand Budapest Hotel...",
        key="add_search_query",
    )

    st.markdown(panel_end_html(), unsafe_allow_html=True)

    if not query:
        return

    with st.spinner("Searching TMDb..."):
        try:
            results, total = search_movies(query.strip())
        except Exception as e:
            st.error(f"Search failed: {e}")
            return

    if not results:
        st.markdown(
            empty_state_html(
                "No movies found",
                "Try a different search term.",
            ),
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        result_summary_html(
            f"Showing {min(len(results), 12)} of {total} results",
            f"Target shelf: {btn_label}",
        ),
        unsafe_allow_html=True,
    )

    added_set = st.session_state.get("added_movies", set())

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
        already_added = tmdb_id in added_set

        with st.container(border=True):
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(img or POSTER_PLACEHOLDER, width=80)
            with cols[1]:
                st.markdown(f"**{title}** ({year})")
                if overview_short:
                    st.caption(overview_short)
                if already_added:
                    st.button(
                        "\u2705 Added!",
                        key=f"add_{tmdb_id}",
                        disabled=True,
                        width="stretch",
                    )
                elif st.button(
                    f"\u2795 Add to {btn_label}",
                    key=f"add_{tmdb_id}",
                    type="primary",
                    width="stretch",
                ):
                    _quick_add(tmdb_id, list_type, added_by)
