import streamlit as st

st.set_page_config(
    page_title="Adam & Sean Movie Night",
    page_icon="\U0001F37F",
    layout="centered",
    initial_sidebar_state="auto",
)

from pages import add_movie, pick_for_us, our_lists, watch_log


def add_movie_page():
    add_movie.render()


def pick_for_us_page():
    pick_for_us.render()


def our_lists_page():
    our_lists.render()


def watch_log_page():
    watch_log.render()


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
            add_movie_page,
            title="Add a Movie",
            icon="\U0001F3AC",
            url_path="add-movie",
            default=True,
        ),
        st.Page(
            pick_for_us_page,
            title="Pick for Us",
            icon="\U0001F3B0",
            url_path="pick-for-us",
        ),
        st.Page(
            our_lists_page,
            title="Our Lists",
            icon="\U0001F4CB",
            url_path="our-lists",
        ),
        st.Page(
            watch_log_page,
            title="Watch Log",
            icon="\U0001F4D6",
            url_path="watch-log",
        ),
    ])
    page.run()


if __name__ == "__main__":
    main()
