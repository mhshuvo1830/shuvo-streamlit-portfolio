"""Md Mahamudul Hasan Shuvo's portfolio, packaged for Streamlit Cloud.

Uses Streamlit's st.iframe with content-height auto sizing to retain the
original, editable HTML/CSS/JavaScript portfolio (including its interactions).
Only trusted, repository-maintained HTML/CSS/JS is rendered.
"""

from base64 import b64encode
from pathlib import Path

import streamlit as st

BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"

st.set_page_config(
    page_title="Md Mahamudul Hasan Shuvo | Software Developer",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data(show_spinner=False)
def build_portfolio() -> str:
    """Inline static assets so they work inside Streamlit's HTML iframe.

    The PDF is served separately via Streamlit static file hosting.
    """
    html = (ASSETS / "index.html").read_text(encoding="utf-8")
    css = (ASSETS / "styles.css").read_text(encoding="utf-8")
    js = (ASSETS / "script.js").read_text(encoding="utf-8")
    headshot = b64encode((ASSETS / "headshot.jpeg").read_bytes()).decode("ascii")

    stylesheet = '<link href="styles.css" rel="stylesheet"/>'
    original_script = '<script defer="" src="script.js"></script>'
    assert stylesheet in html, "Could not find stylesheet link in assets/index.html"
    assert original_script in html, "Could not find script link in assets/index.html"

    html = html.replace(stylesheet, f"<style>\n{css}\n</style>")
    # Inline JS must run after the body has been parsed (unlike the old defer script).
    html = html.replace(original_script, "")
    html = html.replace('src="headshot.jpeg"', f'src="data:image/jpeg;base64,{headshot}"')
    html = html.replace('href="resume.pdf"', 'href="/app/static/resume.pdf"')
    assert '</body>' in html, "HTML template does not contain closing body tag"
    html = html.replace('</body>', f'<script>\n{js}\n</script>\n</body>')
    return html


# Remove Streamlit's default page gutters; the embedded original site is the UI.
st.html("""
<style>
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
footer[data-testid="stFooter"] { display: none !important; }
[data-testid="stAppViewContainer"],
[data-testid="stMain"] { background: #0b1020; }
[data-testid="stMainBlockContainer"] {
    max-width: 100% !important;
    padding: 0 !important;
}
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"] { gap: 0 !important; }
[data-testid="stElementContainer"] { width: 100% !important; }
[data-testid="stIFrame"] { border: 0 !important; width: 100% !important; }
iframe[title="Portfolio website"] { border: 0 !important; display: block; }
</style>
""")

# height="content" keeps the entire long portfolio and footer visible without
# an inner scrollbar, including on phones; requires Streamlit 1.66 or newer.
st.iframe(
    build_portfolio(),
    width="stretch",
    height="content",
    alt="Portfolio website",
)
