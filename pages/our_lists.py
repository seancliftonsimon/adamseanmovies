import streamlit as st
from styles import (inject_css, genre_pills_html, runtime_display,
                    POSTER_PLACEHOLDER)
from database import get_unwatched_movies, remove_movie, mark_watched
from tmdb_api import poster_url as make_poster_url


def render():
    inject_css()
    st.title("\U0001F4CB Our Lists")
    st.caption("Browse all the movies waiting to be watched.")

    adam_movies = get_unwatched_movies("adam_pick")
    sean_movies = get_unwatched_movies("sean_pick")
    mutual_movies = get_unwatched_movies("mutual")

    tab_adam, tab_sean, tab_mutual = st.tabs([
        f"Adam's Picks ({len(adam_movies)})",
        f"Sean's Picks ({len(sean_movies)})",
        f"Mutual Discoveries ({len(mutual_movies)})",
    ])

    with tab_adam:
        _render_list(adam_movies, "adam")
    with tab_sean:
        _render_list(sean_movies, "sean")
    with tab_mutual:
        _render_list(mutual_movies, "mutual")


def _render_list(movies, prefix):
    if not movies:
        st.info("No movies here yet! Head over to **Add a Movie** to get started.")
        return

    sort_option = st.selectbox(
        "Sort by",
        ["Recently Added", "Title A\u2013Z", "Shortest First", "Longest First"],
        key=f"sort_{prefix}",
    )
    movies = _sort_movies(movies, sort_option)

    for movie in movies:
        img = make_poster_url(movie["poster_path"], "w185") if movie["poster_path"] else POSTER_PLACEHOLDER
        with st.expander(f"**{movie['title']}** ({movie['year'] or '?'})  \u2014  {runtime_display(movie['runtime'])}"):
            cols = st.columns([1, 2])
            with cols[0]:
                st.image(img, use_container_width=True)
            with cols[1]:
                if movie["director"]:
                    st.markdown(f"**Director:** {movie['director']}")
                if movie["genres_list"]:
                    st.markdown(genre_pills_html(movie["genres_list"]), unsafe_allow_html=True)
                if movie["runtime"]:
                    st.markdown(f"**Runtime:** {runtime_display(movie['runtime'])}")
                if movie["overview"]:
                    st.caption(movie["overview"])

            action_cols = st.columns([1, 1, 2])
            with action_cols[0]:
                if st.button("\u2705 We watched this!", key=f"watch_{prefix}_{movie['id']}",
                             use_container_width=True):
                    st.session_state[f"rating_movie_{movie['id']}"] = movie
            with action_cols[1]:
                if st.button("\U0001F5D1\uFE0F Remove", key=f"rm_{prefix}_{movie['id']}",
                             use_container_width=True):
                    st.session_state[f"confirm_remove_{movie['id']}"] = True

            if st.session_state.get(f"confirm_remove_{movie['id']}"):
                st.warning(f"Remove **{movie['title']}** from the list?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Yes, remove", key=f"confirm_yes_{prefix}_{movie['id']}",
                                 use_container_width=True):
                        remove_movie(movie["id"])
                        del st.session_state[f"confirm_remove_{movie['id']}"]
                        st.toast(f"Removed {movie['title']}", icon="\U0001F5D1")
                        st.rerun()
                with c2:
                    if st.button("Cancel", key=f"confirm_no_{prefix}_{movie['id']}",
                                 use_container_width=True):
                        del st.session_state[f"confirm_remove_{movie['id']}"]
                        st.rerun()

            if st.session_state.get(f"rating_movie_{movie['id']}"):
                _rating_form(movie, prefix)


def _rating_form(movie, prefix):
    st.markdown(f"### Rate **{movie['title']}**")
    c1, c2 = st.columns(2)
    with c1:
        adam_r = st.slider("Adam's rating", 1, 10, 7, key=f"ar_{prefix}_{movie['id']}")
    with c2:
        sean_r = st.slider("Sean's rating", 1, 10, 7, key=f"sr_{prefix}_{movie['id']}")
    notes = st.text_area("Notes (optional)", key=f"notes_{prefix}_{movie['id']}",
                         placeholder="e.g. We both cried...")
    watch_date = st.date_input("Date watched", key=f"wd_{prefix}_{movie['id']}")
    if st.button("Save to Watch Log", key=f"save_watch_{prefix}_{movie['id']}",
                 type="primary", use_container_width=True):
        mark_watched(movie["id"], adam_r, sean_r, notes, watch_date)
        del st.session_state[f"rating_movie_{movie['id']}"]
        st.toast(f"**{movie['title']}** added to your Watch Log!", icon="\U0001F37F")
        st.balloons()
        st.rerun()


def _sort_movies(movies, sort_option):
    if sort_option == "Title A\u2013Z":
        return sorted(movies, key=lambda m: (m["title"] or "").lower())
    elif sort_option == "Shortest First":
        return sorted(movies, key=lambda m: m["runtime"] or 9999)
    elif sort_option == "Longest First":
        return sorted(movies, key=lambda m: m["runtime"] or 0, reverse=True)
    return movies
