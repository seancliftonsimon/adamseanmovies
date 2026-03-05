import streamlit as st

POSTER_PLACEHOLDER = "https://via.placeholder.com/185x278/1a1a1a/C62828?text=No+Poster"


def inject_css():
    st.markdown("""
    <style>
    /* ===== GLOBAL ===== */
    .block-container {
        max-width: 520px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0D0D0D;
    }
    [data-testid="stApp"] {
        background-color: #0D0D0D;
    }

    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -0.01em;
    }
    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.25rem !important; }
    h3 { font-size: 1.1rem !important; }

    /* ===== HIDE CHROME ===== */
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A0000 0%, #0D0D0D 100%);
        border-right: 1px solid #2A0A0A;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: #FAFAFA;
    }

    /* ===== SECTION HEADER BAR ===== */
    .section-header {
        background: linear-gradient(135deg, #8B0000 0%, #C62828 100%);
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 1rem;
        color: #FFFFFF;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    /* ===== MOVIE CARD ===== */
    .movie-card {
        background: #1A1A1A;
        border-radius: 10px;
        padding: 0.85rem;
        margin-bottom: 0.6rem;
        border: 1px solid #2A2A2A;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .movie-card:hover {
        border-color: #C62828;
        box-shadow: 0 0 12px rgba(198, 40, 40, 0.15);
    }
    .movie-card img {
        border-radius: 6px;
        width: 100%;
        max-width: 185px;
    }

    /* ===== GENRE PILLS ===== */
    .genre-pill {
        display: inline-block;
        background: #2A0A0A;
        color: #FF6B6B;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        margin: 2px 3px 2px 0;
        font-weight: 600;
        border: 1px solid #3D1111;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* ===== STAR RATINGS ===== */
    .stars {
        color: #C62828;
        font-size: 1rem;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* ===== PICKER CARD ===== */
    .picker-card {
        background: #1A1A1A;
        border: 2px solid #C62828;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 0 20px rgba(198, 40, 40, 0.1);
    }
    .picker-card img {
        border-radius: 8px;
        max-height: 350px;
        margin-bottom: 0.5rem;
    }

    /* ===== BUTTONS ===== */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #333;
        transition: all 0.2s;
    }
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #8B0000 0%, #C62828 100%);
        color: #FFFFFF;
        border: none;
        font-size: 1rem;
        padding: 0.65rem 1.5rem;
        border-radius: 8px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        box-shadow: 0 2px 8px rgba(198, 40, 40, 0.25);
    }
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #C62828 0%, #E53935 100%);
        box-shadow: 0 4px 16px rgba(198, 40, 40, 0.35);
    }
    div.stButton > button[kind="secondary"],
    div.stButton > button[data-testid="stBaseButton-secondary"] {
        background: #1A1A1A;
        color: #FAFAFA;
        border: 1px solid #C62828;
    }
    div.stButton > button[kind="secondary"]:hover,
    div.stButton > button[data-testid="stBaseButton-secondary"]:hover {
        background: #2A0A0A;
        border-color: #E53935;
    }

    /* ===== STAT / METRIC CARDS ===== */
    [data-testid="stMetric"] {
        background: #1A1A1A;
        border: 1px solid #2A2A2A;
        border-radius: 10px;
        padding: 0.75rem;
        border-left: 3px solid #C62828;
    }
    [data-testid="stMetric"] label {
        color: #999 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #FAFAFA !important;
        font-weight: 700 !important;
    }

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #1A1A1A;
        border-radius: 10px;
        padding: 4px;
        border: 1px solid #2A2A2A;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 0.85rem;
        color: #999;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B0000, #C62828) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ===== EXPANDER ===== */
    [data-testid="stExpander"] {
        background: #1A1A1A;
        border: 1px solid #2A2A2A;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    [data-testid="stExpander"]:hover {
        border-color: #C62828;
    }
    [data-testid="stExpander"] summary {
        font-weight: 600;
    }

    /* ===== TEXT INPUT ===== */
    [data-testid="stTextInput"] input {
        background: #1A1A1A;
        border: 1px solid #333;
        border-radius: 8px;
        color: #FAFAFA;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #C62828;
        box-shadow: 0 0 0 1px #C62828;
    }

    /* ===== TEXT AREA ===== */
    [data-testid="stTextArea"] textarea {
        background: #1A1A1A;
        border: 1px solid #333;
        border-radius: 8px;
        color: #FAFAFA;
    }
    [data-testid="stTextArea"] textarea:focus {
        border-color: #C62828;
        box-shadow: 0 0 0 1px #C62828;
    }

    /* ===== SELECT BOX ===== */
    [data-testid="stSelectbox"] > div > div {
        background: #1A1A1A;
        border: 1px solid #333;
        border-radius: 8px;
    }

    /* ===== SLIDER ===== */
    [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
        background: #C62828;
    }

    /* ===== DIVIDER ===== */
    [data-testid="stHorizontalRule"] {
        border-color: #2A2A2A;
    }

    /* ===== TOAST ===== */
    [data-testid="stToast"] {
        background: #1A1A1A;
        border: 1px solid #C62828;
        border-radius: 10px;
    }

    /* ===== RADIO ===== */
    [data-testid="stRadio"] label span {
        font-weight: 500;
    }

    /* ===== PROGRESS / SUCCESS BAR ===== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #2E7D32, #4CAF50);
    }

    /* ===== IMAGE STYLING ===== */
    [data-testid="stImage"] img {
        border-radius: 6px;
    }

    /* ===== CAPTION / SECONDARY TEXT ===== */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #888 !important;
    }

    /* ===== ALERT BOXES ===== */
    [data-testid="stAlert"] {
        border-radius: 8px;
        border: none;
    }

    /* ===== NAVIGATION ===== */
    nav[data-testid="stSidebarNav"] a {
        border-radius: 8px;
        font-weight: 500;
        padding: 0.5rem 0.75rem;
        transition: background 0.2s;
    }
    nav[data-testid="stSidebarNav"] a:hover {
        background: #2A0A0A;
    }
    nav[data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(135deg, #8B0000, #C62828);
        color: #FFFFFF;
    }

    /* ===== MOBILE-FIRST ===== */
    @media (max-width: 640px) {
        .block-container {
            max-width: 100%;
            padding-top: 0.5rem;
            padding-left: 0.75rem;
            padding-right: 0.75rem;
        }
        div.stButton > button {
            width: 100%;
            padding: 0.7rem 1rem;
            font-size: 0.9rem;
        }
        h1 { font-size: 1.3rem !important; }
        h2 { font-size: 1.1rem !important; }
        [data-testid="stMetric"] {
            padding: 0.5rem;
        }
        .movie-card {
            padding: 0.65rem;
        }
        .genre-pill {
            font-size: 0.65rem;
            padding: 2px 7px;
        }
    }

    /* ===== WIDE SCREENS ===== */
    @media (min-width: 641px) {
        .block-container {
            max-width: 720px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def section_header(text):
    st.markdown(f'<div class="section-header">{text}</div>',
                unsafe_allow_html=True)


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
