import streamlit as st
from styles import (inject_css, genre_pills_html, runtime_display,
                    stars_html, POSTER_PLACEHOLDER)
from tmdb_api import poster_url as make_poster_url
from database import get_watched_movies, get_watch_stats


def render():
    inject_css()
    st.title("\U0001F4D6 Watch Log")
    st.caption("Every movie you've watched together, rated and remembered.")

    stats = get_watch_stats()
    watched = get_watched_movies()

    if stats["total"] == 0:
        st.info("You haven't watched any movies together yet! "
                "Pick one from your lists and start your journey.")
        return

    _render_stats(stats)
    st.divider()
    _render_log(watched)


def _render_stats(stats):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Movies Watched", stats["total"])
    with c2:
        st.metric("Total Hours", stats["total_hours"])
    with c3:
        st.metric("Adam's Avg Rating", f"{stats['avg_adam']}/10" if stats["avg_adam"] else "N/A")
    with c4:
        st.metric("Sean's Avg Rating", f"{stats['avg_sean']}/10" if stats["avg_sean"] else "N/A")

    c5, c6, c7 = st.columns(3)
    with c5:
        st.metric("Top Genre", stats["top_genre"])
    with c6:
        st.metric("Adam's Picks Watched", stats["adam_suggested_watched"])
    with c7:
        st.metric("Sean's Picks Watched", stats["sean_suggested_watched"])

    if stats["adam_suggested_watched"] > 0 or stats["sean_suggested_watched"] > 0:
        if stats["adam_suggested_watched"] > stats["sean_suggested_watched"]:
            st.success("\U0001F3C6 Adam is winning the 'great suggestions' race!")
        elif stats["sean_suggested_watched"] > stats["adam_suggested_watched"]:
            st.success("\U0001F3C6 Sean is winning the 'great suggestions' race!")
        else:
            st.success("\U0001F91D It's a tie! You both have great taste.")


def _render_log(watched):
    for movie in watched:
        img = make_poster_url(movie["poster_path"], "w185") if movie["poster_path"] else POSTER_PLACEHOLDER
        list_labels = {
            "adam_pick": "Adam's Pick",
            "sean_pick": "Sean's Pick",
            "mutual": "Mutual Discovery",
        }

        header = f"**{movie['title']}** ({movie['year'] or '?'})"
        if movie["watched_date"]:
            header += f"  \u2014  Watched {movie['watched_date']}"

        with st.expander(header):
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(img, use_container_width=True)
            with cols[1]:
                if movie["director"]:
                    st.markdown(f"**Director:** {movie['director']}")
                if movie["genres_list"]:
                    st.markdown(genre_pills_html(movie["genres_list"]), unsafe_allow_html=True)
                if movie["runtime"]:
                    st.markdown(f"**Runtime:** {runtime_display(movie['runtime'])}")

                st.caption(f"Suggested as: {list_labels.get(movie['list_type'], '?')}")

                r_cols = st.columns(2)
                with r_cols[0]:
                    st.markdown(f"**Adam's rating:** {stars_html(movie['adam_rating'])}",
                                unsafe_allow_html=True)
                with r_cols[1]:
                    st.markdown(f"**Sean's rating:** {stars_html(movie['sean_rating'])}",
                                unsafe_allow_html=True)

                if movie.get("notes"):
                    st.markdown(f"\U0001F4DD *{movie['notes']}*")
