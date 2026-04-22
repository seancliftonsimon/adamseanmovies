import streamlit as st
from html import escape
from styles import (inject_css, genre_pills_html, runtime_display,
                    vhs_tape_html, shelf_row_html, shelf_bar_html,
                    POSTER_PLACEHOLDER, SHELF_COLS, page_intro_html,
                    panel_start_html, panel_end_html, workflow_label_html,
                    empty_state_html, result_summary_html)
from database import get_unwatched_movies, remove_movie, mark_watched
from tmdb_api import poster_url as make_poster_url


def _is_mobile_client():
    """Best-effort mobile detection with compact fallback."""
    context = getattr(st, "context", None)
    if context is None:
        # Older Streamlit versions lack st.context; prefer compact layout.
        return True

    headers = getattr(context, "headers", None)
    if not headers:
        return True

    mobile_hint = (headers.get("sec-ch-ua-mobile") or "").strip()
    if mobile_hint == "?1":
        return True
    if mobile_hint == "?0":
        return False

    # Some deployments pass UA through non-standard header names.
    ua_values = []
    for key in headers.keys():
        if "user-agent" in key.lower():
            value = headers.get(key) or ""
            if value:
                ua_values.append(str(value).lower())

    combined_ua = " ".join(ua_values)
    if any(t in combined_ua for t in ("iphone", "android", "mobile", "ipad")):
        return True
    if any(t in combined_ua for t in ("windows", "macintosh", "x11", "linux x86_64")):
        return False

    # Unknown agent: favor compact layout so mobile portrait remains usable.
    return True


def _sort_movies(movies, sort_option):
    if sort_option == "Title A\u2013Z":
        return sorted(movies, key=lambda m: (m["title"] or "").lower())
    elif sort_option == "Shortest First":
        return sorted(movies, key=lambda m: m["runtime"] or 9999)
    elif sort_option == "Longest First":
        return sorted(movies, key=lambda m: m["runtime"] or 0, reverse=True)
    return movies


def _rating_form(movie, prefix):
    st.markdown(f"### Rate **{movie['title']}**")
    c1, c2 = st.columns(2)
    with c1:
        adam_r = st.slider("Adam's rating", 1, 10, 7,
                           key=f"ar_{prefix}_{movie['id']}")
    with c2:
        sean_r = st.slider("Sean's rating", 1, 10, 7,
                           key=f"sr_{prefix}_{movie['id']}")
    notes = st.text_area("Notes (optional)", key=f"nt_{prefix}_{movie['id']}",
                         placeholder="e.g. We both loved it!")
    watch_date = st.date_input("Date watched", key=f"wd_{prefix}_{movie['id']}")
    if st.button("Save to Watch Log", key=f"sv_{prefix}_{movie['id']}",
                 type="primary", width="stretch"):
        mark_watched(movie["id"], adam_r, sean_r, notes, watch_date)
        st.session_state[f"sel_{prefix}"] = None
        st.session_state.pop(f"rate_{prefix}", None)
        st.toast(f"**{movie['title']}** added to your Watch Log!", icon="\U0001F37F")
        st.balloons()
        st.rerun()


def _render_drawer(movie, prefix):
    st.markdown(
        f'<div class="vhs-drawer-header">'
        f'\U0001F4FC {escape(movie["title"])} ({movie["year"] or "?"})'
        f'</div>',
        unsafe_allow_html=True,
    )

    if movie["director"]:
        st.markdown(f"**Director:** {movie['director']}")
    if movie["genres_list"]:
        st.markdown(genre_pills_html(movie["genres_list"]),
                    unsafe_allow_html=True)
    if movie["runtime"]:
        st.markdown(f"**Runtime:** {runtime_display(movie['runtime'])}")
    if movie["overview"]:
        st.caption(movie["overview"])

    if st.button("\u2705 We watched this!", key=f"dw_{prefix}_{movie['id']}",
                 type="primary", width="stretch"):
        st.session_state[f"rate_{prefix}"] = movie["id"]
    if st.button("\U0001F5D1\uFE0F Remove", key=f"drm_{prefix}_{movie['id']}",
                 width="stretch"):
        st.session_state[f"confirm_rm_{prefix}"] = movie["id"]

    if st.session_state.get(f"rate_{prefix}") == movie["id"]:
        _rating_form(movie, prefix)

    if st.session_state.get(f"confirm_rm_{prefix}") == movie["id"]:
        st.warning(f"Remove **{movie['title']}** from the list?")
        rc1, rc2 = st.columns(2)
        with rc1:
            if st.button("Yes, remove", key=f"yrm_{prefix}_{movie['id']}",
                         width="stretch"):
                remove_movie(movie["id"])
                st.session_state[f"sel_{prefix}"] = None
                st.session_state.pop(f"confirm_rm_{prefix}", None)
                st.toast(f"Removed {movie['title']}", icon="\U0001F5D1")
                st.rerun()
        with rc2:
            if st.button("Cancel", key=f"nrm_{prefix}_{movie['id']}",
                         width="stretch"):
                st.session_state.pop(f"confirm_rm_{prefix}", None)

    st.markdown('<div class="vhs-drawer-end"></div>', unsafe_allow_html=True)


def _render_shelf(movies, prefix):
    if not movies:
        st.markdown(
            empty_state_html(
                "This shelf is empty",
                None,
            ),
            unsafe_allow_html=True,
        )
        return

    st.markdown(panel_start_html(tight=True), unsafe_allow_html=True)
    st.markdown(workflow_label_html("Sort shelf"), unsafe_allow_html=True)
    sort_option = st.selectbox(
        "Sort by",
        ["Recently Added", "Title A\u2013Z", "Shortest First", "Longest First"],
        key=f"sort_{prefix}",
        label_visibility="collapsed",
    )
    st.markdown(panel_end_html(), unsafe_allow_html=True)
    movies = _sort_movies(movies, sort_option)

    shelf_cols = 2 if _is_mobile_client() else SHELF_COLS
    rows = [movies[i:i + shelf_cols] for i in range(0, len(movies), shelf_cols)]

    selected_movie_id = st.session_state.get(f"sel_{prefix}")

    for row_idx, row_movies in enumerate(rows):
        with st.container(key=f"shelf-row-{prefix}-{row_idx}"):
            if shelf_cols == 2:
                # Mobile: use controlled HTML layout so two posters fit side-by-side
                st.markdown(
                    shelf_row_html(row_movies, make_poster_url, POSTER_PLACEHOLDER),
                    unsafe_allow_html=True,
                )
                btn_cols = st.columns(shelf_cols, gap="small")
                for col_idx, movie in enumerate(row_movies):
                    with btn_cols[col_idx]:
                        is_open = selected_movie_id == movie["id"]
                        label = "▾ Details" if is_open else "▸ Details"
                        if st.button(label, key=f"open_{prefix}_{movie['id']}", width="stretch"):
                            st.session_state[f"sel_{prefix}"] = None if is_open else movie["id"]
                            st.rerun()
            else:
                # Desktop: use st.columns for posters + buttons
                cols = st.columns(shelf_cols, gap="small")
                for col_idx, movie in enumerate(row_movies):
                    with cols[col_idx]:
                        poster_size = "w185"
                        img = (make_poster_url(movie["poster_path"], poster_size)
                               if movie["poster_path"] else POSTER_PLACEHOLDER)
                        st.markdown(
                            vhs_tape_html(img, movie["title"], movie.get("year")),
                            unsafe_allow_html=True,
                        )
                        is_open = selected_movie_id == movie["id"]
                        label = "▾ Details" if is_open else "▸ Details"
                        if st.button(label, key=f"open_{prefix}_{movie['id']}", width="stretch"):
                            st.session_state[f"sel_{prefix}"] = None if is_open else movie["id"]
                            st.rerun()

            open_in_row = next((m for m in row_movies if m["id"] == st.session_state.get(f"sel_{prefix}")), None)
            if open_in_row:
                _render_drawer(open_in_row, prefix)

            st.markdown(shelf_bar_html(), unsafe_allow_html=True)


@st.fragment
def _render_active_shelf(list_type, prefix):
    movies = get_unwatched_movies(list_type)
    st.markdown(
        result_summary_html(f"{len(movies)} movie(s)", None),
        unsafe_allow_html=True,
    )
    _render_shelf(movies, prefix)


def render():
    inject_css()
    st.markdown(
        page_intro_html(
            "Our Lists",
            "Browse the Shelves",
        ),
        unsafe_allow_html=True,
    )

    st.markdown(panel_start_html(tight=True), unsafe_allow_html=True)
    st.markdown(workflow_label_html("Choose a shelf"), unsafe_allow_html=True)
    active_shelf = st.segmented_control(
        "Choose a shelf",
        ["Adam's Picks", "Sean's Picks", "Mutual"],
        default="Adam's Picks",
        key="our_lists_active_shelf",
        label_visibility="collapsed",
    )
    st.markdown(panel_end_html(), unsafe_allow_html=True)
    shelf_map = {
        "Adam's Picks": ("adam_pick", "adam"),
        "Sean's Picks": ("sean_pick", "sean"),
        "Mutual": ("mutual", "mutual"),
    }
    list_type, prefix = shelf_map[active_shelf]
    _render_active_shelf(list_type, prefix)
