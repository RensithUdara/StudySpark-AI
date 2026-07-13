import html

import streamlit as st


APP_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

:root {
    --lm-navy: #0b2a5f;
    --lm-blue: #1769e0;
    --lm-blue-2: #2f8cff;
    --lm-blue-soft: #dcecff;
    --lm-sky: #eaf4ff;
    --lm-sky-2: #f5faff;
    --lm-text: #10233f;
    --lm-muted: #5f728f;
    --lm-line: #d7e6fa;
    --lm-white: #ffffff;
    --lm-success: #087f5b;
    --lm-warning: #b45309;
    --lm-danger: #be123c;
}

.stApp,
.stApp > div,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: linear-gradient(180deg, #f7fbff 0%, #eef6ff 42%, #ffffff 100%) !important;
    color: var(--lm-text) !important;
}

.block-container,
[data-testid="stMainBlockContainer"] {
    max-width: 1320px !important;
    padding: 1.75rem 2rem 4rem !important;
}

[data-testid="stStatusWidget"],
[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: linear-gradient(180deg, #ffffff 0%, #f4f9ff 100%) !important;
    border-right: 1px solid #cfe0f7 !important;
    box-shadow: 14px 0 34px rgba(16,35,63,0.09) !important;
}
[data-testid="stSidebar"] * { color: var(--lm-text) !important; }
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] caption,
[data-testid="stSidebar"] .stMarkdown p { color: var(--lm-muted) !important; }
[data-testid="stSidebar"] hr { border-color: var(--lm-line) !important; }
[data-testid="stSidebarNav"] {
    padding: 0.75rem 1rem 1rem !important;
}
[data-testid="stSidebarNav"] ul {
    gap: 0.22rem !important;
    padding: 0 !important;
}
[data-testid="stSidebarNav"] li {
    margin: 0 !important;
}
[data-testid="stSidebarNav"] a {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 12px !important;
    margin: 0.08rem 0 !important;
    min-height: 2.45rem !important;
    padding: 0.48rem 0.65rem !important;
    transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease !important;
    width: 100% !important;
}
[data-testid="stSidebarNav"] a span {
    color: #31425e !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
}
[data-testid="stSidebarNav"] a[aria-selected="true"],
[data-testid="stSidebarNav"] a:hover {
    background: #ffffff !important;
    border-color: #b8d5ff !important;
    box-shadow: 0 10px 22px rgba(23,105,224,0.10) !important;
    transform: translateX(2px) !important;
}
[data-testid="stSidebarNav"] a[aria-selected="true"] span {
    color: var(--lm-blue) !important;
}
[data-testid="stSidebarNav"] a::before,
[data-testid="stSidebarNav"] a::after {
    display: none !important;
}

h1, h2, h3 {
    color: var(--lm-text) !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0 !important;
}
h1 {
    font-size: clamp(2rem, 3vw, 2.75rem) !important;
    font-weight: 800 !important;
    margin: 0 !important;
}
h2 { font-size: 1.45rem !important; font-weight: 800 !important; }
h3 { color: var(--lm-navy) !important; font-size: 1.05rem !important; font-weight: 800 !important; }
h4, strong { color: var(--lm-text) !important; }
p, li { color: #42546f !important; line-height: 1.65; }
a { color: var(--lm-blue) !important; }
label { color: #40516d !important; font-size: 0.88rem !important; font-weight: 700 !important; }
small { color: var(--lm-muted) !important; }
hr {
    border: none !important;
    border-top: 1px solid var(--lm-line) !important;
    margin: 1.1rem 0 !important;
}

[data-testid="stHorizontalBlock"] { gap: 1rem !important; }
[data-testid="stVerticalBlock"] { gap: 0.9rem !important; }

.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background: var(--lm-blue) !important;
    border: 1px solid var(--lm-blue) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 22px rgba(23,105,224,0.18) !important;
    color: #ffffff !important;
    font-size: 0.9rem !important;
    font-weight: 800 !important;
    min-height: 2.55rem !important;
    padding: 0.55rem 1rem !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease !important;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background: #0f5ecb !important;
    box-shadow: 0 14px 28px rgba(23,105,224,0.24) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: #ffffff !important;
    border-color: var(--lm-line) !important;
    box-shadow: 0 8px 18px rgba(16,35,63,0.07) !important;
    color: var(--lm-blue) !important;
}

[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid var(--lm-line) !important;
    border-radius: 14px !important;
    box-shadow: 0 14px 30px rgba(16,35,63,0.08) !important;
    padding: 1rem !important;
}
[data-testid="stMetricLabel"] {
    color: var(--lm-muted) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    color: var(--lm-blue) !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
}

[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 1.5px dashed #9fc5ff !important;
    border-radius: 14px !important;
    box-shadow: 0 14px 30px rgba(16,35,63,0.07) !important;
    padding: 1.1rem !important;
}
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stSelectbox > div > div,
[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #cfe0f7 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    color: var(--lm-text) !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--lm-blue-2) !important;
    box-shadow: 0 0 0 3px rgba(47,140,255,0.16) !important;
}
[data-baseweb="popover"] [role="option"] {
    background: #ffffff !important;
    color: var(--lm-text) !important;
}

.stTabs [data-baseweb="tab-list"] {
    align-items: center !important;
    background: #ffffff !important;
    border: 1px solid #cfe0f7 !important;
    border-radius: 999px !important;
    box-shadow: 0 12px 26px rgba(16,35,63,0.07) !important;
    display: inline-flex !important;
    gap: 0.25rem !important;
    min-height: 3rem !important;
    padding: 0.3rem !important;
    width: auto !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 999px !important;
    color: #4d6383 !important;
    font-size: 0.9rem !important;
    font-weight: 800 !important;
    height: 2.3rem !important;
    line-height: 1 !important;
    padding: 0 1rem !important;
    white-space: nowrap !important;
}
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span {
    color: inherit !important;
    font-weight: 800 !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: var(--lm-sky-2) !important;
    border-color: #d7e6fa !important;
    color: var(--lm-blue) !important;
}
.stTabs [aria-selected="true"] {
    background: var(--lm-blue) !important;
    border-color: var(--lm-blue) !important;
    box-shadow: 0 8px 18px rgba(23,105,224,0.18) !important;
    color: #ffffff !important;
}
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span {
    color: #ffffff !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

.stRadio label {
    background: #ffffff !important;
    border: 1px solid var(--lm-line) !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 18px rgba(16,35,63,0.05) !important;
    padding: 0.55rem 0.75rem !important;
}
.stRadio label:hover {
    background: var(--lm-sky-2) !important;
    border-color: #9fc5ff !important;
}

.stAlert,
[data-testid="stExpander"],
[data-testid="stDataFrame"],
[data-testid="stChatMessage"] {
    border-radius: 8px !important;
    border: 1px solid var(--lm-line) !important;
    box-shadow: 0 10px 22px rgba(16,35,63,0.06) !important;
}
[data-testid="stExpander"] {
    background: #ffffff !important;
}
[data-testid="stExpander"] summary {
    color: var(--lm-blue) !important;
    font-weight: 800 !important;
}
[data-testid="stChatMessage"] {
    background: #ffffff !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stBottom"],
[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] > div {
    background: rgba(247,251,255,0.98) !important;
    border-top: 1px solid var(--lm-line) !important;
}
.stProgress > div > div {
    background: #dbeafe !important;
    border-radius: 999px !important;
}
.stProgress > div > div > div {
    background: var(--lm-blue) !important;
    border-radius: 999px !important;
}

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #9fc5ff; border-radius: 999px; }

.lm-sidebar-brand {
    align-items: center;
    display: flex;
    gap: 0.7rem;
    margin-bottom: 0.25rem;
}
.lm-logo-mark {
    align-items: center;
    background: var(--lm-blue);
    border-radius: 8px;
    color: #ffffff;
    display: inline-flex;
    font-size: 0.95rem;
    font-weight: 800;
    height: 2rem;
    justify-content: center;
    width: 2rem;
}
.lm-brand-text {
    color: var(--lm-navy);
    font-size: 1.2rem;
    font-weight: 800;
}
.lm-sidebar-subtitle {
    color: var(--lm-muted) !important;
    font-size: 0.8rem;
    margin: 0 0 1rem 0;
}
.lm-stat-grid {
    background: var(--lm-sky-2);
    border: 1px solid var(--lm-line);
    border-radius: 14px;
    display: grid;
    gap: 0.5rem;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    padding: 0.75rem;
}
.lm-stat-value {
    color: var(--lm-blue);
    font-size: 1.15rem;
    font-weight: 800;
    text-align: center;
}
.lm-stat-label {
    color: var(--lm-muted);
    font-size: 0.68rem;
    font-weight: 700;
    text-align: center;
}

.page-header {
    background:
        linear-gradient(135deg, rgba(23,105,224,0.98), rgba(47,140,255,0.92)),
        linear-gradient(90deg, rgba(255,255,255,0.2) 1px, transparent 1px);
    border: 1px solid rgba(255,255,255,0.55);
    border-radius: 20px;
    box-shadow: 0 22px 48px rgba(23,105,224,0.22);
    margin-bottom: 1.35rem;
    overflow: hidden;
    padding: 1.9rem 1.8rem 1.65rem;
    position: relative;
}
.page-header::after {
    background:
        linear-gradient(90deg, rgba(255,255,255,0.14) 1px, transparent 1px),
        linear-gradient(180deg, rgba(255,255,255,0.12) 1px, transparent 1px);
    background-size: 40px 40px;
    content: "";
    inset: 0;
    opacity: 0.35;
    pointer-events: none;
    position: absolute;
}
.page-header > * {
    position: relative;
    z-index: 1;
}
.page-header h1 {
    color: #ffffff !important;
    font-size: clamp(2rem, 3.2vw, 2.85rem) !important;
    line-height: 1.2 !important;
    padding-top: 0.05rem !important;
}
.page-header p {
    color: rgba(255,255,255,0.88) !important;
    margin: 0.55rem 0 0;
    max-width: 780px;
}

.hero-section {
    background: linear-gradient(135deg, #0b5bd3 0%, #2f8cff 100%);
    border-radius: 18px;
    box-shadow: 0 20px 42px rgba(23,105,224,0.24);
    margin-bottom: 1.2rem;
    overflow: hidden;
    padding: 2.1rem;
    position: relative;
}
.hero-section::after {
    background:
        linear-gradient(90deg, rgba(255,255,255,0.18) 1px, transparent 1px),
        linear-gradient(180deg, rgba(255,255,255,0.16) 1px, transparent 1px);
    background-size: 42px 42px;
    content: "";
    inset: 0;
    opacity: 0.32;
    pointer-events: none;
    position: absolute;
}
.hero-section > * { position: relative; z-index: 1; }
.hero-section h1 {
    color: #ffffff !important;
    font-size: clamp(2.2rem, 5vw, 3.35rem) !important;
    margin-bottom: 0.6rem !important;
}
.hero-section p {
    color: rgba(255,255,255,0.92) !important;
    font-size: 1.02rem;
    margin: 0 0 1rem;
    max-width: 780px;
}

.pill-row { display: flex; flex-wrap: wrap; gap: 0.55rem; }
.feature-pill,
.kw-pill {
    align-items: center;
    background: #ffffff;
    border: 1px solid #cfe0f7;
    border-radius: 999px;
    color: var(--lm-blue) !important;
    display: inline-flex;
    font-size: 0.82rem;
    font-weight: 800;
    line-height: 1.2;
    margin: 0.15rem;
    padding: 0.42rem 0.72rem;
    white-space: nowrap;
}
.hero-section .feature-pill {
    background: rgba(255,255,255,0.18);
    border-color: rgba(255,255,255,0.38);
    color: #ffffff !important;
}

.premium-card,
.step-card,
.content-card,
.quiz-question,
.review-card {
    background: #ffffff;
    border: 1px solid var(--lm-line);
    border-radius: 16px;
    box-shadow: 0 16px 34px rgba(16,35,63,0.08);
}
.premium-card,
.step-card {
    min-height: 100%;
    padding: 1.15rem;
    transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease;
}
.premium-card:hover,
.step-card:hover {
    border-color: #9fc5ff;
    box-shadow: 0 20px 40px rgba(23,105,224,0.13);
    transform: translateY(-2px);
}
.feature-icon,
.step-icon {
    align-items: center;
    background: var(--lm-sky);
    border: 1px solid #c7ddfb;
    border-radius: 12px;
    color: var(--lm-blue);
    display: inline-flex;
    font-size: 0.9rem;
    font-weight: 800;
    height: 2rem;
    justify-content: center;
    margin-bottom: 0.75rem;
    width: 2rem;
}
.premium-card h3,
.step-card h3 { margin: 0 0 0.45rem !important; }
.premium-card p,
.step-card p {
    color: var(--lm-muted) !important;
    font-size: 0.92rem;
    margin: 0;
}
.step-card { text-align: center; }

.info-strip,
.step-item,
.progress-panel {
    background: #ffffff;
    border: 1px solid var(--lm-line);
    border-radius: 14px;
    box-shadow: 0 14px 28px rgba(16,35,63,0.07);
    color: #344866 !important;
}
.info-strip {
    margin: 0.7rem 0 1rem;
    padding: 0.75rem 0.95rem;
}
.lecture-row {
    align-items: center;
    display: flex;
    gap: 0.45rem;
    margin: 0 !important;
    min-height: 3.1rem;
    padding: 0.75rem 1rem;
}
.lecture-row .lecture-title {
    color: var(--lm-text) !important;
    font-size: 1rem;
    line-height: 1.2;
    white-space: nowrap;
}
.lecture-row small {
    border-left: 1px solid #c7d8ee;
    color: #637795 !important;
    line-height: 1.2;
    padding-left: 0.45rem;
}
.step-item {
    align-items: center;
    display: flex;
    font-size: 0.9rem;
    gap: 0.65rem;
    margin-bottom: 0.45rem;
    padding: 0.7rem 0.9rem;
}
.step-item.active { background: var(--lm-sky); border-color: #9fc5ff; color: var(--lm-blue) !important; }
.step-item.done { background: #edfdf8; border-color: #b8ead7; color: var(--lm-success) !important; }
.step-item.error { background: #fff1f2; border-color: #fecdd3; color: var(--lm-danger) !important; }

.progress-meta {
    color: var(--lm-muted);
    display: flex;
    font-size: 0.9rem;
    gap: 1rem;
    justify-content: space-between;
    margin-bottom: 0.45rem;
}
.progress-track {
    background: #dbeafe;
    border-radius: 999px;
    height: 9px;
    margin-bottom: 1.2rem;
    overflow: hidden;
    width: 100%;
}
.progress-fill {
    background: var(--lm-blue);
    border-radius: 999px;
    height: 100%;
    transition: width 0.25s ease;
}

.flashcard-face {
    align-items: center;
    border-radius: 18px;
    box-shadow: 0 18px 36px rgba(16,35,63,0.09);
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 260px;
    padding: 2rem;
    text-align: center;
    width: 100%;
}
.flashcard-front {
    background: #ffffff;
    border: 1px solid #9fc5ff;
}
.flashcard-back {
    background: var(--lm-sky);
    border: 1px solid #9fc5ff;
}
.fc-label {
    color: var(--lm-blue);
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    margin-bottom: 0.75rem;
}
.fc-text {
    color: var(--lm-text);
    font-size: 1.12rem;
    line-height: 1.65;
}
.muted-hint {
    color: var(--lm-muted) !important;
    font-size: 0.82rem;
    margin-top: 0.55rem;
    text-align: center;
}
.quiz-question,
.review-card {
    margin-bottom: 0.75rem;
    padding: 1rem 1.15rem;
}
.review-card.ok { background: #edfdf8; border-color: #b8ead7; }
.review-card.bad { background: #fff1f2; border-color: #fecdd3; }
.score-badge {
    align-items: center;
    border: 1px solid var(--lm-line);
    border-radius: 999px;
    box-shadow: 0 10px 20px rgba(16,35,63,0.07);
    display: inline-flex;
    font-weight: 800;
    gap: 0.5rem;
    padding: 0.62rem 1.05rem;
}
.score-badge.excellent { background: #edfdf8; border-color: #b8ead7; color: var(--lm-success) !important; }
.score-badge.good { background: var(--lm-sky); border-color: #9fc5ff; color: var(--lm-blue) !important; }
.score-badge.review { background: #fff7ed; border-color: #fed7aa; color: var(--lm-warning) !important; }

/* Strong Streamlit overrides for the page menu/tabs and native panels. */
[data-testid="stTabs"] {
    background: transparent !important;
    margin-top: 0.2rem !important;
}
[data-testid="stTabs"] [data-baseweb="tab-list"],
div[data-baseweb="tab-list"],
[role="tablist"] {
    align-items: center !important;
    background: #ffffff !important;
    border: 1px solid #cfe0f7 !important;
    border-radius: 16px !important;
    box-shadow: 0 14px 30px rgba(16,35,63,0.08) !important;
    display: inline-flex !important;
    gap: 0.35rem !important;
    margin: 0 0 1rem !important;
    min-height: 3.15rem !important;
    padding: 0.38rem !important;
    width: auto !important;
}
[data-testid="stTabs"] [data-baseweb="tab"],
button[data-baseweb="tab"],
[role="tab"] {
    align-items: center !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 12px !important;
    color: #48617f !important;
    display: inline-flex !important;
    font-size: 0.9rem !important;
    font-weight: 800 !important;
    height: 2.35rem !important;
    justify-content: center !important;
    line-height: 1 !important;
    min-width: 0 !important;
    padding: 0 1.05rem !important;
    white-space: nowrap !important;
}
[data-testid="stTabs"] [data-baseweb="tab"]::before,
[data-testid="stTabs"] [data-baseweb="tab"]::after,
button[data-baseweb="tab"]::before,
button[data-baseweb="tab"]::after,
[role="tab"]::before,
[role="tab"]::after {
    display: none !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] *,
button[data-baseweb="tab"] *,
[role="tab"] * {
    color: inherit !important;
    font-weight: 800 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover,
button[data-baseweb="tab"]:hover,
[role="tab"]:hover {
    background: #f2f8ff !important;
    border-color: #cfe0f7 !important;
    color: var(--lm-blue) !important;
}
[data-testid="stTabs"] [aria-selected="true"],
button[data-baseweb="tab"][aria-selected="true"],
[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #1769e0, #2f8cff) !important;
    border-color: #1769e0 !important;
    box-shadow: 0 10px 22px rgba(23,105,224,0.24) !important;
    color: #ffffff !important;
}
[data-testid="stTabs"] [aria-selected="true"] *,
button[data-baseweb="tab"][aria-selected="true"] *,
[role="tab"][aria-selected="true"] * {
    color: #ffffff !important;
}
[data-testid="stTabs"] [data-baseweb="tab-border"],
[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-baseweb="tab-border"],
div[data-baseweb="tab-highlight"],
[role="tablist"] + div,
[data-testid="stTabs"] [aria-hidden="true"] {
    display: none !important;
}

[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%) !important;
    border: 1.5px dashed #9fc5ff !important;
    border-radius: 18px !important;
    padding: 1.35rem !important;
}
[data-testid="stFileUploader"] button {
    background: #ffffff !important;
    border: 1px solid #c7d8ee !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 18px rgba(16,35,63,0.07) !important;
    color: var(--lm-blue) !important;
    font-weight: 800 !important;
}
[data-testid="stAlert"] {
    border-radius: 14px !important;
    box-shadow: 0 14px 28px rgba(16,35,63,0.07) !important;
}
[data-testid="stForm"],
[data-testid="stExpander"],
[data-testid="stDataFrame"],
[data-testid="stPlotlyChart"] {
    background: #ffffff !important;
    border-radius: 16px !important;
}

@media (max-width: 768px) {
    .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .hero-section { padding: 1.35rem; }
    .pill-row,
    .progress-meta { flex-direction: column; gap: 0.45rem; }
}
</style>
"""


def inject_css():
    """Inject shared app styling."""
    st.html(APP_CSS)


def page_header(title: str, subtitle: str = ""):
    """Render a styled page header with optional subtitle."""
    subtitle_html = f"<p>{html.escape(subtitle)}</p>" if subtitle else ""
    st.html(
        f"""
        <section class="page-header">
            <h1>{html.escape(title)}</h1>
            {subtitle_html}
        </section>
        """
    )


def keyword_pills_html(keywords: list) -> str:
    """Convert a list of keywords into styled pill badges HTML."""
    pills = "".join(
        f"<span class='kw-pill'>{html.escape(str(keyword))}</span>"
        for keyword in keywords
        if str(keyword).strip()
    )
    return f"<div style='margin:0.5rem 0 1rem 0; line-height:2.2;'>{pills}</div>" if pills else ""


def score_badge_html(score: int, total: int) -> str:
    """Return an HTML score badge based on percentage."""
    pct = (score / total * 100) if total > 0 else 0
    if pct >= 80:
        cls, label = "excellent", "Excellent"
    elif pct >= 60:
        cls, label = "good", "Good work"
    else:
        cls, label = "review", "Review needed"
    return f"<div class='score-badge {cls}'>{score}/{total} - {label} ({pct:.0f}%)</div>"
