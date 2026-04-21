import streamlit as st
from html import escape
from styles import (inject_css, genre_pills_html, runtime_display,
                    stars_html, section_header, vhs_tape_html,
                    shelf_bar_html, stat_cards_row_html,
                    POSTER_PLACEHOLDER, SHELF_COLS)
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
        {"label": "Top Genre", "value": top_genre,
         "sub": "most watched genre"},
        {"label": "Adam's Picks Done",
         "value": stats["adam_suggested_watched"]},
        {"label": "Sean's Picks Done",
         "value": stats["sean_suggested_watched"]},
    ]
    st.markdown(stat_cards_row_html(row2), unsafe_allow_html=True)

    if stats["adam_suggested_watched"] > 0 or stats["sean_suggested_watched"] > 0:
        if stats["adam_suggested_watched"] > stats["sean_suggested_watched"]:
            st.success("\U0001F3C6 Adam is winning the 'great suggestions' race!")
        elif stats["sean_suggested_watched"] > stats["adam_suggested_watched"]:
            st.success("\U0001F3C6 Sean is winning the 'great suggestions' race!")
        else:
            st.success("\U0001F91D It's a tie! You both have great taste.")


def _render_watched_drawer(movie):
    list_labels = {
        "adam_pick": "Adam's Pick",
        "sean_pick": "Sean's Pick",
        "mutual": "Mutual Discovery",
    }

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
        st.caption(
            f"Suggested as: {list_labels.get(movie['list_type'], '?')}"
        )

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
    if "sel_watched" not in st.session_state:
        st.session_state["sel_watched"] = None

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
                is_sel = st.session_state["sel_watched"] == movie["id"]
                if st.button(
                    "\u25B2" if is_sel else "\u25BC",
                    key=f"wvhs_{movie['id']}",
                    width="stretch",
                ):
                    st.session_state["sel_watched"] = (
                        None if is_sel else movie["id"]
                    )
                    st.rerun()

        st.markdown(shelf_bar_html(), unsafe_allow_html=True)

        sel_id = st.session_state.get("sel_watched")
        sel_movie = next((m for m in row_movies if m["id"] == sel_id), None)
        if sel_movie:
            _render_watched_drawer(sel_movie)


def render():
    inject_css()
    section_header("\U0001F4FC Watched Together")
    st.caption("Every movie you've watched together, rated and remembered.")

    stats = get_watch_stats()
    watched = get_watched_movies()

    if stats["total"] == 0:
        st.info("You haven't watched any movies together yet! "
                "Pick one from your lists and start your journey.")
        return

    _render_stats(stats)
    st.divider()
    _render_shelf(watched)
