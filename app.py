import streamlit as st

st.set_page_config(
    page_title="Adam & Sean Movie Night",
    page_icon="\U0001F37F",
    layout="centered",
    initial_sidebar_state="auto",
)

from pages import add_movie, pick_for_us, our_lists, watch_log


def main():
    with st.sidebar:
        st.markdown("## \U0001F37F Movie Night")
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
        st.Page(
            add_movie.render,
            title="Add a Movie",
            icon="\U0001F3AC",
            url_path="add-movie",
            default=True,
        ),
        st.Page(
            pick_for_us.render,
            title="Pick for Us",
            icon="\U0001F3B0",
            url_path="pick-for-us",
        ),
        st.Page(
            our_lists.render,
            title="Our Lists",
            icon="\U0001F4CB",
            url_path="our-lists",
        ),
        st.Page(
            watch_log.render,
            title="Watch Log",
            icon="\U0001F4D6",
            url_path="watch-log",
        ),
    ])
    page.run()


if __name__ == "__main__":
    main()
