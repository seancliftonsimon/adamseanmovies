import streamlit as st

POSTER_PLACEHOLDER = "https://via.placeholder.com/185x278/1a1a2e/e8b004?text=No+Poster"


def inject_css():
    st.markdown("""
    <style>
    /* ---- Global polish ---- */
    .block-container { max-width: 900px; padding-top: 1.5rem; }

    /* ---- Movie card ---- */
    .movie-card {
        background: #1A1A2E;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border: 1px solid #2a2a3e;
        transition: border-color 0.2s;
    }
    .movie-card:hover { border-color: #E8B004; }

    .movie-card img {
        border-radius: 8px;
        width: 100%;
        max-width: 185px;
    }

    /* ---- Genre pills ---- */
    .genre-pill {
        display: inline-block;
        background: #2a2a3e;
        color: #E8B004;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        margin: 2px 3px 2px 0;
        font-weight: 500;
    }

    /* ---- Star ratings ---- */
    .stars { color: #E8B004; font-size: 1.1rem; letter-spacing: 1px; }

    /* ---- Picker animation placeholder ---- */
    .picker-card {
        background: #1A1A2E;
        border: 2px solid #E8B004;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
    }
    .picker-card img {
        border-radius: 12px;
        max-height: 400px;
        margin-bottom: 0.75rem;
    }

    /* ---- Big pick button ---- */
    div.stButton > button[kind="primary"] {
        font-size: 1.3rem;
        padding: 0.8rem 2rem;
        border-radius: 12px;
    }

    /* ---- Stat cards ---- */
    [data-testid="stMetric"] {
        background: #1A1A2E;
        border: 1px solid #2a2a3e;
        border-radius: 10px;
        padding: 0.8rem;
    }

    /* ---- Mobile friendly ---- */
    @media (max-width: 640px) {
        .block-container { padding-top: 0.5rem; padding-left: 0.5rem; padding-right: 0.5rem; }
        div.stButton > button { width: 100%; }
    }

    /* ---- Hide Streamlit top bar clutter ---- */
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }

    /* ---- Tabs styling ---- */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 20px;
    }
    </style>
    """, unsafe_allow_html=True)


def genre_pills_html(genres):
    if not genres:
        return ""
    pills = "".join(f'<span class="genre-pill">{g}</span>' for g in genres)
    return pills


def stars_html(rating, max_stars=10):
    if not rating:
        return '<span class="stars">Not rated</span>'
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = max_stars - full - half
    s = "★" * full + ("½" if half else "") + "☆" * empty
    return f'<span class="stars">{s} {rating}/10</span>'


def runtime_display(minutes):
    if not minutes:
        return "Unknown"
    h, m = divmod(minutes, 60)
    if h:
        return f"{h}h {m}m"
    return f"{m}m"
