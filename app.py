import streamlit as st

st.set_page_config(
    page_title="Adam & Sean Movie Night",
    page_icon="\U0001F4FC",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from pages import add_movie, pick_for_us, our_lists, watch_log
from styles import inject_css
from database import get_db_status


def main():
    inject_css()

    db_status = get_db_status()
    if db_status.get("fallback"):
        st.warning(
            "**Database connection failed** — running on local SQLite. "
            "Data won't persist across app restarts or be shared between users. "
            "Check the DATABASE_URL in your Streamlit secrets and review the "
            "app logs for details.",
            icon="\u26a0\ufe0f",
        )

    add_pg = st.Page(add_movie.render, title="Add a Movie", icon="\U0001F3AC",
                     default=True, url_path="add-movie")
    pick_pg = st.Page(pick_for_us.render, title="Pick for Us", icon="\U0001F3B0",
                      url_path="pick-for-us")
    lists_pg = st.Page(our_lists.render, title="Our Lists", icon="\U0001F4CB",
                       url_path="our-lists")
    log_pg = st.Page(watch_log.render, title="Watch Log", icon="\U0001F4FC",
                     url_path="watch-log")

    all_pages = [add_pg, pick_pg, lists_pg, log_pg]
    page = st.navigation(all_pages, position="hidden")

    nav_cols = st.columns(len(all_pages))
    nav_labels = ["Add", "Pick", "Lists", "Log"]
    for col, pg, label in zip(nav_cols, all_pages, nav_labels):
        with col:
            st.page_link(pg, label=label, icon=pg.icon,
                         use_container_width=True)

    page.run()


if __name__ == "__main__":
    main()
