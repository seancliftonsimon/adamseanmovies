import inspect
import random
import time
from html import escape
from textwrap import dedent

import streamlit as st

import database
from database import get_unwatched_movies, mark_watched
from styles import (
    POSTER_PLACEHOLDER,
    genre_pills_html,
    inject_css,
    runtime_display,
    page_intro_html,
    workflow_label_html,
    empty_state_html,
    result_summary_html,
)
from tmdb_api import poster_url

LIST_OPTIONS = ["All", "Adam's Picks", "Sean's Picks", "Mutual Discoveries"]
LIST_MAP = {
    "All": None,
    "Adam's Picks": "adam_pick",
    "Sean's Picks": "sean_pick",
    "Mutual Discoveries": "mutual",
}
RUNTIME_OPTIONS = ["Any Length", "Under 1h 30m", "Under 2h", "Under 2h 30m", "Custom"]
RUNTIME_LIMITS = {
    "Under 1h 30m": 90,
    "Under 2h": 120,
    "Under 2h 30m": 150,
}


def _runtime_label(total_minutes):
    total = max(0, int(total_minutes))
    hours, minutes = divmod(total, 60)
    if hours and minutes:
        return f"{hours}h {minutes:02d}m"
    if hours:
        return f"{hours}h"
    return f"{minutes}m"


def _watch_form(movie):
    st.markdown(f"### Rate **{movie['title']}**")
    c1, c2 = st.columns(2)
    with c1:
        adam_r = st.slider("Adam's rating", 1, 10, 7, key="pick_adam_r")
    with c2:
        sean_r = st.slider("Sean's rating", 1, 10, 7, key="pick_sean_r")
    notes = st.text_area("Notes (optional)", key="pick_notes", placeholder="e.g. Great pick!")
    watch_date = st.date_input("Date watched", key="pick_wd")
    if st.button("Save to Watch Log", key="pick_save_watch", type="primary", width="stretch"):
        mark_watched(movie["id"], adam_r, sean_r, notes, watch_date)
        st.session_state["watching_movie"] = None
        st.toast(f"**{movie['title']}** saved to your Watch Log!", icon="🍿")
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

    facts_html = "".join(f'<span class="pick-meta-pill">{escape(fact)}</span>' for fact in facts)

    with st.container():
        st.markdown('<div class="pick-result-anchor"></div>', unsafe_allow_html=True)
        st.markdown('<div class="pick-result-kicker">Tonight\'s Movie</div>', unsafe_allow_html=True)

        img = poster_url(movie["poster_path"]) if movie["poster_path"] else POSTER_PLACEHOLDER
        cols = st.columns([0.85, 1.35], gap="large")
        with cols[0]:
            st.image(img, width="stretch")
        with cols[1]:
            st.markdown(f'<h2 class="pick-result-title">{escape(movie["title"])}</h2>', unsafe_allow_html=True)
            st.markdown(f'<div class="pick-meta-band">{facts_html}</div>', unsafe_allow_html=True)
            if movie["genres_list"]:
                st.markdown(genre_pills_html(movie["genres_list"]), unsafe_allow_html=True)
            if movie["overview"]:
                st.markdown(f'<p class="pick-result-overview">{escape(movie["overview"])}</p>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎲 Spin Again", key="spin_again", width="stretch"):
                st.session_state["picked_movie"] = None
                st.rerun()
        with c2:
            if st.button("✅ Let's Watch This!", key="lets_watch", type="primary", width="stretch"):
                st.session_state["watching_movie"] = movie
                st.session_state["picked_movie"] = None
                st.rerun()



def _run_reveal(filtered, placeholder):
    speed_curve = [15, 12, 9, 7, 5.5, 4.2, 3.4, 2.8, 2.4, 2.1, 2.4, 2.9, 3.6, 4.5, 5.8, 7.2]
    winner = random.choice(filtered)
    for i, speed in enumerate(speed_curve):
        spotlight = random.choice(filtered)
        with placeholder.container():
            st.markdown(
                _poster_carousel_html(
                    filtered,
                    duration=max(1.8, speed),
                    show_ticker=True,
                    status=f"Spinning up..." if i < 5 else "Locking in your pick...",
                    spotlight_title=spotlight["title"],
                ),
                unsafe_allow_html=True,
            )
        time.sleep(0.08 + (i * 0.02))

    st.session_state["picked_movie"] = winner


def _poster_carousel_html(movies, duration=16, show_ticker=False, status=None, spotlight_title=None):
    if not movies:
        return ""

    sample_size = min(len(movies), 16)
    sample = random.sample(movies, sample_size) if len(movies) > sample_size else list(movies)
    posters = sample + sample + sample

    tiles = []
    for movie in posters:
        poster = poster_url(movie["poster_path"], "w185") if movie["poster_path"] else POSTER_PLACEHOLDER
        safe_title = escape(movie["title"])
        tiles.append(
            dedent(
                f"""
                <div class="pick-carousel-item">
                    <img src="{poster}" alt="{safe_title}" loading="lazy" />
                    <span>{safe_title}</span>
                </div>
                """
            ).strip()
        )

    ticker_html = '<div class="pick-carousel-ticker">▼</div>' if show_ticker else ""
    status_html = f'<div class="pick-carousel-status">{escape(status)}</div>' if status else ""
    spotlight_html = (
        f'<div class="pick-carousel-spotlight">{escape(spotlight_title)}</div>' if spotlight_title else ""
    )

    return dedent(
        f"""
        <div class="pick-carousel-wrap">
            {ticker_html}
            <div class="pick-carousel-track" style="--carousel-duration:{duration:.2f}s;">
                {''.join(tiles)}
            </div>
        </div>
        {status_html}
        {spotlight_html}
        """
    ).strip()


def _apply_filters(all_movies):
    filtered = list(all_movies)

    selected_list_label = st.session_state.get("pick_list_filter", "All")
    selected_list = LIST_MAP.get(selected_list_label)
    if selected_list:
        filtered = [m for m in filtered if m["list_type"] == selected_list]

    selected_genres = st.session_state.get("pick_genre_filter", [])
    if selected_genres:
        selected_set = set(selected_genres)
        filtered = [m for m in filtered if selected_set.intersection(m["genres_list"])]

    runtime_choice = st.session_state.get("pick_runtime_choice", "Any Length")
    custom_runtime = int(st.session_state.get("pick_custom_runtime", 150))
    if runtime_choice != "Any Length":
        max_runtime = custom_runtime if runtime_choice == "Custom" else RUNTIME_LIMITS[runtime_choice]
        filtered = [m for m in filtered if not m.get("runtime") or int(m["runtime"]) <= max_runtime]

    active_filters = []
    if selected_list_label != "All":
        active_filters.append(selected_list_label)
    if selected_genres:
        active_filters.extend(selected_genres)
    if runtime_choice != "Any Length":
        active_filters.append(f"Under {_runtime_label(custom_runtime)}" if runtime_choice == "Custom" else runtime_choice)

    return filtered, active_filters


def _active_filter_row(active_filters):
    if not active_filters:
        return
    pills = "".join(f'<span class="pick-meta-pill">{escape(item)}</span>' for item in active_filters)
    st.markdown(f'<div class="pick-active-filters">{pills}</div>', unsafe_allow_html=True)


def _runtime_selector():
    runtime_choice = st.pills(
        "Runtime",
        RUNTIME_OPTIONS,
        default=st.session_state.get("pick_runtime_choice", "Any Length"),
        key="pick_runtime_choice",
        label_visibility="collapsed",
    )

    custom_runtime = st.session_state.get("pick_custom_runtime", 150)
    if runtime_choice == "Custom":
        slider_sig = inspect.signature(st.slider)
        kwargs = {
            "label": "Custom max runtime",
            "min_value": 60,
            "max_value": 300,
            "value": custom_runtime,
            "step": 5,
            "key": "pick_custom_runtime",
        }
        if "label_visibility" in slider_sig.parameters:
            kwargs["label_visibility"] = "collapsed"
        custom_runtime = st.slider(**kwargs)

    return runtime_choice, custom_runtime


def _render_filters(all_movies):
    with st.container():
        st.markdown('<div class="pick-filters-card-anchor"></div>', unsafe_allow_html=True)

        st.markdown(workflow_label_html("Whose picks?"), unsafe_allow_html=True)
        st.pills(
            "Whose Picks?",
            LIST_OPTIONS,
            default=st.session_state.get("pick_list_filter", "All"),
            key="pick_list_filter",
            label_visibility="collapsed",
        )

        st.markdown(workflow_label_html("Genres"), unsafe_allow_html=True)
        available_genres = database.get_all_genres()
        st.pills(
            "Genres",
            available_genres,
            selection_mode="multi",
            key="pick_genre_filter",
            label_visibility="collapsed",
        ) if available_genres else []

        st.markdown(workflow_label_html("Runtime"), unsafe_allow_html=True)
        _runtime_selector()


def _render_results_card(filtered, has_optional_filters):
    pick_requested = False
    with st.container():
        has_results = len(filtered) > 0
        if has_results:
            st.markdown(
                result_summary_html(f"{len(filtered)} Tapes Ready", None),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                empty_state_html(
                    "No tapes match these filters",
                    None,
                ),
                unsafe_allow_html=True,
            )

        if st.button("Pick for Us", key="pick_btn", type="primary", width="stretch", disabled=not has_results):
            pick_requested = True

        if (not has_results) and has_optional_filters:
            if st.button("Clear All", key="clear_all_results", width="stretch"):
                st.session_state["pick_list_filter"] = "All"
                st.session_state["pick_genre_filter"] = []
                st.session_state["pick_runtime_choice"] = "Any Length"
                st.session_state["pick_custom_runtime"] = 150
                st.rerun()

    return pick_requested


def render():
    inject_css()
    st.markdown('<div class="pick-page-anchor"></div>', unsafe_allow_html=True)
    st.markdown(
        page_intro_html(
            None,
            "Pick For Us",
        ),
        unsafe_allow_html=True,
    )

    all_movies = get_unwatched_movies()
    if not all_movies:
        st.markdown(
            empty_state_html(
                "No unwatched movies yet",
                None,
            ),
            unsafe_allow_html=True,
        )
        return

    filtered, active_filters = _apply_filters(all_movies)
    has_optional_filters = bool(active_filters)

    st.markdown('<div class="pick-results-card-anchor"></div>', unsafe_allow_html=True)
    if active_filters:
        _active_filter_row(active_filters)

    carousel_slot = st.empty()
    with carousel_slot.container():
        st.markdown(
            _poster_carousel_html(
                filtered if filtered else all_movies,
                duration=18,
                show_ticker=False,
                status="Eligible posters are continuously rolling — press Pick for Us to spin.",
            ),
            unsafe_allow_html=True,
        )

    pick_requested = _render_results_card(filtered, has_optional_filters)

    _render_filters(all_movies)

    reveal_container = st.container()
    with reveal_container:
        if st.session_state.get("picked_movie"):
            _show_picked_movie(st.session_state["picked_movie"])

    if pick_requested:
        _run_reveal(filtered, carousel_slot)
        st.rerun()

    if st.session_state.get("watching_movie"):
        _watch_form(st.session_state["watching_movie"])
