"""Md Mahamudul Hasan Shuvo's portfolio, packaged for Streamlit Cloud.

Uses a viewport-height, internally scrollable st.iframe so section navigation
works correctly (including mobile links and the footer's Back to Top).
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


# Make the portfolio iframe the ONE scrolling surface. When the iframe was
# height="content", anchors scrolled its (non-scrollable) document instead of
# the visible Streamlit page. A viewport-sized iframe lets native # links and
# CSS scroll-behavior work, and keeps the sticky navigation bar visible.
st.html("""
<style>
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
footer[data-testid="stFooter"] { display: none !important; }
html, body, #root { height: 100% !important; overflow: hidden !important; }
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #0b1020;
    height: 100dvh !important;
    overflow: hidden !important;
}
[data-testid="stMainBlockContainer"] {
    max-width: 100% !important;
    padding: 0 !important;
}
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"] { gap: 0 !important; }
[data-testid="stElementContainer"] { width: 100% !important; }
[data-testid="stIFrame"] { border: 0 !important; width: 100% !important; }
iframe[title="Portfolio website"] {
    display: block !important;
    width: 100% !important;
    height: 100vh !important; /* fallback for browsers without dvh */
    height: 100dvh !important;
    border: 0 !important;
}
</style>
""")

# IMPORTANT: Do NOT use height="content" here. Use an explicit height so
# native anchor navigation actually scrolls *within* the portfolio iframe.
# The above CSS sizes the iframe dynamically to the visitor's viewport.
st.iframe(
    build_portfolio(),
    width="stretch",
    height=900,  # fallback when CSS is unavailable; iframe remains scrollable
    alt="Portfolio website",
)
