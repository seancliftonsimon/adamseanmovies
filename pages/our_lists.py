import streamlit as st
from html import escape
from styles import (inject_css, genre_pills_html, runtime_display,
                    section_header, vhs_tape_html, shelf_row_html, shelf_bar_html,
                    POSTER_PLACEHOLDER, SHELF_COLS)
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

    c1, c2 = st.columns(2)
    with c1:
        if st.button("\u2705 We watched this!", key=f"dw_{prefix}_{movie['id']}",
                     type="primary", width="stretch"):
            st.session_state[f"rate_{prefix}"] = movie["id"]
    with c2:
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
                st.rerun()

    st.markdown('<div class="vhs-drawer-end"></div>', unsafe_allow_html=True)


def _render_shelf(movies, prefix):
    if not movies:
        st.info("This shelf is empty! Head over to **Add a Movie** to stock it.")
        return

    sort_option = st.selectbox(
        "Sort by",
        ["Recently Added", "Title A\u2013Z", "Shortest First", "Longest First"],
        key=f"sort_{prefix}",
    )
    movies = _sort_movies(movies, sort_option)

    if f"sel_{prefix}" not in st.session_state:
        st.session_state[f"sel_{prefix}"] = None

    shelf_cols = 2 if _is_mobile_client() else SHELF_COLS
    rows = [movies[i:i + shelf_cols] for i in range(0, len(movies), shelf_cols)]

    for row_idx, row_movies in enumerate(rows):
        with st.container(key=f"shelf-row-{prefix}-{row_idx}"):
            if shelf_cols == 2:
                # Mobile: use controlled HTML layout so two posters fit side-by-side
                st.markdown(
                    shelf_row_html(row_movies, make_poster_url, POSTER_PLACEHOLDER),
                    unsafe_allow_html=True,
                )
                btn_cols = st.columns(2, gap="small")
                for col_idx, movie in enumerate(row_movies):
                    with btn_cols[col_idx]:
                        is_sel = st.session_state[f"sel_{prefix}"] == movie["id"]
                        if st.button(
                            "\u25B2" if is_sel else "\u25BC",
                            key=f"vhs_{prefix}_{movie['id']}",
                            width="stretch",
                        ):
                            if is_sel:
                                st.session_state[f"sel_{prefix}"] = None
                            else:
                                st.session_state[f"sel_{prefix}"] = movie["id"]
                                st.session_state.pop(f"rate_{prefix}", None)
                                st.session_state.pop(f"confirm_rm_{prefix}", None)
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
                        is_sel = st.session_state[f"sel_{prefix}"] == movie["id"]
                        if st.button(
                            "\u25B2" if is_sel else "\u25BC",
                            key=f"vhs_{prefix}_{movie['id']}",
                            width="stretch",
                        ):
                            if is_sel:
                                st.session_state[f"sel_{prefix}"] = None
                            else:
                                st.session_state[f"sel_{prefix}"] = movie["id"]
                                st.session_state.pop(f"rate_{prefix}", None)
                                st.session_state.pop(f"confirm_rm_{prefix}", None)
                            st.rerun()

            st.markdown(shelf_bar_html(), unsafe_allow_html=True)

        sel_id = st.session_state.get(f"sel_{prefix}")
        sel_movie = next((m for m in row_movies if m["id"] == sel_id), None)
        if sel_movie:
            _render_drawer(sel_movie, prefix)


def render():
    inject_css()
    section_header("\U0001F4FC Our Lists")
    st.caption("Browse the shelves and pick something to watch.")

    adam_movies = get_unwatched_movies("adam_pick")
    sean_movies = get_unwatched_movies("sean_pick")
    mutual_movies = get_unwatched_movies("mutual")

    tab_adam, tab_sean, tab_mutual = st.tabs([
        f"Adam's Picks ({len(adam_movies)})",
        f"Sean's Picks ({len(sean_movies)})",
        f"Mutual ({len(mutual_movies)})",
    ])

    with tab_adam:
        _render_shelf(adam_movies, "adam")
    with tab_sean:
        _render_shelf(sean_movies, "sean")
    with tab_mutual:
        _render_shelf(mutual_movies, "mutual")
