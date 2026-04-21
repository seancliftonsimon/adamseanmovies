import streamlit as st
from html import escape

POSTER_PLACEHOLDER = "https://via.placeholder.com/185x278/003399/F2E400?text=NO+TAPE"

SHELF_COLS = 4


def inject_css():
    st.markdown("""
    <style>
    /* ===== GOOGLE FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Epilogue:ital,wght@0,400;0,700;0,800;0,900;1,800;1,900&family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap');

    /* ===== GLOBAL ===== */
    .block-container {
        max-width: 580px;
        padding-top: 1rem;
        padding-bottom: 5rem;
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

    /* ===== HIDE STREAMLIT CHROME ===== */
    #MainMenu, header, footer { display: none !important; }

    /* ===== STICKY APP HEADER ===== */
    .app-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background: #003399;
        border-bottom: 3px solid #1a1a1a;
        box-shadow: 0 4px 0 #F2E400;
        height: 56px;
        display: flex;
        align-items: center;
        padding: 0 1rem;
        gap: 0.75rem;
        box-sizing: border-box;
    }
    .app-header-logo {
        font-family: 'Epilogue', sans-serif;
        font-weight: 900;
        font-style: italic;
        font-size: 1.4rem;
        color: #F2E400;
        text-transform: uppercase;
        letter-spacing: -0.04em;
        text-shadow: 2px 2px 0 rgba(0,0,0,0.7);
        line-height: 1;
        white-space: nowrap;
    }
    .app-header-sep {
        width: 2px;
        height: 20px;
        background: rgba(255,255,255,0.25);
        flex-shrink: 0;
    }
    .app-header-tagline {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.58rem;
        font-weight: 700;
        color: rgba(255,255,255,0.5);
        text-transform: uppercase;
        letter-spacing: 0.14em;
        line-height: 1;
    }

    /* ===== NAVIGATION PILLS — dark strip style ===== */
    [data-testid="stPills"] {
        background: #1a1a1a !important;
        padding: 0 4px !important;
        border-radius: 0 !important;
        border-bottom: 2px solid #000 !important;
        margin-bottom: 1rem !important;
        gap: 0 !important;
    }
    [data-testid="stPills"] > label { display: none !important; }
    [data-testid="stPills"] [data-baseweb="radio-group"] {
        gap: 0 !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
    }
    [data-testid="stPills"] button {
        background: transparent !important;
        color: rgba(255,255,255,0.55) !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
        border-radius: 0 !important;
        font-family: 'Epilogue', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.68rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        padding: 10px 14px !important;
        box-shadow: none !important;
        transition: color 0.1s, border-color 0.1s !important;
    }
    [data-testid="stPills"] button:hover {
        background: rgba(255,255,255,0.08) !important;
        color: #ffffff !important;
        transform: none !important;
        box-shadow: none !important;
        border-color: rgba(242,228,0,0.4) !important;
    }
    [data-testid="stPills"] button[aria-checked="true"] {
        color: #F2E400 !important;
        border-bottom-color: #F2E400 !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    /* ===== FIXED BOTTOM NAV ===== */
    .app-bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background: #F2E400;
        border-top: 3px solid #1a1a1a;
        box-shadow: 0 -3px 0 rgba(0,0,0,0.15);
        height: 60px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 0;
        box-sizing: border-box;
    }
    .bnav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 2px;
        padding: 6px 18px;
        opacity: 0.6;
    }
    .bnav-item.bnav-active {
        opacity: 1;
        background: #003399;
        padding: 8px 18px;
        border: 2px solid #1a1a1a;
        box-shadow: 3px -3px 0 #1a1a1a;
        transform: translateY(-6px);
    }
    .bnav-item.bnav-active .bnav-icon,
    .bnav-item.bnav-active .bnav-label {
        color: #F2E400;
    }
    .bnav-icon {
        font-size: 1.1rem;
        line-height: 1;
        color: #1a1a1a;
    }
    .bnav-label {
        font-family: 'Epilogue', sans-serif;
        font-weight: 800;
        font-size: 0.48rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #1a1a1a;
        line-height: 1;
    }

    /* ===== VHS TAPE CARD ===== */
    .vhs-tape {
        background: #111111;
        border: 2px solid #1a1a1a;
        border-radius: 2px;
        box-shadow: 3px 3px 0 #1a1a1a;
        overflow: hidden;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
        margin-bottom: 2px;
    }
    .vhs-tape:hover {
        transform: translate(-2px, -2px);
        box-shadow: 5px 5px 0 #1a1a1a;
    }
    .vhs-img-wrap {
        position: relative;
        overflow: hidden;
    }
    .vhs-img-wrap img {
        width: 100%;
        display: block;
        aspect-ratio: 2/3;
        object-fit: cover;
        filter: grayscale(15%);
        transition: filter 0.3s ease;
    }
    .vhs-tape:hover .vhs-img-wrap img {
        filter: grayscale(0%);
    }
    .vhs-badge {
        position: absolute;
        top: 5px;
        left: 5px;
        background: #F2E400;
        color: #1a1a1a;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.42rem;
        font-weight: 700;
        padding: 2px 4px;
        border: 1px solid #1a1a1a;
        box-shadow: 1px 1px 0 #1a1a1a;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        line-height: 1.2;
    }
    /* Gloss overlay */
    .vhs-img-wrap::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg,
            rgba(255,255,255,0.12) 0%,
            rgba(255,255,255,0) 50%,
            rgba(0,0,0,0.08) 100%);
        pointer-events: none;
    }
    .vhs-info {
        background: #ffffff;
        border-top: 2px solid #1a1a1a;
        padding: 4px 6px 3px;
    }
    .vhs-title {
        display: block;
        font-family: 'Epilogue', sans-serif;
        font-weight: 800;
        font-size: 0.56rem;
        color: #1a1a1a;
        text-transform: uppercase;
        letter-spacing: -0.01em;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        line-height: 1.2;
    }
    .vhs-meta {
        display: block;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.42rem;
        font-weight: 500;
        color: #747684;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        line-height: 1.2;
        margin-top: 1px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
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
        margin-bottom: 0;
        font-family: 'Epilogue', sans-serif;
        font-weight: 800;
        color: #F2E400;
        font-size: 0.85rem;
        letter-spacing: 0.04em;
        border-radius: 4px 4px 0 0;
        text-transform: uppercase;
        border: 2px solid #1a1a1a;
        border-bottom: none;
        box-shadow: 3px 0 0 #1a1a1a, -1px 0 0 #1a1a1a;
    }
    .vhs-drawer-end {
        height: 4px;
        background: #F2E400;
        border: 2px solid #1a1a1a;
        border-top: none;
        margin-top: 0;
        margin-bottom: 0.75rem;
    }

    /* ===== STAT CARDS ===== */
    .stat-cards-row {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-bottom: 1.25rem;
    }
    .stat-card {
        background: #ffffff;
        border: 2px solid #1a1a1a;
        box-shadow: 4px 4px 0 #1a1a1a;
        padding: 1rem 0.85rem 0.75rem;
        position: relative;
        overflow: hidden;
    }
    .stat-card-yellow {
        background: #F2E400;
    }
    .stat-label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.58rem;
        font-weight: 700;
        color: #002068;
        opacity: 0.65;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 0 0 4px;
        line-height: 1;
    }
    .stat-card-yellow .stat-label { color: #1a1a1a; opacity: 0.7; }
    .stat-value {
        font-family: 'Epilogue', sans-serif;
        font-weight: 900;
        font-size: 2rem;
        color: #002068;
        line-height: 1;
        letter-spacing: -0.04em;
        margin: 0 0 4px;
    }
    .stat-card-yellow .stat-value { color: #1a1a1a; }
    .stat-sub {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.56rem;
        font-weight: 700;
        color: #444653;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin: 0;
        line-height: 1.3;
    }

    /* ===== STORE SIGN (section headers) ===== */
    .store-sign {
        background: #003399;
        color: #F2E400;
        padding: 0.65rem 1rem;
        border-radius: 4px;
        font-family: 'Epilogue', sans-serif;
        font-size: 1.05rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        text-align: center;
        margin-bottom: 0.75rem;
        border: 2px solid #1a1a1a;
        box-shadow: 4px 4px 0 #1a1a1a;
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

    /* ===== METRIC CARDS (legacy — used as fallback) ===== */
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
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* ===== EXPANDER ===== */
    [data-testid="stExpander"] {
        background: #ffffff;
        border: 2px solid #1a1a1a !important;
        border-radius: 4px;
        margin-bottom: 0.5rem;
        box-shadow: 3px 3px 0 #1a1a1a;
    }
    [data-testid="stExpander"]:hover { box-shadow: 4px 4px 0 #1a1a1a; }
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
    [data-testid="stHorizontalRule"] { border-color: #1a1a1a; border-width: 2px; }

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

    /* ===== PICKER CARD (pick_for_us) ===== */
    .picker-card {
        background: #003399;
        border: 2px solid #1a1a1a;
        border-radius: 6px;
        padding: 1.5rem 1.25rem;
        text-align: center;
        box-shadow: 6px 6px 0 #1a1a1a;
        color: #ffffff;
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

    /* ===== SIDEBAR (fallback) ===== */
    [data-testid="stSidebar"] {
        background: #003399;
        border-right: 3px solid #1a1a1a;
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }

    /* ===== MOBILE ===== */
    @media (max-width: 640px) {
        .block-container {
            width: 100vw !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
            overflow-x: clip !important;
            padding-top: 0.5rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            padding-bottom: 5rem;
        }
        div.stButton > button {
            width: 100%;
            padding: 0.5rem 0.5rem;
        }
        h1 { font-size: 1.4rem !important; }
        .store-sign { font-size: 0.9rem; padding: 0.5rem 0.75rem; }
        .genre-pill { font-size: 0.58rem; padding: 2px 5px; }
        [data-testid="stMetric"] { padding: 0.4rem; }
        .stat-cards-row { gap: 8px; }
        .stat-value { font-size: 1.6rem; }

        /* Shelf row: controlled 2-col flex layout */
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

        /* Legacy 2-col fallback */
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
        .block-container { max-width: 680px; padding-top: 1.5rem; }
        .app-header-logo { font-size: 1.6rem; }
        .stat-cards-row { grid-template-columns: repeat(4, 1fr); }
    }
    </style>
    """, unsafe_allow_html=True)


# ── Layout HTML helpers ──────────────────────────────────────────────

def app_header_html():
    """Sticky top header bar."""
    return (
        '<div class="app-header">'
        '<div class="app-header-logo">📼 Adam &amp; Sean</div>'
        '<div class="app-header-sep"></div>'
        '<div class="app-header-tagline">Movie Vault</div>'
        '</div>'
    )


def bottom_nav_html(active=None):
    """Fixed bottom navigation bar. active = the current page label string."""
    items = [
        ("🎬", "Add"),
        ("🎰", "Pick"),
        ("📋", "Lists"),
        ("📼", "Log"),
    ]
    parts = []
    for icon, label in items:
        is_active = active and label in active
        cls = "bnav-item bnav-active" if is_active else "bnav-item"
        parts.append(
            f'<div class="{cls}">'
            f'<span class="bnav-icon">{icon}</span>'
            f'<span class="bnav-label">{label.upper()}</span>'
            f'</div>'
        )
    return f'<div class="app-bottom-nav">{"".join(parts)}</div>'


# ── Content HTML helpers ──────────────────────────────────────────────

def section_header(text):
    st.markdown(f'<div class="store-sign">{escape(text)}</div>',
                unsafe_allow_html=True)


def vhs_tape_html(img_url, title, year=None, badge=None):
    """VHS-style movie card: black image area with white info footer."""
    meta = str(year) if year else ""
    badge_html = (f'<div class="vhs-badge">{escape(badge)}</div>'
                  if badge else "")
    return (
        f'<div class="vhs-tape">'
        f'<div class="vhs-img-wrap">'
        f'<img src="{img_url}" alt="{escape(title)}" loading="lazy" />'
        f'{badge_html}'
        f'</div>'
        f'<div class="vhs-info">'
        f'<span class="vhs-title">{escape(title)}</span>'
        + (f'<span class="vhs-meta">{escape(meta)}</span>' if meta else '')
        + f'</div>'
        f'</div>'
    )


def shelf_row_html(movies, make_poster_url_fn, poster_placeholder):
    """Render a row of posters in a controlled 2-col flex layout for mobile."""
    cells = []
    for movie in movies:
        img = (make_poster_url_fn(movie["poster_path"], "w154")
               if movie["poster_path"] else poster_placeholder)
        title = movie["title"]
        year = str(movie["year"]) if movie.get("year") else ""
        cells.append(
            f'<div class="shelf-cell">'
            f'<div class="vhs-tape">'
            f'<div class="vhs-img-wrap">'
            f'<img src="{img}" alt="{escape(title)}" loading="lazy" />'
            f'</div>'
            f'<div class="vhs-info">'
            f'<span class="vhs-title">{escape(title)}</span>'
            + (f'<span class="vhs-meta">{escape(year)}</span>' if year else '')
            + f'</div>'
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


def stat_card_html(label, value, sub=None, yellow=False):
    """Single stat card with big Epilogue number."""
    cls = "stat-card stat-card-yellow" if yellow else "stat-card"
    sub_html = f'<p class="stat-sub">{escape(str(sub))}</p>' if sub else ""
    return (
        f'<div class="{cls}">'
        f'<p class="stat-label">{escape(label)}</p>'
        f'<h2 class="stat-value">{escape(str(value))}</h2>'
        f'{sub_html}'
        f'</div>'
    )


def stat_cards_row_html(cards):
    """Render a row of stat cards. cards = list of dicts with label/value/sub/yellow."""
    inner = "".join(
        stat_card_html(c["label"], c["value"], c.get("sub"), c.get("yellow", False))
        for c in cards
    )
    return f'<div class="stat-cards-row">{inner}</div>'
