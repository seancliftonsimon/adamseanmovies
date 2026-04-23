import inspect
import random
import time
from html import escape

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



def _run_reveal(filtered):
    placeholder = st.empty()
    for i in range(12):
        movie = random.choice(filtered)
        img = poster_url(movie["poster_path"]) if movie["poster_path"] else POSTER_PLACEHOLDER
        with placeholder.container():
            st.markdown('<div class="pick-reveal-anchor"></div>', unsafe_allow_html=True)
            st.markdown('<div class="pick-reveal-copy">Finding your perfect tape...</div>', unsafe_allow_html=True)
            cols = st.columns([1, 2, 1])
            with cols[1]:
                st.image(img, width=160)
                st.markdown(f"#### {movie['title']}")
        time.sleep(0.08 + (i * 0.03))

    st.session_state["picked_movie"] = random.choice(filtered)
    placeholder.empty()


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
    st.markdown('<div class="pick-filter-panel-anchor"></div>', unsafe_allow_html=True)
    st.markdown('<div class="workflow-stack">', unsafe_allow_html=True)
    st.markdown('<div class="workflow-block">', unsafe_allow_html=True)

    st.markdown(workflow_label_html("1. Whose picks?"), unsafe_allow_html=True)
    list_filter = st.pills(
        "Whose Picks?",
        LIST_OPTIONS,
        default=st.session_state.get("pick_list_filter", "All"),
        key="pick_list_filter",
        label_visibility="collapsed",
    )

    filtered = list(all_movies)
    selected_list = LIST_MAP.get(list_filter)
    if selected_list:
        filtered = [m for m in filtered if m["list_type"] == selected_list]

    st.markdown('</div><div class="workflow-block">', unsafe_allow_html=True)
    st.markdown(workflow_label_html("2. Genres"), unsafe_allow_html=True)
    available_genres = database.get_all_genres()
    selected_genres = st.pills(
        "Genres",
        available_genres,
        selection_mode="multi",
        key="pick_genre_filter",
        label_visibility="collapsed",
    ) if available_genres else []
    if selected_genres:
        selected_set = set(selected_genres)
        filtered = [m for m in filtered if selected_set.intersection(m["genres_list"])]

    st.markdown('</div><div class="workflow-block">', unsafe_allow_html=True)
    st.markdown(workflow_label_html("3. Runtime"), unsafe_allow_html=True)
    runtime_choice, custom_runtime = _runtime_selector()
    if runtime_choice != "Any Length":
        max_runtime = custom_runtime if runtime_choice == "Custom" else RUNTIME_LIMITS[runtime_choice]
        filtered = [m for m in filtered if not m.get("runtime") or int(m["runtime"]) <= max_runtime]

    active_filters = []
    if list_filter != "All":
        active_filters.append(list_filter)
    if selected_genres:
        active_filters.extend(selected_genres)
    if runtime_choice != "Any Length":
        active_filters.append(f"Under {_runtime_label(custom_runtime)}" if runtime_choice == "Custom" else runtime_choice)
    _active_filter_row(active_filters)

    st.markdown('</div></div>', unsafe_allow_html=True)

    return filtered, bool(active_filters)


def _render_results_card(filtered, has_optional_filters):
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

    sample = filtered[:3]
    if sample:
        thumbs_html = []
        for movie in sample:
            img = poster_url(movie["poster_path"], "w154") if movie["poster_path"] else POSTER_PLACEHOLDER
            thumbs_html.append(f'<img src="{img}" alt="{escape(movie["title"])}" />')
        st.markdown(f'<div class="pick-results-thumbs">{"".join(thumbs_html)}</div>', unsafe_allow_html=True)

    if st.button("Pick for Us", key="pick_btn", type="primary", width="stretch", disabled=not has_results):
        _run_reveal(filtered)
        st.rerun()

    if (not has_results) and has_optional_filters:
        if st.button("Clear All", key="clear_all_results", width="stretch"):
            st.session_state["pick_list_filter"] = "All"
            st.session_state["pick_genre_filter"] = []
            st.session_state["pick_runtime_choice"] = "Any Length"
            st.session_state["pick_custom_runtime"] = 150
            st.rerun()


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

    left_col, right_col = st.columns([1.65, 1], gap="large")
    with left_col:
        filtered, has_optional_filters = _render_filters(all_movies)

    with right_col:
        _render_results_card(filtered, has_optional_filters)

    if st.session_state.get("picked_movie"):
        _show_picked_movie(st.session_state["picked_movie"])
    elif st.session_state.get("watching_movie"):
        _watch_form(st.session_state["watching_movie"])
