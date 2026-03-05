import random
import time
import streamlit as st
from styles import (inject_css, genre_pills_html, runtime_display,
                    stars_html, section_header, POSTER_PLACEHOLDER)
from tmdb_api import poster_url
from database import get_unwatched_movies, get_all_genres, mark_watched


VIBE_PRESETS = {
    "Quick Watch": {"max_runtime": 100, "genres": []},
    "Epic Night": {"min_runtime": 150, "genres": []},
    "Feel Good": {"genres": ["Comedy", "Romance", "Animation", "Family"]},
    "Edge of Our Seats": {"genres": ["Action", "Thriller", "Horror", "Crime"]},
    "Deep Dive": {"genres": ["Drama", "Documentary", "History"]},
}


def _apply_vibe(cfg):
    if cfg.get("genres"):
        st.session_state["pick_genre_filter"] = cfg["genres"]
    else:
        st.session_state["pick_genre_filter"] = []
    if cfg.get("max_runtime"):
        st.session_state["pick_runtime"] = cfg["max_runtime"]
    elif cfg.get("min_runtime"):
        st.session_state["pick_runtime"] = 300
    else:
        st.session_state["pick_runtime"] = 300


def _has_genre(movie, genre_filter):
    movie_genres = movie.get("genres_list", [])
    return any(g in movie_genres for g in genre_filter)


def _watch_form(movie):
    st.markdown(f"### Rate **{movie['title']}**")
    c1, c2 = st.columns(2)
    with c1:
        adam_r = st.slider("Adam's rating", 1, 10, 7, key="pick_adam_r")
    with c2:
        sean_r = st.slider("Sean's rating", 1, 10, 7, key="pick_sean_r")
    notes = st.text_area("Notes (optional)", key="pick_notes",
                         placeholder="e.g. Great pick!")
    watch_date = st.date_input("Date watched", key="pick_wd")
    if st.button("Save to Watch Log", key="pick_save_watch", type="primary",
                 width="stretch"):
        mark_watched(movie["id"], adam_r, sean_r, notes, watch_date)
        st.session_state["watching_movie"] = None
        st.toast(f"**{movie['title']}** saved to your Watch Log!",
                 icon="\U0001F37F")
        st.balloons()
        st.rerun()


def _show_picked_movie(movie, celebrate=False):
    if celebrate:
        st.balloons()

    st.markdown("---")
    section_header("\U0001F37F Tonight's Movie")

    img = (poster_url(movie["poster_path"])
           if movie["poster_path"] else POSTER_PLACEHOLDER)
    cols = st.columns([1, 2])
    with cols[0]:
        st.image(img, width="stretch")
    with cols[1]:
        st.markdown(f"# {movie['title']}")
        st.markdown(f"**{movie['year'] or '?'}**")
        if movie["director"]:
            st.markdown(f"**Director:** {movie['director']}")
        if movie["genres_list"]:
            st.markdown(genre_pills_html(movie["genres_list"]),
                        unsafe_allow_html=True)
        if movie["runtime"]:
            st.markdown(f"**Runtime:** {runtime_display(movie['runtime'])}")
        if movie["overview"]:
            st.markdown(movie["overview"])

        list_labels = {
            "adam_pick": "Adam's Pick",
            "sean_pick": "Sean's Pick",
            "mutual": "Mutual Discovery",
        }
        st.caption(
            f"From: {list_labels.get(movie['list_type'], movie['list_type'])}"
        )

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("\U0001F3B2 Spin Again", key="spin_again",
                     width="stretch"):
            st.session_state["picked_movie"] = None
            st.rerun()
    with c2:
        if st.button("\u2705 Let's Watch This!", key="lets_watch",
                     type="primary", width="stretch"):
            st.session_state["watching_movie"] = movie
            st.session_state["picked_movie"] = None
            st.rerun()

    if st.session_state.get("watching_movie"):
        _watch_form(st.session_state["watching_movie"])


def _run_reveal(filtered):
    placeholder = st.empty()

    steps = 18
    for i in range(steps):
        movie = random.choice(filtered)
        img = (poster_url(movie["poster_path"])
               if movie["poster_path"] else POSTER_PLACEHOLDER)
        with placeholder.container():
            st.markdown("### \U0001F4FC Finding your perfect tape...")
            cols = st.columns([1, 2, 1])
            with cols[1]:
                st.image(img, width="stretch")
                st.markdown(f"#### {movie['title']}")
        delay = 0.08 + (i * 0.04)
        time.sleep(delay)

    final = random.choice(filtered)
    st.session_state["picked_movie"] = final
    placeholder.empty()
    _show_picked_movie(final, celebrate=True)


def _pick_button(filtered):
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        pick_clicked = st.button(
            "\U0001F3B2 PICK FOR US!",
            type="primary",
            width="stretch",
            key="pick_btn",
        )

    if pick_clicked:
        _run_reveal(filtered)
    elif st.session_state.get("picked_movie"):
        _show_picked_movie(st.session_state["picked_movie"])


def _filter_bar(movies):
    with st.expander("\U0001F527 Filters & Vibes", expanded=False):
        list_filter = st.radio(
            "Whose picks?",
            ["All", "Adam's Picks", "Sean's Picks", "Mutual Discoveries"],
            horizontal=True,
            key="pick_list_filter",
        )

        list_map = {
            "All": None,
            "Adam's Picks": "adam_pick",
            "Sean's Picks": "sean_pick",
            "Mutual Discoveries": "mutual",
        }
        lt = list_map[list_filter]
        if lt:
            movies = [m for m in movies if m["list_type"] == lt]

        available_genres = get_all_genres()
        genre_filter = st.multiselect("Genres", available_genres,
                                      key="pick_genre_filter")

        max_runtime = st.slider(
            "Max runtime (minutes)", 60, 300, 300, step=10,
            key="pick_runtime",
        )

        st.markdown("**Quick vibes:**")
        vibe_cols = st.columns(len(VIBE_PRESETS))
        for i, (vibe_name, vibe_cfg) in enumerate(VIBE_PRESETS.items()):
            with vibe_cols[i]:
                if st.button(vibe_name, key=f"vibe_{vibe_name}",
                             width="stretch"):
                    _apply_vibe(vibe_cfg)
                    st.rerun()

    if genre_filter:
        movies = [m for m in movies if _has_genre(m, genre_filter)]

    movies = [m for m in movies
              if (m["runtime"] or 0) <= max_runtime or not m["runtime"]]

    return movies


def render():
    inject_css()
    section_header("\U0001F3B0 Pick for Us")
    st.caption("Let fate decide your movie night. Set your filters and spin!")

    all_movies = get_unwatched_movies()
    if not all_movies:
        st.info("No unwatched movies yet! Head over to **Add a Movie** "
                "to build your list.")
        return

    filtered = _filter_bar(all_movies)

    if not filtered:
        st.warning("No movies match those filters. Try broadening your "
                   "search or add more movies!")
        return

    st.markdown(f"**{len(filtered)}** tapes in the pool")

    _pick_button(filtered)
