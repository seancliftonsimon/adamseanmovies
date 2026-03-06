import streamlit as st
from html import escape

POSTER_PLACEHOLDER = "https://via.placeholder.com/185x278/001029/FFD700?text=No+Tape"

SHELF_COLS = 4


def inject_css():
    st.markdown("""
    <style>
    /* ===== GLOBAL ===== */
    .block-container {
        max-width: 540px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {
        background-color: #001029;
    }

    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3 { font-weight: 800 !important; }
    h1 { font-size: 1.4rem !important; color: #FFD700 !important; }
    h2 { font-size: 1.2rem !important; color: #FFD700 !important; }
    h3 { font-size: 1.05rem !important; }

    /* ===== HIDE CHROME ===== */
    #MainMenu, header, footer { visibility: hidden; }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001940 0%, #001029 100%);
        border-right: 2px solid #004B93;
    }

    /* ===== STORE SIGN (section headers) ===== */
    .store-sign {
        background: linear-gradient(135deg, #004B93 0%, #0060B8 100%);
        color: #FFD700;
        padding: 0.7rem 1rem;
        border-radius: 6px;
        font-size: 1.1rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        text-align: center;
        margin-bottom: 0.75rem;
        border: 2px solid #FFD700;
        box-shadow: 0 2px 12px rgba(0, 75, 147, 0.5);
    }

    /* ===== VHS TAPE ===== */
    .vhs-tape {
        background: #0a0a0a;
        border: 2px solid #1a1a1a;
        border-radius: 3px;
        padding: 4px 4px 0 4px;
        box-shadow:
            2px 2px 8px rgba(0,0,0,0.6),
            inset 0 0 0 1px rgba(255,255,255,0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        margin-bottom: 2px;
    }
    .vhs-tape:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow:
            2px 5px 14px rgba(0,0,0,0.7),
            0 0 10px rgba(255,215,0,0.12);
    }
    .vhs-tape img {
        width: 100%;
        display: block;
        border-radius: 1px;
        aspect-ratio: 2/3;
        object-fit: cover;
    }
    .vhs-spine {
        background: linear-gradient(135deg, #FFD700, #FFC107);
        color: #002244;
        font-size: 0.52rem;
        font-weight: 800;
        padding: 3px 3px;
        text-align: center;
        margin-top: 3px;
        margin-bottom: 2px;
        border-radius: 1px;
        text-transform: uppercase;
        letter-spacing: 0.02em;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        line-height: 1.3;
    }

    /* ===== SHELF BAR ===== */
    .shelf-bar {
        height: 6px;
        background: linear-gradient(180deg, #004B93 0%, #003366 50%, #002244 100%);
        margin: 2px 0 8px;
        border-radius: 1px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }

    /* ===== DRAWER ===== */
    .vhs-drawer-header {
        background: linear-gradient(135deg, #002244, #003366);
        border-top: 3px solid #FFD700;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.25rem;
        font-weight: 700;
        color: #FFD700;
        font-size: 0.85rem;
        letter-spacing: 0.02em;
        border-radius: 4px 4px 0 0;
    }
    .vhs-drawer-end {
        height: 3px;
        background: linear-gradient(90deg, #FFD700, #FFC107, #FFD700);
        margin-top: 0.5rem;
        margin-bottom: 0.75rem;
        border-radius: 0 0 4px 4px;
    }

    /* ===== GENRE PILLS ===== */
    .genre-pill {
        display: inline-block;
        background: #002244;
        color: #FFD700;
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.68rem;
        margin: 2px 3px 2px 0;
        font-weight: 700;
        border: 1px solid #004B93;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    /* ===== STAR RATINGS ===== */
    .stars {
        color: #FFD700;
        font-size: 1rem;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* ===== BUTTONS ===== */
    div.stButton > button {
        background: #004B93;
        color: #FFD700;
        border: 1px solid #005BB5;
        border-radius: 4px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        font-size: 0.7rem;
        transition: all 0.15s;
    }
    div.stButton > button:hover {
        background: #005BB5;
        border-color: #FFD700;
        box-shadow: 0 0 8px rgba(255,215,0,0.15);
    }
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #FFD700, #FFC107);
        color: #002244;
        border: none;
        font-weight: 800;
        font-size: 0.8rem;
        padding: 0.55rem 1rem;
        border-radius: 6px;
        box-shadow: 0 2px 8px rgba(255, 215, 0, 0.25);
    }
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #FFC107, #FFB300);
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.35);
    }

    /* ===== STAT / METRIC CARDS ===== */
    [data-testid="stMetric"] {
        background: #001940;
        border: 1px solid #003366;
        border-radius: 8px;
        padding: 0.65rem;
        border-left: 3px solid #FFD700;
    }
    [data-testid="stMetric"] label {
        color: #7aafd4 !important;
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-weight: 800 !important;
    }

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #001940;
        border-radius: 8px;
        padding: 3px;
        border: 1px solid #003366;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 7px 14px;
        font-weight: 700;
        font-size: 0.78rem;
        color: #7aafd4;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #004B93, #0066CC) !important;
        color: #FFD700 !important;
        border-radius: 6px !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ===== EXPANDER ===== */
    [data-testid="stExpander"] {
        background: #001940;
        border: 1px solid #003366;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    [data-testid="stExpander"]:hover {
        border-color: #FFD700;
    }

    /* ===== TEXT INPUT ===== */
    [data-testid="stTextInput"] input {
        background: #001940;
        border: 1px solid #003366;
        border-radius: 6px;
        color: #FAFAFA;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #FFD700;
        box-shadow: 0 0 0 1px #FFD700;
    }

    /* ===== TEXT AREA ===== */
    [data-testid="stTextArea"] textarea {
        background: #001940;
        border: 1px solid #003366;
        border-radius: 6px;
        color: #FAFAFA;
    }
    [data-testid="stTextArea"] textarea:focus {
        border-color: #FFD700;
        box-shadow: 0 0 0 1px #FFD700;
    }

    /* ===== SELECT BOX ===== */
    [data-testid="stSelectbox"] > div > div {
        background: #001940;
        border: 1px solid #003366;
        border-radius: 6px;
    }

    /* ===== DIVIDER ===== */
    [data-testid="stHorizontalRule"] { border-color: #003366; }

    /* ===== IMAGE ===== */
    [data-testid="stImage"] img { border-radius: 4px; }

    /* ===== CAPTION ===== */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #7aafd4 !important;
    }

    /* ===== ALERTS ===== */
    [data-testid="stAlert"] { border-radius: 6px; }

    /* ===== NAVIGATION ===== */
    nav[data-testid="stSidebarNav"] a {
        border-radius: 6px;
        font-weight: 600;
        padding: 0.5rem 0.75rem;
    }
    nav[data-testid="stSidebarNav"] a:hover { background: #002244; }
    nav[data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(135deg, #004B93, #0066CC);
        color: #FFD700;
    }

    /* ===== PICKER CARD (pick_for_us) ===== */
    .picker-card {
        background: #001940;
        border: 2px solid #FFD700;
        border-radius: 10px;
        padding: 1.25rem;
        text-align: center;
    }

    /* ===== MOVIE CARD (search results in add_movie) ===== */
    .movie-card {
        background: #001940;
        border-radius: 8px;
        padding: 0.85rem;
        margin-bottom: 0.5rem;
        border: 1px solid #003366;
        transition: border-color 0.15s;
    }
    .movie-card:hover { border-color: #FFD700; }
    .movie-card img {
        border-radius: 4px;
        width: 100%;
        max-width: 185px;
    }

    /* ===== MOBILE-FIRST ===== */
    @media (max-width: 640px) {
        .block-container {
            max-width: 100%;
            padding-top: 2.8rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        div.stButton > button {
            width: 100%;
            padding: 0.5rem 0.5rem;
        }
        h1 { font-size: 1.2rem !important; }
        .store-sign { font-size: 0.9rem; padding: 0.5rem 0.75rem; }
        .vhs-spine { font-size: 0.45rem; padding: 2px; }
        .genre-pill { font-size: 0.58rem; padding: 2px 5px; }
        [data-testid="stMetric"] { padding: 0.4rem; }

        /* Keep movie shelf rows in a real two-up grid on mobile. */
        [class*="st-key-shelf_row_"] [data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            gap: 0.35rem !important;
        }
        [class*="st-key-shelf_row_"] [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            flex: 1 1 0 !important;
            width: 0 !important;
            min-width: 0 !important;
        }
    }

    @media (min-width: 641px) {
        .block-container { max-width: 740px; }
    }
    </style>
    """, unsafe_allow_html=True)


# ── HTML helpers ──────────────────────────────────────────────


def section_header(text):
    st.markdown(f'<div class="store-sign">{escape(text)}</div>',
                unsafe_allow_html=True)


def vhs_tape_html(img_url, title, year=None):
    label = title if len(title) <= 20 else title[:18] + "\u2026"
    if year:
        yr = f" ({year})"
        if len(label) + len(yr) <= 24:
            label += yr
    return (
        f'<div class="vhs-tape">'
        f'<img src="{img_url}" alt="{escape(title)}" />'
        f'<div class="vhs-spine">{escape(label)}</div>'
        f'</div>'
    )


def shelf_bar_html():
    return '<div class="shelf-bar"></div>'


def genre_pills_html(genres):
    if not genres:
        return ""
    return "".join(
        f'<span class="genre-pill">{escape(g)}</span>' for g in genres
    )


def stars_html(rating, max_stars=10):
    if not rating:
        return '<span class="stars">Not rated</span>'
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = max_stars - full - half
    s = "\u2605" * full + ("\u00BD" if half else "") + "\u2606" * empty
    return f'<span class="stars">{s} {rating}/10</span>'


def runtime_display(minutes):
    if not minutes:
        return "Unknown"
    h, m = divmod(minutes, 60)
    if h:
        return f"{h}h {m}m"
    return f"{m}m"
