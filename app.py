import streamlit as st

st.set_page_config(
    page_title="Adam & Sean Movie Night",
    page_icon="\U0001F37F",
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
            '<span style="font-size:1.6rem;">&#127871;</span>'
            '<div style="font-size:1.1rem; font-weight:700; color:#FAFAFA; '
            'letter-spacing:0.02em; margin-top:0.15rem;">Movie Night</div>'
            '<div style="font-size:0.7rem; color:#C62828; text-transform:uppercase; '
            'letter-spacing:0.12em; font-weight:600;">Adam &amp; Sean</div>'
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
        st.Page(add_movie.render, title="Add a Movie", icon="\U0001F3AC", default=True),
        st.Page(pick_for_us.render, title="Pick for Us", icon="\U0001F3B0"),
        st.Page(our_lists.render, title="Our Lists", icon="\U0001F4CB"),
        st.Page(watch_log.render, title="Watch Log", icon="\U0001F4D6"),
    ])
    page.run()


if __name__ == "__main__":
    main()
