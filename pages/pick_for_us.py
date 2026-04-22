import random
import time
from html import escape
import streamlit as st
from styles import inject_css, genre_pills_html, runtime_display, POSTER_PLACEHOLDER
from tmdb_api import poster_url
from database import get_unwatched_movies, get_all_genres, mark_watched


def _has_genre(movie, genre_filter):
    movie_genres = movie.get("genres_list", [])
    return any(g in movie_genres for g in genre_filter)



def _runtime_label(total_minutes):
    hours, minutes = divmod(int(total_minutes), 60)
    return f"{hours}h {minutes:02d}m"

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

    list_labels = {
        "adam_pick": "Adam's Pick",
        "sean_pick": "Sean's Pick",
        "mutual": "Mutual Discovery",
    }

    facts = []
    if movie.get("year"):
        facts.append(str(movie["year"]))
    if movie.get("director"):
        facts.append(f"Dir. {movie['director']}")
    if movie.get("runtime"):
        facts.append(runtime_display(movie["runtime"]))
    facts.append(list_labels.get(movie["list_type"], movie["list_type"]))

    facts_html = "".join(
        f'<span class="pick-meta-pill">{escape(fact)}</span>'
        for fact in facts
    )

    with st.container():
        st.markdown('<div class="pick-result-anchor"></div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="pick-result-kicker">Tonight\'s Movie</div>',
                    unsafe_allow_html=True)

        img = (poster_url(movie["poster_path"])
               if movie["poster_path"] else POSTER_PLACEHOLDER)
        cols = st.columns([0.85, 1.35], gap="large")
        with cols[0]:
            st.image(img, width="stretch")
        with cols[1]:
            st.markdown(
                f'<h2 class="pick-result-title">{escape(movie["title"])}</h2>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="pick-meta-band">{facts_html}</div>',
                unsafe_allow_html=True,
            )
            if movie["genres_list"]:
                st.markdown(genre_pills_html(movie["genres_list"]),
                            unsafe_allow_html=True)
            if movie["overview"]:
                st.markdown(
                    f'<p class="pick-result-overview">{escape(movie["overview"])}</p>',
                    unsafe_allow_html=True,
                )

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
            st.markdown('<div class="pick-reveal-anchor"></div>',
                        unsafe_allow_html=True)
            st.markdown(
                '<div class="pick-reveal-copy">Finding your perfect tape...</div>',
                unsafe_allow_html=True,
            )
            cols = st.columns([1, 2, 1])
            with cols[1]:
                st.image(img, width=160)
                st.markdown(f"#### {movie['title']}")
        delay = 0.08 + (i * 0.04)
        time.sleep(delay)

    final = random.choice(filtered)
    st.session_state["picked_movie"] = final
    placeholder.empty()
    _show_picked_movie(final, celebrate=True)


def _pick_button(filtered):
    pick_clicked = st.button(
        "\U0001F3B2 PICK FOR US!",
        type="primary",
        width="stretch",
        key="pick_btn",
    )

    if pick_clicked:
        _run_reveal(filtered)


def _filter_bar(movies):
    list_filter = st.pills(
        "Whose picks?",
        ["All", "Adam's Picks", "Sean's Picks", "Mutual Discoveries"],
        default="All",
        key="pick_list_filter",
    )

    list_map = {
        "All": None,
        "Adam's Picks": "adam_pick",
        "Sean's Picks": "sean_pick",
        "Mutual Discoveries": "mutual",
    }
    lt = list_map.get(list_filter, None)
    if lt:
        movies = [m for m in movies if m["list_type"] == lt]

    available_genres = get_all_genres()
    if available_genres:
        genre_filter = st.pills(
            "Genres",
            available_genres,
            selection_mode="multi",
            key="pick_genre_filter",
        )
    else:
        genre_filter = []

    min_runtime, max_runtime = st.slider(
        "Runtime range (minutes)", 0, 300, (0, 300), step=5,
        key="pick_runtime",
        format_func=_runtime_label,
    )
    st.caption(
        f"Runtime selected: {_runtime_label(min_runtime)} - {_runtime_label(max_runtime)}"
    )

    if genre_filter:
        movies = [m for m in movies if _has_genre(m, genre_filter)]

    movies = [
        m for m in movies
        if not m["runtime"] or min_runtime <= m["runtime"] <= max_runtime
    ]

    return movies


def render():
    inject_css()
    st.markdown('<div class="pick-page-anchor"></div>',
                unsafe_allow_html=True)

    all_movies = get_unwatched_movies()
    if not all_movies:
        st.info("No unwatched movies yet! Head over to **Add a Movie** "
                "to build your list.")
        return

    with st.container():
        st.markdown('<div class="pick-result-anchor"></div>',
                    unsafe_allow_html=True)
        if st.session_state.get("picked_movie"):
            _show_picked_movie(st.session_state["picked_movie"])
        elif st.session_state.get("watching_movie"):
            _watch_form(st.session_state["watching_movie"])
        else:
            st.markdown('<div class="pick-result-kicker">Tonight\'s Movie</div>',
                        unsafe_allow_html=True)
            st.caption("Spin below to pick tonight's movie.")

    with st.container():
        st.markdown('<div class="pick-filter-panel-anchor"></div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="pick-panel-line"></div>',
                    unsafe_allow_html=True)

        filtered = _filter_bar(all_movies)

        if not filtered:
            st.warning("No movies match those filters. Try broadening your "
                       "search or add more movies!")
            return

        st.markdown(
            (
                '<div class="pick-pool-banner">'
                '<div class="pick-pool-copy">Matching tapes</div>'
                f'<div class="pick-pool-count">{len(filtered)}</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

        _pick_button(filtered)
