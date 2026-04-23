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
        /* Color tokens */
        --color-ink: #111111;
        --color-ink-soft: #1a1a1a;
        --color-ink-muted: #444653;
        --color-outline: #747684;
        --color-royal: #003399;
        --color-royal-shadow: #2c69d8;
        --color-royal-deep: #002068;
        --color-pop-yellow: #F2E400;
        --color-pop-gold: #F2C900;
        --color-paper: #fffcf3;
        --color-paper-warm: #f7f3e8;
        --color-white: #ffffff;
        --color-off-white: #fffef6;
        --color-warning: #fff6bf;

        /* Type scale */
        --font-display: 'Epilogue', sans-serif;
        --font-label: 'Space Grotesk', sans-serif;
        --font-body: 'Inter', sans-serif;
        --type-xs: 0.62rem;
        --type-sm: 0.78rem;
        --type-md: 1rem;
        --type-lg: 1.25rem;
        --type-xl: 1.5rem;
        --type-2xl: 2rem;

        /* Spacing */
        --space-unit: 8px;
        --space-0-5: calc(var(--space-unit) * 0.5);
        --space-0-75: calc(var(--space-unit) * 0.75);
        --space-1: var(--space-unit);
        --space-1-5: calc(var(--space-unit) * 1.5);
        --space-2: calc(var(--space-unit) * 2);
        --space-3: calc(var(--space-unit) * 3);
        --space-4: calc(var(--space-unit) * 4);

        /* Borders + radius */
        --border-thin: 1px;
        --border-base: 2px;
        --border-strong: 3px;
        --border-heavy: 4px;
        --radius-xs: 2px;
        --radius-sm: 4px;
        --radius-md: 6px;
        --radius-pill: 999px;

        /* Shadows */
        --shadow-offset-sm-x: 3px;
        --shadow-offset-sm-y: 3px;
        --shadow-offset-md-x: 4px;
        --shadow-offset-md-y: 4px;
        --shadow-offset-lg-x: 6px;
        --shadow-offset-lg-y: 6px;
        --hard-shadow-sm: var(--shadow-offset-sm-x) var(--shadow-offset-sm-y) 0 var(--color-ink-soft);
        --hard-shadow-md: var(--shadow-offset-md-x) var(--shadow-offset-md-y) 0 var(--color-ink-soft);
        --hard-shadow-lg: var(--shadow-offset-lg-x) var(--shadow-offset-lg-y) 0 var(--color-ink-soft);
        --focus-ring: 0 0 0 var(--border-strong) var(--color-pop-yellow);

        /* Layers */
        --z-base: 1;
        --z-nav: 900;
        --z-header: 950;
        --z-overlay: 999;

        /* Backwards-compatible aliases */
        --ink: var(--color-ink-soft);
        --royal: var(--color-royal);
        --pop-yellow: var(--color-pop-yellow);
        --paper: var(--color-paper);
        --panel-shadow: var(--color-royal-shadow);
        --hard-shadow: var(--hard-shadow-md);
    }

    /* ===== BASE ===== */
    .block-container {
        max-width: 980px;
        padding-top: 6.2rem;   /* clears combined fixed header/nav */
        padding-bottom: 2.2rem;
        font-family: var(--font-body);
        font-size: 1rem;
    }
    html, body {
        overflow-x: hidden;
        overflow-y: auto !important;
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {
        background:
            radial-gradient(circle at top right, rgba(0, 51, 153, 0.05), transparent 22%),
            linear-gradient(180deg, var(--color-paper-warm) 0%, #f6f2e8 100%);
        overflow-x: hidden !important;
        overflow-y: auto !important;
    }
    [data-testid="stAppViewContainer"] > .main,
    [data-testid="stAppViewContainer"] [data-testid="stMain"] {
        overflow-y: visible !important;
    }

    /* ===== HIDE STREAMLIT CHROME ===== */
    #MainMenu, header, footer { display: none !important; }

    /* ===== TYPOGRAPHY ROLES ===== */
    h1, h2, h3 {
        font-family: var(--font-display) !important;
        font-weight: 900 !important;
        color: var(--color-ink-soft) !important;
        letter-spacing: -0.02em !important;
    }
    h1 { font-size: var(--type-2xl) !important; letter-spacing: -0.03em !important; }
    h2 { font-size: var(--type-xl) !important; }
    h3 { font-size: 1.2rem !important; }
    p, li { font-family: var(--font-body); color: var(--color-ink-soft); font-size: var(--type-md); }

    /* ===== NAV ===== */
    .app-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: var(--z-header);
        background: var(--color-royal-shadow);
        border-bottom: var(--border-heavy) solid var(--color-ink);
        box-shadow: 0 var(--shadow-offset-md-y) 0 var(--color-pop-gold);
        height: 74px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 1.6rem;
        gap: 0.9rem;
        box-sizing: border-box;
    }
    .app-header-main {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        min-width: 0;
        flex-shrink: 0;
    }
    .app-header-logo {
        font-family: var(--font-display);
        font-weight: 900;
        font-style: italic;
        font-size: 2rem;
        color: #FFD51F;
        text-transform: uppercase;
        letter-spacing: -0.05em;
        text-shadow: 2px 2px 0 var(--color-ink);
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
        font-family: var(--font-label);
        font-size: 0.7rem;
        font-weight: 700;
        color: rgba(255,255,255,0.75);
        text-transform: uppercase;
        letter-spacing: 0.18em;
        line-height: 1;
    }
    .app-header-nav {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, auto));
        gap: var(--space-1);
        align-items: center;
        justify-content: end;
    }
    .top-nav-link {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.32rem;
        min-height: 38px;
        padding: 0.28rem 0.72rem;
        border-radius: var(--radius-sm);
        border: var(--border-base) solid var(--color-ink-soft);
        background: #fff9db;
        color: var(--color-ink-soft);
        box-shadow: 4px 4px 0 rgba(0,51,153,0.18);
        font-family: var(--font-display);
        font-weight: 800;
        font-size: 0.72rem;
        letter-spacing: 0.06em;
        line-height: 1;
        text-transform: uppercase;
        text-decoration: none;
        text-align: center;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
    }
    .top-nav-icon {
        font-size: 0.88rem;
        line-height: 1;
    }
    .top-nav-text {
        margin-top: 0;
    }
    .top-nav-link:hover {
        transform: translate(-1px, -1px);
        box-shadow: 5px 5px 0 var(--color-ink-soft);
        color: var(--color-ink-soft);
    }
    .top-nav-link.is-active {
        background: var(--color-royal);
        color: var(--color-pop-yellow);
        box-shadow: var(--hard-shadow-md);
    }

    /* ===== PANEL SHELL ===== */
    .layer-panel {
        background: var(--color-paper);
        border: var(--border-strong) solid var(--color-ink);
        border-radius: var(--radius-md);
        box-shadow: 8px 8px 0 var(--color-royal-shadow);
    }
    .layer-shell-title {
        font-family: var(--font-label);
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    .layer-card {
        background: var(--color-white);
        border: var(--border-base) solid var(--color-ink-soft);
        border-radius: var(--radius-sm);
        box-shadow: var(--hard-shadow-sm);
    }

    .page-intro {
        margin-bottom: var(--space-3);
    }
    .page-intro-kicker {
        display: inline-flex;
        align-items: center;
        gap: var(--space-0-5);
        background: var(--color-royal);
        color: var(--color-pop-yellow);
        border: var(--border-base) solid var(--color-ink-soft);
        box-shadow: var(--hard-shadow-sm);
        border-radius: var(--radius-sm);
        padding: var(--space-0-75) var(--space-1-5);
        font-family: var(--font-label);
        font-size: var(--type-sm);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
    .page-intro-title {
        margin: var(--space-1) 0 var(--space-1);
        font-family: var(--font-display);
        font-size: clamp(2rem, 6vw, 3.7rem);
        line-height: 0.95;
        text-transform: uppercase;
        font-style: italic;
        letter-spacing: -0.04em;
        color: var(--color-royal);
    }
    .page-intro-support {
        margin: 0;
        max-width: 44rem;
        color: #4f5a70;
        font-family: var(--font-body);
        line-height: 1.55;
    }

    .panel-shell {
        background: var(--color-paper);
        border: var(--border-strong) solid var(--color-ink-soft);
        box-shadow: 8px 8px 0 var(--color-royal-shadow);
        border-radius: var(--radius-md);
        padding: var(--space-2);
        margin-bottom: var(--space-2);
    }
    .panel-shell-tight { padding: var(--space-1-5); }
    .panel-kicker {
        margin: 0 0 var(--space-1);
        font-family: var(--font-label);
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #5d6780;
        font-weight: 700;
    }

    /* ===== CONTROLS ===== */
    [data-testid="stPills"] {
        gap: 6px !important;
    }
    [data-testid="stPills"] > label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        font-size: 0.85rem !important;
        color: var(--color-ink-soft) !important;
    }
    [data-testid="stPills"] button {
        background: #fffdf5 !important;
        color: var(--color-ink-soft) !important;
        border: 2px solid var(--color-ink-soft) !important;
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
        box-shadow: 3px 3px 0 var(--color-ink-soft) !important;
        background: var(--color-white) !important;
        color: var(--color-ink-soft) !important;
    }
    [data-testid="stPills"] button[aria-checked="true"] {
        background: var(--color-royal) !important;
        color: var(--color-pop-yellow) !important;
        border-color: var(--color-ink-soft) !important;
        box-shadow: 4px 4px 0 var(--color-ink-soft) !important;
        transform: none !important;
    }

    /* ===== VHS TAPE CARD ===== */
    .vhs-tape,
    .layer-card-vhs {
        background: var(--color-ink);
        border: 2px solid var(--color-ink-soft);
        border-radius: var(--radius-xs);
        box-shadow: 3px 3px 0 var(--color-ink-soft);
        overflow: hidden;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
        margin-bottom: 2px;
    }
    .vhs-tape:hover,
    .layer-card-vhs:hover {
        transform: translate(-2px, -2px);
        box-shadow: 5px 5px 0 var(--color-ink-soft);
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
        background: var(--color-pop-yellow);
        color: var(--color-ink-soft);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.48rem;
        font-weight: 700;
        padding: 2px 5px;
        border: 1px solid var(--color-ink-soft);
        box-shadow: 1px 1px 0 var(--color-ink-soft);
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
        background: var(--color-white);
        border-top: 2px solid var(--color-ink-soft);
        padding: 5px 7px 4px;
    }
    .vhs-title {
        display: block;
        font-family: 'Epilogue', sans-serif;
        font-weight: 800;
        font-size: 0.65rem;
        color: var(--color-ink-soft);
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
        background: var(--color-ink-soft);
        margin: 2px 0 10px;
    }

    /* ===== DRAWER ===== */
    .vhs-drawer-header {
        background: var(--color-royal);
        padding: 0.6rem 0.85rem;
        margin-bottom: 0;
        font-family: 'Epilogue', sans-serif;
        font-weight: 800;
        color: var(--color-pop-yellow);
        font-size: 0.95rem;
        letter-spacing: 0.04em;
        border-radius: var(--radius-sm) 4px 0 0;
        text-transform: uppercase;
        border: 2px solid var(--color-ink-soft);
        border-bottom: none;
        box-shadow: 3px 0 0 var(--color-ink-soft), -1px 0 0 var(--color-ink-soft);
    }
    .vhs-drawer-end {
        height: 4px;
        background: var(--color-pop-yellow);
        border: 2px solid var(--color-ink-soft);
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
    .stat-card-yellow { background: var(--color-pop-yellow); }
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
    .stat-card-yellow .stat-label { color: var(--color-ink-soft); opacity: 0.7; }
    .stat-value {
        font-family: 'Epilogue', sans-serif;
        font-weight: 900;
        font-size: 2.4rem;
        color: #002068;
        line-height: 1;
        letter-spacing: -0.04em;
        margin: 0 0 4px;
    }
    .stat-card-yellow .stat-value { color: var(--color-ink-soft); }
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
    .store-sign,
    .section-shell-title {
        background: var(--royal);
        color: var(--pop-yellow);
        padding: 0.85rem 1.1rem;
        border-radius: var(--radius-sm);
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
        background: var(--color-ink-soft);
        color: var(--color-pop-yellow);
        padding: 3px 10px;
        border-radius: 20px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.72rem;
        margin: 2px 3px 2px 0;
        font-weight: 700;
        border: 1.5px solid var(--color-ink-soft);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* ===== STAR RATINGS ===== */
    .stars {
        color: var(--color-pop-yellow);
        font-size: 1.1rem;
        letter-spacing: 1px;
        font-weight: 700;
        -webkit-text-stroke: 0.5px var(--color-ink-soft);
    }

    /* ===== BUTTONS (global) ===== */
    div.stButton > button {
        background: var(--paper);
        color: var(--ink);
        border: 2px solid var(--ink);
        border-radius: var(--radius-sm);
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
        box-shadow: 4px 4px 0 var(--color-ink-soft);
        border-color: var(--color-ink-soft);
        background: var(--color-white);
        color: var(--color-ink-soft);
    }
    div.stButton > button:active {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0 var(--color-ink-soft);
    }
    div.stButton > button:focus-visible,
    [data-baseweb="button-group"] > button:focus-visible,
    [data-testid="stPills"] button:focus-visible,
    [data-testid="stExpander"] summary:focus-visible,
    [data-testid="stSelectbox"] [role="combobox"]:focus-visible,
    [data-testid="stTextInput"] input:focus-visible,
    [data-testid="stTextArea"] textarea:focus-visible {
        outline: none !important;
        box-shadow: var(--focus-ring) !important;
    }
    div.stButton > button:disabled,
    [data-baseweb="button-group"] > button:disabled,
    [data-testid="stPills"] button:disabled,
    [data-testid="stExpander"] summary[aria-disabled="true"] {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="stBaseButton-primary"] {
        background: var(--color-pop-yellow) !important;
        color: var(--color-ink-soft) !important;
        border: 2px solid var(--color-ink-soft);
        font-family: 'Epilogue', sans-serif;
        font-weight: 800;
        font-size: 0.9rem;
        padding: 0.6rem 1rem;
        border-radius: var(--radius-sm);
        box-shadow: 4px 4px 0 var(--color-ink-soft);
    }
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: var(--color-pop-yellow) !important;
        color: var(--color-ink-soft) !important;
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0 var(--color-ink-soft);
    }
    div.stButton > button[kind="primary"]:active,
    div.stButton > button[data-testid="stBaseButton-primary"]:active {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0 var(--color-ink-soft);
    }

    /* ===== METRIC CARDS ===== */
    [data-testid="stMetric"] {
        background: var(--color-white);
        border: 2px solid var(--color-ink-soft);
        border-radius: var(--radius-sm);
        padding: 0.85rem;
        box-shadow: 3px 3px 0 var(--color-ink-soft);
    }
    [data-testid="stMetric"] label {
        color: #444444 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--color-royal) !important;
        font-family: 'Epilogue', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.8rem !important;
    }

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #e2e2e2;
        border-radius: var(--radius-sm);
        padding: 4px;
        border: 2px solid var(--color-ink-soft);
        box-shadow: 3px 3px 0 var(--color-ink-soft);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-xs);
        padding: var(--space-1) var(--space-2);
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.82rem;
        color: #444444;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stTabs [aria-selected="true"] {
        background: var(--color-royal) !important;
        color: var(--color-pop-yellow) !important;
        border-radius: var(--radius-xs) !important;
        box-shadow: 2px 2px 0 var(--color-ink-soft) !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* ===== EXPANDER ===== */
    [data-testid="stExpander"] {
        background: var(--color-white);
        border: 2px solid var(--color-ink-soft) !important;
        border-radius: var(--radius-sm);
        margin-bottom: 0.6rem;
        box-shadow: 3px 3px 0 var(--color-ink-soft);
    }
    [data-testid="stExpander"]:hover { box-shadow: 4px 4px 0 var(--color-ink-soft); }
    [data-testid="stExpander"] summary {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.85rem;
        color: var(--color-ink-soft);
        padding: 0.75rem 1rem;
    }

    /* ===== TEXT INPUT ===== */
    [data-testid="stTextInput"] input {
        background: var(--color-white);
        border: 2px solid var(--color-ink-soft);
        border-radius: var(--radius-sm);
        color: var(--color-ink-soft);
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        padding: 0.6rem 0.75rem;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: var(--color-royal);
        box-shadow: var(--focus-ring);
    }
    [data-testid="stTextInput"] label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 0.82rem !important;
        color: var(--color-ink-soft) !important;
    }

    /* ===== TEXT AREA ===== */
    [data-testid="stTextArea"] textarea {
        background: var(--color-white);
        border: 2px solid var(--color-ink-soft);
        border-radius: var(--radius-sm);
        color: var(--color-ink-soft);
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
    }
    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--color-royal);
        box-shadow: var(--focus-ring);
    }
    [data-testid="stTextArea"] label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 0.82rem !important;
        color: var(--color-ink-soft) !important;
    }

    /* ===== SELECT BOX ===== */
    [data-testid="stSelectbox"] > div > div {
        background: var(--color-white);
        border: 2px solid var(--color-ink-soft);
        border-radius: var(--radius-sm);
        color: var(--color-ink-soft);
        font-size: 1rem;
    }
    [data-testid="stSelectbox"] label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 0.82rem !important;
        color: var(--color-ink-soft) !important;
    }

    /* ===== RADIO BUTTONS ===== */
    [data-testid="stRadio"] label {
        color: var(--color-ink-soft) !important;
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
        background-color: var(--color-royal) !important;
        border-color: var(--color-royal) !important;
    }

    /* ===== SLIDER ===== */
    [data-testid="stSlider"] > label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        font-size: 0.82rem !important;
        color: var(--color-ink-soft) !important;
    }
    [data-testid="stSlider"] [data-testid="stTickBar"] span,
    [data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
        color: var(--color-ink-soft) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
    }

    /* ===== DIVIDER ===== */
    [data-testid="stHorizontalRule"] { border-color: var(--color-ink-soft); border-width: 2px; }

    /* ===== IMAGE ===== */
    [data-testid="stImage"] img {
        border-radius: var(--radius-xs);
        border: 2px solid var(--color-ink-soft);
        box-shadow: 3px 3px 0 var(--color-ink-soft);
    }

    /* ===== CAPTION ===== */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #444653 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
    }

    /* ===== FEEDBACK STATES ===== */
    [data-testid="stAlert"] {
        border-radius: var(--radius-sm);
        border: 2px solid var(--color-ink-soft) !important;
        box-shadow: 3px 3px 0 var(--color-ink-soft);
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
    }

    .workflow-label {
        margin: 0 0 0.2rem;
        font-family: var(--font-label);
        font-size: var(--type-sm);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #677089;
    }

    .app-empty-state {
        display: grid;
        gap: var(--space-1);
        background: #fffef8;
        border: var(--border-base) dashed var(--color-outline);
        border-radius: var(--radius-sm);
        padding: var(--space-2);
        margin: 0 0 var(--space-1);
    }
    .app-empty-title {
        margin: 0;
        font-family: var(--font-display);
        font-size: var(--type-lg);
        letter-spacing: -0.02em;
        color: var(--color-ink-soft);
    }
    .app-empty-copy {
        margin: 0;
        font-family: var(--font-body);
        color: #4f5a70;
    }

    .result-summary {
        display: grid;
        gap: var(--space-1);
        margin-bottom: var(--space-1-5);
    }
    .result-summary-count {
        margin: 0;
        font-family: var(--font-display);
        font-size: clamp(1.4rem, 3vw, 2.1rem);
        font-weight: 900;
        letter-spacing: -0.03em;
        color: var(--color-royal);
        text-transform: uppercase;
        line-height: 0.98;
    }
    .result-summary-copy {
        margin: 0;
        font-family: var(--font-label);
        font-size: var(--type-sm);
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #59647c;
    }

    /* ===== PICKER CARD ===== */
    .picker-card {
        background: var(--color-royal);
        border: 2px solid var(--color-ink-soft);
        border-radius: var(--radius-md);
        padding: 1.75rem 1.5rem;
        text-align: center;
        box-shadow: 6px 6px 0 var(--color-ink-soft);
        color: var(--color-white);
    }

    /* ===== PICK PAGE ===== */
    .pick-page-anchor,
    .pick-filters-card-anchor,
    .pick-results-card-anchor,
    .pick-result-anchor,
    .pick-reveal-anchor {
        display: none;
    }

    .pick-kicker,
    .pick-result-kicker {
        display: inline-block;
        background: var(--color-royal);
        color: var(--color-white);
        border: var(--border-strong) solid var(--color-ink);
        box-shadow: 5px 5px 0 var(--color-ink);
        padding: 0.55rem 0.95rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }

    .pick-title {
        margin: 0.45rem 0 0.35rem;
        font-family: 'Epilogue', sans-serif;
        font-size: clamp(2.75rem, 8vw, 4.9rem);
        line-height: 0.92;
        font-style: italic;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -0.06em;
        color: var(--color-royal);
    }

    .pick-lead {
        margin: 0;
        max-width: 42rem;
        color: #586273;
        font-size: 1.05rem;
        line-height: 1.55;
    }

    [data-testid="stVerticalBlock"]:has(.add-workflow-anchor) {
        background: rgba(255, 252, 243, 0.98);
        border: var(--border-strong) solid var(--color-ink);
        border-radius: var(--radius-md);
        box-shadow: 8px 8px 0 var(--color-royal-shadow);
        padding: var(--space-2);
        margin-bottom: var(--space-2);
        gap: var(--space-2);
    }
    [data-testid="stVerticalBlock"]:has(.add-workflow-anchor) [data-testid="stPills"] {
        margin-bottom: 0.2rem;
    }
    [data-testid="stVerticalBlock"]:has(.add-workflow-anchor) [data-testid="stPills"] [role="radiogroup"],
    [data-testid="stVerticalBlock"]:has(.add-workflow-anchor) [data-testid="stPills"] [role="group"] {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
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

    .pick-active-filters {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.8rem;
    }

    .pick-results-count {
        font-family: 'Epilogue', sans-serif;
        color: var(--color-royal);
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
        border: 2px solid var(--color-ink);
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
        border: 2px solid var(--color-ink);
        border-radius: 999px;
        padding: 0.38rem 0.72rem;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--color-ink-soft);
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
        color: var(--color-royal);
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
        border: var(--border-strong) solid var(--color-ink);
        border-radius: var(--radius-md);
        box-shadow: 10px 10px 0 var(--panel-shadow);
        padding: 1.45rem clamp(1rem, 2.4vw, 2rem);
        margin-bottom: 1.6rem;
        gap: 1rem;
    }

    [data-testid="stVerticalBlock"]:has(.pick-filters-card-anchor) {
        background: var(--color-paper);
        border: var(--border-strong) solid var(--color-ink-soft);
        box-shadow: 6px 6px 0 var(--color-royal-shadow);
        border-radius: var(--radius-md);
        padding: var(--space-1-5);
        margin-bottom: var(--space-1-5);
        gap: var(--space-1);
    }

    [data-testid="stVerticalBlock"]:has(.pick-results-card-anchor) {
        background: #fffef6;
        border: var(--border-strong) solid var(--color-ink);
        box-shadow: 10px 10px 0 var(--color-ink);
        border-radius: var(--radius-md);
        padding: 1rem;
        position: sticky;
        top: 142px;
        gap: 0.75rem;
    }

    [data-testid="stVerticalBlock"]:has(.pick-result-anchor) [data-testid="stHorizontalBlock"] {
        align-items: start;
    }

    [data-testid="stVerticalBlock"]:has(.pick-result-anchor) [data-testid="stImage"] img,
    [data-testid="stVerticalBlock"]:has(.pick-reveal-anchor) [data-testid="stImage"] img {
        box-shadow: 7px 7px 0 var(--color-ink);
    }

    [data-testid="stVerticalBlock"]:has(.pick-page-anchor) .page-intro {
        margin-bottom: var(--space-1-5);
    }
    [data-testid="stVerticalBlock"]:has(.pick-page-anchor) .page-intro-title {
        margin-top: 0;
    }
    [data-testid="stVerticalBlock"]:has(.pick-filters-card-anchor) [data-testid="stPills"] {
        margin-bottom: 0.2rem;
    }
    [data-testid="stVerticalBlock"]:has(.pick-filters-card-anchor) [data-testid="stPills"] [role="radiogroup"],
    [data-testid="stVerticalBlock"]:has(.pick-filters-card-anchor) [data-testid="stPills"] [role="group"] {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    [data-testid="stVerticalBlock"]:has(.pick-results-card-anchor) div.stButton > button[kind="primary"],
    [data-testid="stVerticalBlock"]:has(.pick-results-card-anchor) div.stButton > button[data-testid="stBaseButton-primary"] {
        min-height: 3.6rem !important;
        font-size: 1.08rem !important;
        letter-spacing: 0.08em !important;
        box-shadow: 7px 7px 0 var(--color-ink) !important;
    }

    /* ===== MOVIE CARD (search results) ===== */
    .movie-card {
        background: var(--paper);
        border-radius: var(--radius-sm);
        padding: 1rem;
        margin-bottom: 0.6rem;
        border: 2px solid var(--color-ink-soft);
        box-shadow: 3px 3px 0 var(--color-ink-soft);
        transition: transform 0.1s, box-shadow 0.1s;
    }
    .movie-card:hover {
        transform: translate(-1px, -1px);
        box-shadow: 4px 4px 0 var(--color-ink-soft);
    }
    .movie-card img {
        border-radius: var(--radius-xs);
        width: 100%;
        max-width: 185px;
        border: 1px solid var(--color-ink-soft);
    }

    /* ===== SIDEBAR (fallback) ===== */
    [data-testid="stSidebar"] {
        background: var(--color-royal);
        border-right: 3px solid var(--color-ink-soft);
    }
    [data-testid="stSidebar"] * { color: var(--color-white) !important; }

    /* ===== RESPONSIVE OVERRIDES ===== */
    @media (max-width: 640px) {
        .block-container {
            width: 100vw !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
            overflow-x: clip !important;
            padding-top: 6.8rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            padding-bottom: 2.2rem;
        }
        h1 { font-size: 1.6rem !important; }
        .store-sign { font-size: 1rem; padding: 0.65rem 0.85rem; }
        .stat-value { font-size: 1.9rem; }
        .stat-cards-row { gap: 10px; }
        .app-header {
            height: 84px;
            padding: 0.65rem 0.85rem;
            align-items: flex-start;
        }
        .app-header-main {
            gap: 0.55rem;
        }
        .app-header-logo { font-size: 1.45rem; }
        .app-header-sep,
        .app-header-tagline {
            display: none;
        }
        .app-header-nav {
            gap: 0.35rem;
            align-self: center;
        }
        .top-nav-link {
            min-height: 34px;
            padding: 0.22rem 0.45rem;
            font-size: 0.64rem;
            letter-spacing: 0.05em;
            box-shadow: 3px 3px 0 rgba(0,51,153,0.18);
        }
        .top-nav-icon { font-size: 0.72rem; }
        .pick-kicker,
        .pick-result-kicker {
            font-size: 0.74rem;
            padding: 0.48rem 0.7rem;
            box-shadow: 4px 4px 0 var(--color-ink);
        }
        .pick-title { margin-top: 0.8rem; }
        .pick-lead { font-size: 0.97rem; }
        [data-testid="stVerticalBlock"]:has(.pick-result-anchor),
        [data-testid="stVerticalBlock"]:has(.pick-reveal-anchor) {
            box-shadow: 7px 7px 0 #2c69d8;
            padding: 1rem 0.95rem;
        }
        [data-testid="stVerticalBlock"]:has(.pick-results-card-anchor) {
            position: static;
            top: auto;
            box-shadow: 7px 7px 0 var(--color-ink);
        }
        .pick-results-count {
            font-size: 1.55rem;
        }
        .page-intro-title {
            font-size: clamp(1.8rem, 9vw, 2.8rem);
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
        .block-container { max-width: 980px; padding-top: 6.2rem; }
        .stat-cards-row { grid-template-columns: repeat(4, 1fr); }
    }
    </style>
    """, unsafe_allow_html=True)


# ── Layout HTML helpers ──────────────────────────────────────────────

def app_header_html(nav_links_html=""):
    """Sticky top header bar."""
    return (
        '<div class="app-header">'
        '<div class="app-header-main">'
        '<div class="app-header-logo">📼 Adam &amp; Sean</div>'
        '<div class="app-header-sep"></div>'
        '<div class="app-header-tagline">Movie Vault</div>'
        '</div>'
        '<nav class="app-header-nav" aria-label="Primary">'
        f'{nav_links_html}'
        '</nav>'
        '</div>'
    )


# ── Content HTML helpers ──────────────────────────────────────────────

def section_header(text):
    st.markdown(f'<div class="store-sign section-shell-title layer-shell-title">{escape(text)}</div>',
                unsafe_allow_html=True)


def page_intro_html(kicker, title, support=None):
    kicker_html = (
        f'<div class="page-intro-kicker">{escape(kicker)}</div>'
        if kicker else ""
    )
    support_html = (
        f'<p class="page-intro-support">{escape(support)}</p>'
        if support else ""
    )
    return (
        '<section class="page-intro">'
        f'{kicker_html}'
        f'<h1 class="page-intro-title">{escape(title)}</h1>'
        f'{support_html}'
        '</section>'
    )


def panel_start_html(panel_label=None, tight=False):
    klass = "panel-shell panel-shell-tight" if tight else "panel-shell"
    kicker_html = (
        f'<p class="panel-kicker">{escape(panel_label)}</p>'
        if panel_label else ""
    )
    return f'<section class="{klass}">{kicker_html}'


def panel_end_html():
    return "</section>"


def workflow_label_html(text):
    return f'<p class="workflow-label">{escape(text)}</p>'


def empty_state_html(title, copy=None):
    copy_html = f'<p class="app-empty-copy">{escape(copy)}</p>' if copy else ""
    return (
        '<div class="app-empty-state">'
        f'<h3 class="app-empty-title">{escape(title)}</h3>'
        f'{copy_html}'
        '</div>'
    )


def result_summary_html(count_text, summary_text=None):
    summary_html = (
        f'<p class="result-summary-copy">{escape(summary_text)}</p>'
        if summary_text else ""
    )
    return (
        '<div class="result-summary">'
        f'<p class="result-summary-count">{escape(count_text)}</p>'
        f'{summary_html}'
        '</div>'
    )


def vhs_tape_html(img_url, title, year=None, badge=None):
    """VHS-style movie card: black image area with white info footer."""
    meta = str(year) if year else ""
    badge_html = (f'<div class="vhs-badge">{escape(badge)}</div>'
                  if badge else "")
    return (
        f'<div class="vhs-tape layer-card-vhs layer-card">'
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
            f'<div class="vhs-tape layer-card-vhs layer-card">'
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
