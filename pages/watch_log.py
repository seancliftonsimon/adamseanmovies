import streamlit as st
from html import escape
from styles import (inject_css, genre_pills_html, runtime_display,
                    stars_html, vhs_tape_html,
                    shelf_bar_html, stat_cards_row_html,
                    POSTER_PLACEHOLDER, SHELF_COLS, page_intro_html,
                    panel_start_html, panel_end_html, workflow_label_html,
                    empty_state_html)
from tmdb_api import poster_url as make_poster_url
from database import get_watched_movies, get_watch_stats


def _render_stats(stats):
    row1 = [
        {"label": "Movies Watched", "value": stats["total"], "yellow": True},
        {"label": "Total Hours", "value": f"{stats['total_hours']}h"},
        {"label": "Adam's Avg",
         "value": f"{stats['avg_adam']}/10" if stats["avg_adam"] else "—"},
        {"label": "Sean's Avg",
         "value": f"{stats['avg_sean']}/10" if stats["avg_sean"] else "—"},
    ]
    st.markdown(stat_cards_row_html(row1), unsafe_allow_html=True)

    top_genre = stats.get("top_genre") or "—"
    row2 = [
        {"label": "Top Genre", "value": top_genre},
        {"label": "Adam's Picks Done",
         "value": stats["adam_suggested_watched"]},
        {"label": "Sean's Picks Done",
         "value": stats["sean_suggested_watched"]},
    ]
    st.markdown(stat_cards_row_html(row2), unsafe_allow_html=True)


def _render_watched_drawer(movie):
    st.markdown(
        f'<div class="vhs-drawer-header">'
        f'\U0001F4FC {escape(movie["title"])} ({movie["year"] or "?"})'
        f'</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns([1, 2])
    with cols[0]:
        img = (make_poster_url(movie["poster_path"])
               if movie["poster_path"] else POSTER_PLACEHOLDER)
        st.image(img, width="stretch")
    with cols[1]:
        if movie["director"]:
            st.markdown(f"**Director:** {movie['director']}")
        if movie["genres_list"]:
            st.markdown(genre_pills_html(movie["genres_list"]),
                        unsafe_allow_html=True)
        if movie["runtime"]:
            st.markdown(f"**Runtime:** {runtime_display(movie['runtime'])}")

    r_cols = st.columns(2)
    with r_cols[0]:
        st.markdown(f"**Adam's rating:** {stars_html(movie['adam_rating'])}",
                    unsafe_allow_html=True)
    with r_cols[1]:
        st.markdown(f"**Sean's rating:** {stars_html(movie['sean_rating'])}",
                    unsafe_allow_html=True)

    if movie.get("watched_date"):
        st.caption(f"Watched on: {movie['watched_date']}")
    if movie.get("notes"):
        st.markdown(f"\U0001F4DD *{movie['notes']}*")

    st.markdown('<div class="vhs-drawer-end"></div>', unsafe_allow_html=True)


def _render_shelf(watched):
    rows = [watched[i:i + SHELF_COLS]
            for i in range(0, len(watched), SHELF_COLS)]

    for row_movies in rows:
        cols = st.columns(SHELF_COLS)
        for col_idx, movie in enumerate(row_movies):
            with cols[col_idx]:
                img = (make_poster_url(movie["poster_path"], "w185")
                       if movie["poster_path"] else POSTER_PLACEHOLDER)
                st.markdown(
                    vhs_tape_html(img, movie["title"], movie.get("year")),
                    unsafe_allow_html=True,
                )
                with st.expander("Details", expanded=False):
                    _render_watched_drawer(movie)

        st.markdown(shelf_bar_html(), unsafe_allow_html=True)


def render():
    inject_css()
    st.markdown(
        page_intro_html(
            "Watch Log",
            "Watched Together",
        ),
        unsafe_allow_html=True,
    )

    st.markdown(panel_start_html("View Mode", tight=True), unsafe_allow_html=True)
    st.markdown(workflow_label_html("Choose a view"), unsafe_allow_html=True)
    view = st.segmented_control(
        "View",
        ["Overview", "Watched Shelf"],
        default="Overview",
        key="watch_log_view",
        label_visibility="collapsed",
    )
    st.markdown(panel_end_html(), unsafe_allow_html=True)

    stats = get_watch_stats() if view == "Overview" else None
    watched = get_watched_movies() if view == "Watched Shelf" else None

    total = stats["total"] if stats else len(watched or [])
    if total == 0:
        st.markdown(
            empty_state_html(
                "No watched movies yet",
                None,
            ),
            unsafe_allow_html=True,
        )
        return

    if view == "Overview":
        _render_stats(stats)
    else:
        _render_shelf(watched)
