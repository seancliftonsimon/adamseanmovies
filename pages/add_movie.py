import streamlit as st
from styles import (inject_css, genre_pills_html, runtime_display,
                    section_header, POSTER_PLACEHOLDER)
from tmdb_api import search_movies, get_movie_details, poster_url, small_poster_url
from database import add_movie, movie_exists


def _save_movie(details, list_type, added_by):
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
    list_labels = {
        "adam_pick": "Adam's Picks",
        "sean_pick": "Sean's Picks",
        "mutual": "Mutual Discoveries",
    }
    if success:
        st.toast(f"Added **{details['title']}** to {list_labels[list_type]}!",
                 icon="\U0001F37F")
        st.session_state.selected_tmdb_id = None
        st.balloons()
        st.rerun()
    else:
        st.error("This movie is already in your collection!")
    return success


def _show_detail_and_add(tmdb_id, who):
    with st.spinner("Loading movie details..."):
        try:
            details = get_movie_details(tmdb_id)
        except Exception as e:
            st.error(f"Could not load details: {e}")
            return

    existing = movie_exists(tmdb_id)
    if existing:
        list_labels = {
            "adam_pick": "Adam's Picks",
            "sean_pick": "Sean's Picks",
            "mutual": "Mutual Discoveries",
        }
        label = list_labels.get(existing["list_type"], existing["list_type"])
        status = "watched" if existing["watched"] else "unwatched"
        st.warning(
            f"**{existing['title']}** is already in **{label}** ({status})."
        )
        if st.button("Back to search results", key="back_from_existing"):
            st.session_state.selected_tmdb_id = None
            st.rerun()
        return

    img = poster_url(details["poster_path"])

    st.subheader(f"{details['title']} ({details['year'] or '?'})")

    cols = st.columns([1, 2])
    with cols[0]:
        if img:
            st.image(img, width="stretch")
        else:
            st.image(POSTER_PLACEHOLDER, width="stretch")
    with cols[1]:
        if details["director"]:
            st.markdown(f"**Director:** {details['director']}")
        if details["genres"]:
            pills = genre_pills_html(details["genres"])
            st.markdown(pills, unsafe_allow_html=True)
        if details["runtime"]:
            st.markdown(f"**Runtime:** {runtime_display(details['runtime'])}")
        if details["vote_average"]:
            st.markdown(f"**TMDb Rating:** {details['vote_average']:.1f}/10")
        if details["overview"]:
            st.markdown(details["overview"])

    st.divider()
    st.markdown("**Which list should this go on?**")

    col1, col2, col3 = st.columns(3)
    added = False
    with col1:
        if st.button("\U0001F3AC Adam's Pick", key="add_adam",
                     width="stretch",
                     help="Adam has seen this and wants to share it"):
            added = _save_movie(details, "adam_pick", who)
    with col2:
        if st.button("\U0001F3AC Sean's Pick", key="add_sean",
                     width="stretch",
                     help="Sean has seen this and wants to share it"):
            added = _save_movie(details, "sean_pick", who)
    with col3:
        if st.button("\U0001F31F Mutual Discovery", key="add_mutual",
                     width="stretch",
                     help="Neither of us has seen this \u2014 we both want to!"):
            added = _save_movie(details, "mutual", who)

    if st.button("Cancel", key="cancel_add"):
        st.session_state.selected_tmdb_id = None
        st.rerun()


def _do_search(query, who):
    with st.spinner("Searching TMDb..."):
        try:
            results, total = search_movies(query.strip())
        except Exception as e:
            st.error(f"Search failed: {e}")
            return

    if not results:
        st.info("No movies found. Try a different search term.")
        return

    st.markdown(f"**{min(len(results), 20)} results** (of {total} total)")

    if "selected_tmdb_id" not in st.session_state:
        st.session_state.selected_tmdb_id = None

    for movie in results[:12]:
        tmdb_id = movie["id"]
        title = movie.get("title", "Unknown")
        rd = movie.get("release_date", "")
        year = rd[:4] if rd else "?"
        overview_short = (movie.get("overview", "") or "")[:120]
        if len(movie.get("overview", "")) > 120:
            overview_short += "..."
        img = small_poster_url(movie.get("poster_path"))

        cols = st.columns([1, 3])
        with cols[0]:
            if img:
                st.image(img, width="stretch")
            else:
                st.image(POSTER_PLACEHOLDER, width="stretch")
        with cols[1]:
            if st.button(f"**{title}** ({year})", key=f"sel_{tmdb_id}",
                         width="stretch"):
                st.session_state.selected_tmdb_id = tmdb_id
            if overview_short:
                st.caption(overview_short)

    if st.session_state.selected_tmdb_id:
        st.divider()
        _show_detail_and_add(st.session_state.selected_tmdb_id, who)


def render():
    inject_css()

    section_header("\U0001F3AC Add a Movie")
    st.caption("Search for a movie, preview it, and add it to the right list.")

    who = st.session_state.get("current_user", "Adam")

    query = st.text_input(
        "Search for a movie",
        placeholder="e.g. Eternal Sunshine, The Grand Budapest Hotel...",
        key="add_search_query",
    )

    if query:
        _do_search(query, who)
