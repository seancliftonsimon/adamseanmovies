import streamlit as st

st.set_page_config(
    page_title="Adam & Sean Movie Night",
    page_icon="\U0001F4FC",
    layout="centered",
    initial_sidebar_state="auto",
)

from pages import add_movie, pick_for_us, our_lists, watch_log
from styles import inject_css


def main():
    inject_css()

    with st.sidebar:
        st.markdown(
            '<div style="text-align:center; padding: 0.5rem 0 0.25rem;">'
            '<span style="font-size:1.6rem;">\U0001F4FC</span>'
            '<div style="font-size:1.1rem; font-weight:800; color:#FFD700; '
            'letter-spacing:0.06em; margin-top:0.15rem; '
            'text-transform:uppercase;">Movie Night</div>'
            '<div style="font-size:0.65rem; color:#7aafd4; '
            'text-transform:uppercase; letter-spacing:0.12em; '
            'font-weight:600;">Adam &amp; Sean</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown("---")

        if "current_user" not in st.session_state:
            st.session_state.current_user = "Adam"

        user = st.radio(
            "Who's adding?",
            ["Adam", "Sean"],
            index=0 if st.session_state.current_user == "Adam" else 1,
            key="user_select",
            horizontal=True,
        )
        st.session_state.current_user = user
        st.caption(f"Logged in as **{user}**")
        st.markdown("---")

    page = st.navigation([
        st.Page(add_movie.render, title="Add a Movie", icon="\U0001F3AC",
                default=True, url_path="add-movie"),
        st.Page(pick_for_us.render, title="Pick for Us", icon="\U0001F3B0",
                url_path="pick-for-us"),
        st.Page(our_lists.render, title="Our Lists", icon="\U0001F4CB",
                url_path="our-lists"),
        st.Page(watch_log.render, title="Watch Log", icon="\U0001F4FC",
                url_path="watch-log"),
    ])
    page.run()


if __name__ == "__main__":
    main()
