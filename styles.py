import streamlit as st
from html import escape

POSTER_PLACEHOLDER = "https://via.placeholder.com/185x278/003399/F2E400?text=NO+TAPE"

SHELF_COLS = 4


def inject_css():
    st.markdown("""
    <style>
    /* ===== GOOGLE FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Epilogue:ital,wght@0,400;0,700;0,800;0,900;1,800;1,900&family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap');
    :root {
        --ink: #1a1a1a;
        --royal: #003399;
        --pop-yellow: #F2E400;
        --paper: #fffcf3;
        --panel-shadow: #2c69d8;
        --hard-shadow: 4px 4px 0 var(--ink);
    }

    /* ===== GLOBAL ===== */
    .block-container {
        max-width: 980px;
        padding-top: 8.9rem;   /* clears fixed header + top nav */
        padding-bottom: 2.2rem;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
    }
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {
        background:
            radial-gradient(circle at top right, rgba(0, 51, 153, 0.05), transparent 22%),
            linear-gradient(180deg, #f7f3e8 0%, #f6f2e8 100%);
        overflow-x: hidden;
    }

    /* ===== HIDE STREAMLIT CHROME ===== */
    #MainMenu, header, footer { display: none !important; }

    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3 {
        font-family: 'Epilogue', sans-serif !important;
        font-weight: 900 !important;
        color: #1a1a1a !important;
        letter-spacing: -0.02em !important;
    }
    h1 { font-size: 2rem !important; letter-spacing: -0.03em !important; }
    h2 { font-size: 1.5rem !important; }
    h3 { font-size: 1.2rem !important; }
    p, li { font-family: 'Inter', sans-serif; color: #1a1a1a; font-size: 1rem; }

    /* ===== STICKY APP HEADER ===== */
    .app-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background: #2c69d8;
        border-bottom: 4px solid #111111;
        box-shadow: 0 4px 0 #F2C900;
        height: 74px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding: 0 1.6rem;
        gap: 0.9rem;
        box-sizing: border-box;
    }
    .app-header-logo {
        font-family: 'Epilogue', sans-serif;
        font-weight: 900;
        font-style: italic;
        font-size: 2rem;
        color: #FFD51F;
        text-transform: uppercase;
        letter-spacing: -0.05em;
        text-shadow: 2px 2px 0 #111111;
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
        font-size: 0.7rem;
        font-weight: 700;
        color: rgba(255,255,255,0.75);
        text-transform: uppercase;
        letter-spacing: 0.18em;
        line-height: 1;
    }

    /* ===== TOP NAV BAR ===== */
    [data-testid="stVerticalBlock"]:has(.top-nav-widget-anchor) {
        position: fixed;
        top: 74px;
        left: 0;
        right: 0;
        z-index: 999;
        padding: 0.35rem 1rem 0.55rem;
        background: #2c69d8;
        border-bottom: 3px solid #1a1a1a;
        box-shadow: 0 4px 0 #F2C900;
    }
    .top-nav-widget-anchor { display: none; }
    [data-testid="stVerticalBlock"]:has(.top-nav-widget-anchor) [data-testid="stSegmentedControl"] {
        max-width: 980px;
        margin: 0 auto;
    }
    [data-testid="stVerticalBlock"]:has(.top-nav-widget-anchor) [data-baseweb="button-group"] {
        width: 100%;
        display: grid !important;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 8px;
        background: transparent !important;
    }
    [data-testid="stVerticalBlock"]:has(.top-nav-widget-anchor) [data-baseweb="button-group"] > button {
        min-height: 52px;
        border-radius: 4px !important;
        border: 2px solid #1a1a1a !important;
        background: #fff9db !important;
        color: #1a1a1a !important;
        box-shadow: 4px 4px 0 rgba(0,51,153,0.18) !important;
        font-family: 'Epilogue', sans-serif;
        font-weight: 800;
        font-size: 0.76rem;
        letter-spacing: 0.06em;
        line-height: 1.3;
        text-transform: uppercase;
    }
    [data-testid="stVerticalBlock"]:has(.top-nav-widget-anchor) [data-baseweb="button-group"] > button:hover {
        transform: translate(-1px, -1px);
        box-shadow: 5px 5px 0 #1a1a1a !important;
    }
    [data-testid="stVerticalBlock"]:has(.top-nav-widget-anchor) [data-baseweb="button-group"] > button[aria-pressed="true"] {
        background: #003399;
        color: #F2E400 !important;
        box-shadow: 4px 4px 0 #1a1a1a !important;
    }

    /* ===== PILLS (genre filter, list selector — NOT nav) ===== */
    [data-testid="stPills"] {
        gap: 6px !important;
    }
    [data-testid="stPills"] > label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        font-size: 0.85rem !important;
        color: #1a1a1a !important;
    }
    [data-testid="stPills"] button {
        background: #fffdf5 !important;
        color: #1a1a1a !important;
        border: 2px solid #1a1a1a !important;
        border-radius: 999px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.78rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 6px 14px !important;
        box-shadow: 3px 3px 0 rgba(0,51,153,0.15) !important;
        transition: transform 0.1s !important;
    }
    [data-testid="stPills"] button:hover {
        transform: translate(-1px, -1px) !important;
        box-shadow: 3px 3px 0 #1a1a1a !important;
        background: #ffffff !important;
        color: #1a1a1a !important;
    }
    [data-testid="stPills"] button[aria-checked="true"] {
        background: #003399 !important;
        color: #F2E400 !important;
        border-color: #1a1a1a !important;
        box-shadow: 4px 4px 0 #1a1a1a !important;
        transform: none !important;
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
    .vhs-img-wrap { position: relative; overflow: hidden; }
    .vhs-img-wrap img {
        width: 100%;
        display: block;
        aspect-ratio: 2/3;
        object-fit: cover;
        filter: grayscale(15%);
        transition: filter 0.3s ease;
    }
    .vhs-tape:hover .vhs-img-wrap img { filter: grayscale(0%); }
    .vhs-badge {
        position: absolute;
        top: 5px;
        left: 5px;
        background: #F2E400;
        color: #1a1a1a;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.48rem;
        font-weight: 700;
        padding: 2px 5px;
        border: 1px solid #1a1a1a;
        box-shadow: 1px 1px 0 #1a1a1a;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        line-height: 1.2;
    }
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
        padding: 5px 7px 4px;
    }
    .vhs-title {
        display: block;
        font-family: 'Epilogue', sans-serif;
        font-weight: 800;
        font-size: 0.65rem;
        color: #1a1a1a;
        text-transform: uppercase;
        letter-spacing: -0.01em;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        line-height: 1.25;
    }
    .vhs-meta {
        display: block;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.52rem;
        font-weight: 500;
        color: #747684;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        line-height: 1.2;
        margin-top: 2px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    /* ===== SHELF BAR ===== */
    .shelf-bar {
        height: 6px;
        background: #1a1a1a;
        margin: 2px 0 10px;
    }

    /* ===== DRAWER ===== */
    .vhs-drawer-header {
        background: #003399;
        padding: 0.6rem 0.85rem;
        margin-bottom: 0;
        font-family: 'Epilogue', sans-serif;
        font-weight: 800;
        color: #F2E400;
        font-size: 0.95rem;
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
        margin-bottom: 1rem;
    }

    /* ===== STAT CARDS ===== */
    .stat-cards-row {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 14px;
        margin-bottom: 1.5rem;
    }
    .stat-card {
        background: var(--paper);
        border: 2px solid var(--ink);
        box-shadow: var(--hard-shadow);
        padding: 1.1rem 1rem 0.85rem;
        position: relative;
        overflow: hidden;
    }
    .stat-card-yellow { background: #F2E400; }
    .stat-label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.68rem;
        font-weight: 700;
        color: #002068;
        opacity: 0.65;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 0 0 6px;
        line-height: 1;
    }
    .stat-card-yellow .stat-label { color: #1a1a1a; opacity: 0.7; }
    .stat-value {
        font-family: 'Epilogue', sans-serif;
        font-weight: 900;
        font-size: 2.4rem;
        color: #002068;
        line-height: 1;
        letter-spacing: -0.04em;
        margin: 0 0 4px;
    }
    .stat-card-yellow .stat-value { color: #1a1a1a; }
    .stat-sub {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.62rem;
        font-weight: 700;
        color: #444653;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin: 0;
        line-height: 1.3;
    }

    /* ===== STORE SIGN (section headers) ===== */
    .store-sign {
        background: var(--royal);
        color: var(--pop-yellow);
        padding: 0.85rem 1.1rem;
        border-radius: 4px;
        font-family: 'Epilogue', sans-serif;
        font-size: 1.25rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        text-align: center;
        margin-bottom: 0.85rem;
        border: 2px solid var(--ink);
        box-shadow: var(--hard-shadow);
    }

    /* ===== GENRE PILLS ===== */
    .genre-pill {
        display: inline-block;
        background: #1a1a1a;
        color: #F2E400;
        padding: 3px 10px;
        border-radius: 20px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.72rem;
        margin: 2px 3px 2px 0;
        font-weight: 700;
        border: 1.5px solid #1a1a1a;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* ===== STAR RATINGS ===== */
    .stars {
        color: #F2E400;
        font-size: 1.1rem;
        letter-spacing: 1px;
        font-weight: 700;
        -webkit-text-stroke: 0.5px #1a1a1a;
    }

    /* ===== BUTTONS (global) ===== */
    div.stButton > button {
        background: var(--paper);
        color: var(--ink);
        border: 2px solid var(--ink);
        border-radius: 4px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.8rem;
        padding: 0.55rem 0.9rem;
        box-shadow: 3px 3px 0 var(--ink);
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
        background: #F2E400 !important;
        color: #1a1a1a !important;
        border: 2px solid #1a1a1a;
        font-family: 'Epilogue', sans-serif;
        font-weight: 800;
        font-size: 0.9rem;
        padding: 0.6rem 1rem;
        border-radius: 4px;
        box-shadow: 4px 4px 0 #1a1a1a;
    }
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: #F2E400 !important;
        color: #1a1a1a !important;
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0 #1a1a1a;
    }
    div.stButton > button[kind="primary"]:active,
    div.stButton > button[data-testid="stBaseButton-primary"]:active {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0 #1a1a1a;
    }

    /* ===== METRIC CARDS ===== */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 2px solid #1a1a1a;
        border-radius: 4px;
        padding: 0.85rem;
        box-shadow: 3px 3px 0 #1a1a1a;
    }
    [data-testid="stMetric"] label {
        color: #444444 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #003399 !important;
        font-family: 'Epilogue', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.8rem !important;
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
        padding: 8px 16px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.82rem;
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
        margin-bottom: 0.6rem;
        box-shadow: 3px 3px 0 #1a1a1a;
    }
    [data-testid="stExpander"]:hover { box-shadow: 4px 4px 0 #1a1a1a; }
    [data-testid="stExpander"] summary {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.85rem;
        color: #1a1a1a;
        padding: 0.75rem 1rem;
    }

    /* ===== TEXT INPUT ===== */
    [data-testid="stTextInput"] input {
        background: #ffffff;
        border: 2px solid #1a1a1a;
        border-radius: 4px;
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        padding: 0.6rem 0.75rem;
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
        font-size: 0.82rem !important;
        color: #1a1a1a !important;
    }

    /* ===== TEXT AREA ===== */
    [data-testid="stTextArea"] textarea {
        background: #ffffff;
        border: 2px solid #1a1a1a;
        border-radius: 4px;
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
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
        font-size: 0.82rem !important;
        color: #1a1a1a !important;
    }

    /* ===== SELECT BOX ===== */
    [data-testid="stSelectbox"] > div > div {
        background: #ffffff;
        border: 2px solid #1a1a1a;
        border-radius: 4px;
        color: #1a1a1a;
        font-size: 1rem;
    }
    [data-testid="stSelectbox"] label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 0.82rem !important;
        color: #1a1a1a !important;
    }

    /* ===== RADIO BUTTONS ===== */
    [data-testid="stRadio"] label {
        color: #1a1a1a !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
    }
    [data-testid="stRadio"] > label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        font-size: 0.82rem !important;
    }
    /* Selected radio dot — white fill so it's readable on any bg */
    [data-testid="stRadio"] [data-baseweb="radio"][aria-checked="true"] [role="presentation"] {
        background-color: #003399 !important;
        border-color: #003399 !important;
    }

    /* ===== SLIDER ===== */
    [data-testid="stSlider"] > label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        font-size: 0.82rem !important;
        color: #1a1a1a !important;
    }
    [data-testid="stSlider"] [data-testid="stTickBar"] span,
    [data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
        color: #1a1a1a !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
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
        font-size: 0.78rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
    }

    /* ===== ALERTS ===== */
    [data-testid="stAlert"] {
        border-radius: 4px;
        border: 2px solid #1a1a1a !important;
        box-shadow: 3px 3px 0 #1a1a1a;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
    }

    /* ===== PICKER CARD ===== */
    .picker-card {
        background: #003399;
        border: 2px solid #1a1a1a;
        border-radius: 6px;
        padding: 1.75rem 1.5rem;
        text-align: center;
        box-shadow: 6px 6px 0 #1a1a1a;
        color: #ffffff;
    }

    /* ===== PICK PAGE ===== */
    .pick-page-anchor,
    .pick-filter-panel-anchor,
    .pick-result-anchor,
    .pick-reveal-anchor {
        display: none;
    }

    .pick-kicker,
    .pick-result-kicker {
        display: inline-block;
        background: #003399;
        color: #ffffff;
        border: 3px solid #111111;
        box-shadow: 5px 5px 0 #111111;
        padding: 0.55rem 0.95rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }

    .pick-title {
        margin: 1rem 0 0.7rem;
        font-family: 'Epilogue', sans-serif;
        font-size: clamp(2.75rem, 8vw, 4.9rem);
        line-height: 0.92;
        font-style: italic;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -0.06em;
        color: #003399;
    }

    .pick-lead {
        margin: 0;
        max-width: 42rem;
        color: #586273;
        font-size: 1.05rem;
        line-height: 1.55;
    }

    .pick-flow-section {
        margin-top: 1rem;
    }

    .pick-flow-card {
        background: rgba(255, 252, 243, 0.98);
        border: 3px solid #111111;
        box-shadow: 8px 8px 0 #2c69d8;
        padding: 1rem 1rem 1.1rem;
    }

    .pick-subhead {
        margin-bottom: 0.45rem;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #677089;
    }

    .pick-runtime-subhead {
        margin-top: 1rem;
    }

    .pick-results-card {
        background: #fffef6;
        border: 3px solid #111111;
        box-shadow: 10px 10px 0 #111111;
        padding: 1rem;
        position: sticky;
        top: 142px;
    }

    .pick-results-count {
        font-family: 'Epilogue', sans-serif;
        color: #003399;
        font-weight: 900;
        font-size: clamp(1.45rem, 3vw, 2.2rem);
        line-height: 1.02;
        letter-spacing: -0.03em;
        margin: 0.15rem 0 0.35rem;
    }

    .pick-results-summary {
        color: #4f5a70;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.82rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    .pick-results-thumbs {
        display: flex;
        gap: 0.45rem;
        margin-bottom: 0.85rem;
    }

    .pick-results-thumbs img {
        width: 62px;
        aspect-ratio: 2 / 3;
        object-fit: cover;
        border: 2px solid #111111;
        box-shadow: 3px 3px 0 #2c69d8;
    }

    .pick-meta-band {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin: 0.35rem 0 1rem;
    }

    .pick-meta-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: #fff6bf;
        border: 2px solid #111111;
        border-radius: 999px;
        padding: 0.38rem 0.72rem;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #1a1a1a;
    }

    .pick-result-title {
        margin: 0.75rem 0 0.45rem;
        font-family: 'Epilogue', sans-serif;
        font-size: clamp(2rem, 5vw, 3rem);
        line-height: 0.95;
        font-style: italic;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -0.05em;
        color: #003399;
    }

    .pick-result-overview {
        margin: 0.75rem 0 0;
        color: #334158;
        font-size: 1rem;
        line-height: 1.65;
    }

    .pick-reveal-copy {
        text-align: center;
        padding: 1rem 0 0.4rem;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #5e6880;
    }

    [data-testid="stVerticalBlock"]:has(.pick-result-anchor),
    [data-testid="stVerticalBlock"]:has(.pick-reveal-anchor) {
        background: var(--paper);
        border: 3px solid #111111;
        border-radius: 6px;
        box-shadow: 10px 10px 0 var(--panel-shadow);
        padding: 1.45rem clamp(1rem, 2.4vw, 2rem);
        margin-bottom: 1.6rem;
        gap: 1rem;
    }

    [data-testid="stVerticalBlock"]:has(.pick-result-anchor) [data-testid="stHorizontalBlock"] {
        align-items: start;
    }

    [data-testid="stVerticalBlock"]:has(.pick-result-anchor) [data-testid="stImage"] img,
    [data-testid="stVerticalBlock"]:has(.pick-reveal-anchor) [data-testid="stImage"] img {
        box-shadow: 7px 7px 0 #111111;
    }

    [data-testid="stVerticalBlock"]:has(.pick-flow-card) [data-testid="stPills"] {
        margin-bottom: 0.4rem;
    }

    [data-testid="stVerticalBlock"]:has(.pick-flow-card) [data-testid="stPills"] [role="radiogroup"],
    [data-testid="stVerticalBlock"]:has(.pick-flow-card) [data-testid="stPills"] [role="group"] {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    [data-testid="stVerticalBlock"]:has(.pick-flow-card) [data-testid="stPills"] button {
        min-height: 2.25rem;
    }

    [data-testid="stVerticalBlock"]:has(.pick-results-card) div.stButton > button[kind="primary"],
    [data-testid="stVerticalBlock"]:has(.pick-results-card) div.stButton > button[data-testid="stBaseButton-primary"] {
        min-height: 3.6rem !important;
        font-size: 1.08rem !important;
        letter-spacing: 0.08em !important;
        box-shadow: 7px 7px 0 #111111 !important;
    }

    /* ===== MOVIE CARD (search results) ===== */
    .movie-card {
        background: var(--paper);
        border-radius: 4px;
        padding: 1rem;
        margin-bottom: 0.6rem;
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
            padding-top: 8.2rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            padding-bottom: 2.2rem;
        }
        h1 { font-size: 1.6rem !important; }
        .store-sign { font-size: 1rem; padding: 0.65rem 0.85rem; }
        .stat-value { font-size: 1.9rem; }
        .stat-cards-row { gap: 10px; }
        .app-header {
            height: 68px;
            padding: 0 1rem;
        }
        .app-header-logo { font-size: 1.6rem; }
        [data-testid="stVerticalBlock"]:has(.top-nav-widget-anchor) {
            top: 68px;
            padding: 0.45rem 0.6rem 0.6rem;
        }
        [data-testid="stVerticalBlock"]:has(.top-nav-widget-anchor) [data-baseweb="button-group"] {
            gap: 6px;
        }
        [data-testid="stVerticalBlock"]:has(.top-nav-widget-anchor) [data-baseweb="button-group"] > button {
            min-height: 48px;
            font-size: 0.7rem;
        }
        .pick-kicker,
        .pick-result-kicker {
            font-size: 0.74rem;
            padding: 0.48rem 0.7rem;
            box-shadow: 4px 4px 0 #111111;
        }
        .pick-title { margin-top: 0.8rem; }
        .pick-lead { font-size: 0.97rem; }
        [data-testid="stVerticalBlock"]:has(.pick-filter-panel-anchor),
        [data-testid="stVerticalBlock"]:has(.pick-result-anchor),
        [data-testid="stVerticalBlock"]:has(.pick-reveal-anchor) {
            box-shadow: 7px 7px 0 #2c69d8;
            padding: 1rem 0.95rem;
        }
        .pick-results-card {
            position: static;
            top: auto;
            box-shadow: 7px 7px 0 #111111;
        }
        .pick-results-count {
            font-size: 1.55rem;
        }

        /* Shelf row: 2-col flex layout */
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
        .block-container { max-width: 980px; padding-top: 8.9rem; }
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
