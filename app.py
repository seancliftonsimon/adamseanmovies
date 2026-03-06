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

NAV_ITEMS = [
    ("\U0001F3AC Add", add_movie.render),
    ("\U0001F3B0 Pick", pick_for_us.render),
    ("\U0001F4CB Lists", our_lists.render),
    ("\U0001F4FC Log", watch_log.render),
]


def _render_top_menu():
    labels = [label for label, _ in NAV_ITEMS]
    selected = st.pills(
        "Menu",
        labels,
        default=labels[0],
        key="top_nav_menu",
    )
    return selected or labels[0]


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

    selected_menu = _render_top_menu()
    render_map = dict(NAV_ITEMS)
    render_map[selected_menu]()


if __name__ == "__main__":
    main()
