import streamlit as st
from html import escape

POSTER_PLACEHOLDER = "https://via.placeholder.com/185x278/003399/F2E400?text=NO+TAPE"

SHELF_COLS = 4


def inject_css():
    st.markdown("""
    <style>
    /* ===== GOOGLE FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Epilogue:wght@400;700;800;900&family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap');

    /* ===== GLOBAL ===== */
    .block-container {
        max-width: 540px;
        padding-top: 1rem;
        padding-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {
        background-color: #f9f9f9;
        overflow-x: hidden;
    }

    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3 {
        font-family: 'Epilogue', sans-serif !important;
        font-weight: 900 !important;
        color: #1a1a1a !important;
        letter-spacing: -0.02em !important;
    }
    h1 { font-size: 1.8rem !important; letter-spacing: -0.03em !important; }
    h2 { font-size: 1.4rem !important; }
    h3 { font-size: 1.1rem !important; }
    p, li { font-family: 'Inter', sans-serif; color: #1a1a1a; }

    /* ===== HIDE CHROME ===== */
    #MainMenu, header, footer { visibility: hidden; }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: #003399;
        border-right: 3px solid #1a1a1a;
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    [data-testid="stSidebarUserContent"] p,
    [data-testid="stSidebarUserContent"] span {
        color: #ffffff !important;
    }

    /* ===== STORE SIGN (section headers) ===== */
    .store-sign {
        background: #003399;
        color: #F2E400;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        font-family: 'Epilogue', sans-serif;
        font-size: 1.1rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        text-align: center;
        margin-bottom: 0.75rem;
        border: 2px solid #1a1a1a;
        box-shadow: 4px 4px 0 #1a1a1a;
    }

    /* ===== VHS TAPE ===== */
    .vhs-tape {
        background: #ffffff;
        border: 2px solid #1a1a1a;
        border-radius: 3px;
        padding: 3px 3px 0 3px;
        box-shadow: 3px 3px 0 #1a1a1a;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
        margin-bottom: 2px;
    }
    .vhs-tape:hover {
        transform: translate(-2px, -2px);
        box-shadow: 5px 5px 0 #1a1a1a;
    }
    .vhs-tape img {
        width: 100%;
        display: block;
        border-radius: 1px;
        aspect-ratio: 2/3;
        object-fit: cover;
    }
    .vhs-spine {
        background: #003399;
        color: #F2E400;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.52rem;
        font-weight: 700;
        padding: 3px 3px;
        text-align: center;
        margin-top: 3px;
        margin-bottom: 2px;
        border-radius: 1px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        line-height: 1.3;
    }

    /* ===== SHELF BAR ===== */
    .shelf-bar {
        height: 6px;
        background: #1a1a1a;
        margin: 2px 0 8px;
        border-radius: 0;
    }

    /* ===== DRAWER ===== */
    .vhs-drawer-header {
        background: #003399;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.25rem;
        font-family: 'Epilogue', sans-serif;
        font-weight: 800;
        color: #F2E400;
        font-size: 0.85rem;
        letter-spacing: 0.04em;
        border-radius: 4px 4px 0 0;
        text-transform: uppercase;
        border: 2px solid #1a1a1a;
        border-bottom: none;
        box-shadow: 3px 3px 0 #1a1a1a;
    }
    .vhs-drawer-end {
        height: 4px;
        background: #F2E400;
        border: 2px solid #1a1a1a;
        border-top: none;
        margin-top: 0;
        margin-bottom: 0.75rem;
    }

    /* ===== GENRE PILLS ===== */
    .genre-pill {
        display: inline-block;
        background: #1a1a1a;
        color: #F2E400;
        padding: 2px 8px;
        border-radius: 20px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.65rem;
        margin: 2px 3px 2px 0;
        font-weight: 700;
        border: 1.5px solid #1a1a1a;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* ===== STAR RATINGS ===== */
    .stars {
        color: #F2E400;
        font-size: 1rem;
        letter-spacing: 1px;
        font-weight: 700;
        -webkit-text-stroke: 0.5px #1a1a1a;
    }

    /* ===== BUTTONS ===== */
    div.stButton > button {
        background: #ffffff;
        color: #1a1a1a;
        border: 2px solid #1a1a1a;
        border-radius: 4px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.7rem;
        box-shadow: 3px 3px 0 #1a1a1a;
        transition: transform 0.1s, box-shadow 0.1s;
    }
    div.stButton > button:hover {
        transform: translate(-1px, -1px);
        box-shadow: 4px 4px 0 #1a1a1a;
        border-color: #1a1a1a;
        background: #ffffff;
        color: #1a1a1a;
    }
    div.stButton > button:active {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0 #1a1a1a;
    }
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="stBaseButton-primary"] {
        background: #F2E400;
        color: #1a1a1a;
        border: 2px solid #1a1a1a;
        font-family: 'Epilogue', sans-serif;
        font-weight: 800;
        font-size: 0.8rem;
        padding: 0.55rem 1rem;
        border-radius: 4px;
        box-shadow: 4px 4px 0 #1a1a1a;
    }
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: #F2E400;
        color: #1a1a1a;
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0 #1a1a1a;
    }
    div.stButton > button[kind="primary"]:active,
    div.stButton > button[data-testid="stBaseButton-primary"]:active {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0 #1a1a1a;
    }

    /* ===== STAT / METRIC CARDS ===== */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 2px solid #1a1a1a;
        border-radius: 4px;
        padding: 0.65rem;
        box-shadow: 3px 3px 0 #1a1a1a;
    }
    [data-testid="stMetric"] label {
        color: #444444 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.65rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #003399 !important;
        font-family: 'Epilogue', sans-serif !important;
        font-weight: 900 !important;
    }

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #e2e2e2;
        border-radius: 4px;
        padding: 4px;
        border: 2px solid #1a1a1a;
        box-shadow: 3px 3px 0 #1a1a1a;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 2px;
        padding: 7px 14px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.75rem;
        color: #444444;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stTabs [aria-selected="true"] {
        background: #003399 !important;
        color: #F2E400 !important;
        border-radius: 2px !important;
        box-shadow: 2px 2px 0 #1a1a1a !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ===== EXPANDER ===== */
    [data-testid="stExpander"] {
        background: #ffffff;
        border: 2px solid #1a1a1a !important;
        border-radius: 4px;
        margin-bottom: 0.5rem;
        box-shadow: 3px 3px 0 #1a1a1a;
    }
    [data-testid="stExpander"]:hover {
        box-shadow: 4px 4px 0 #1a1a1a;
    }
    [data-testid="stExpander"] summary {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #1a1a1a;
    }

    /* ===== TEXT INPUT ===== */
    [data-testid="stTextInput"] input {
        background: #ffffff;
        border: 2px solid #1a1a1a;
        border-radius: 4px;
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #003399;
        box-shadow: 0 0 0 3px #F2E400;
    }
    [data-testid="stTextInput"] label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 0.75rem !important;
        color: #1a1a1a !important;
    }

    /* ===== TEXT AREA ===== */
    [data-testid="stTextArea"] textarea {
        background: #ffffff;
        border: 2px solid #1a1a1a;
        border-radius: 4px;
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stTextArea"] textarea:focus {
        border-color: #003399;
        box-shadow: 0 0 0 3px #F2E400;
    }
    [data-testid="stTextArea"] label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 0.75rem !important;
        color: #1a1a1a !important;
    }

    /* ===== SELECT BOX ===== */
    [data-testid="stSelectbox"] > div > div {
        background: #ffffff;
        border: 2px solid #1a1a1a;
        border-radius: 4px;
        color: #1a1a1a;
    }
    [data-testid="stSelectbox"] label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 0.75rem !important;
        color: #1a1a1a !important;
    }

    /* ===== DIVIDER ===== */
    [data-testid="stHorizontalRule"] {
        border-color: #1a1a1a;
        border-width: 2px;
    }

    /* ===== IMAGE ===== */
    [data-testid="stImage"] img {
        border-radius: 2px;
        border: 2px solid #1a1a1a;
        box-shadow: 3px 3px 0 #1a1a1a;
    }

    /* ===== CAPTION ===== */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #444653 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.68rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
    }

    /* ===== ALERTS ===== */
    [data-testid="stAlert"] {
        border-radius: 4px;
        border: 2px solid #1a1a1a !important;
        box-shadow: 3px 3px 0 #1a1a1a;
        font-family: 'Inter', sans-serif;
    }

    /* ===== NAVIGATION ===== */
    nav[data-testid="stSidebarNav"] a {
        border-radius: 4px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        padding: 0.5rem 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #ffffff !important;
    }
    nav[data-testid="stSidebarNav"] a:hover {
        background: #002068;
        color: #F2E400 !important;
    }
    nav[data-testid="stSidebarNav"] a[aria-current="page"] {
        background: #F2E400;
        color: #1a1a1a !important;
        border: 2px solid #1a1a1a;
        box-shadow: 2px 2px 0 #1a1a1a;
    }

    /* ===== PICKER CARD (pick_for_us) ===== */
    .picker-card {
        background: #ffffff;
        border: 2px solid #1a1a1a;
        border-radius: 6px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 5px 5px 0 #003399;
    }

    /* ===== MOVIE CARD (search results in add_movie) ===== */
    .movie-card {
        background: #ffffff;
        border-radius: 4px;
        padding: 0.85rem;
        margin-bottom: 0.5rem;
        border: 2px solid #1a1a1a;
        box-shadow: 3px 3px 0 #1a1a1a;
        transition: transform 0.1s, box-shadow 0.1s;
    }
    .movie-card:hover {
        transform: translate(-1px, -1px);
        box-shadow: 4px 4px 0 #1a1a1a;
    }
    .movie-card img {
        border-radius: 2px;
        width: 100%;
        max-width: 185px;
        border: 1px solid #1a1a1a;
    }

    /* ===== MOBILE-FIRST ===== */
    @media (max-width: 640px) {
        .block-container {
            width: 100vw !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
            overflow-x: clip !important;
            padding-top: 2.8rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        div.stButton > button {
            width: 100%;
            padding: 0.5rem 0.5rem;
        }
        h1 { font-size: 1.4rem !important; }
        .store-sign { font-size: 0.9rem; padding: 0.5rem 0.75rem; }
        .vhs-spine { font-size: 0.45rem; padding: 2px; }
        .genre-pill { font-size: 0.58rem; padding: 2px 5px; }
        [data-testid="stMetric"] { padding: 0.4rem; }

        /* Shelf row: controlled 2-col flex layout (our_lists mobile only) */
        .shelf-row-two-col {
            display: flex !important;
            gap: 0.5rem !important;
            width: 100% !important;
            max-width: 100% !important;
            margin-bottom: 2px !important;
            overflow: hidden !important;
        }
        .shelf-row-two-col .shelf-cell {
            flex: 0 0 calc(50% - 0.25rem) !important;
            max-width: calc(50% - 0.25rem) !important;
            min-width: 0 !important;
            box-sizing: border-box !important;
        }
        .shelf-row-two-col .vhs-tape {
            width: 100% !important;
            max-width: 100% !important;
        }

        /* Legacy: 2-col column layout constraint (fallback if using st.columns) */
        [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:first-child:nth-last-child(2)):has(.vhs-tape) {
            display: flex !important;
            flex-wrap: nowrap !important;
            gap: 0.35rem !important;
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            overflow: hidden !important;
        }
        [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:first-child:nth-last-child(2)):has(.vhs-tape) > [data-testid="column"] {
            flex: 0 0 calc(50% - 0.2rem) !important;
            max-width: calc(50% - 0.2rem) !important;
            min-width: 0 !important;
            overflow: hidden !important;
        }
        [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:first-child:nth-last-child(2)):has(.vhs-tape) .vhs-tape {
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
        }
        [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:first-child:nth-last-child(2)):has(.vhs-tape) .vhs-tape img {
            max-width: 100% !important;
            width: 100% !important;
            height: auto !important;
            aspect-ratio: 2/3 !important;
            object-fit: cover !important;
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


def shelf_row_html(movies, make_poster_url_fn, poster_placeholder):
    """Render a row of posters in a controlled 2-col flex layout for mobile."""
    cells = []
    for movie in movies:
        img = (make_poster_url_fn(movie["poster_path"], "w154")
               if movie["poster_path"] else poster_placeholder)
        label = movie["title"] if len(movie["title"]) <= 20 else movie["title"][:18] + "\u2026"
        if movie.get("year"):
            yr = f" ({movie['year']})"
            if len(label) + len(yr) <= 24:
                label += yr
        cells.append(
            f'<div class="shelf-cell">'
            f'<div class="vhs-tape">'
            f'<img src="{img}" alt="{escape(movie["title"])}" />'
            f'<div class="vhs-spine">{escape(label)}</div>'
            f'</div></div>'
        )
    return f'<div class="shelf-row-two-col">{"".join(cells)}</div>'


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
