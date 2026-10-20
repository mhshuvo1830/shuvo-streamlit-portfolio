# Shuvo's portfolio — Streamlit Community Cloud

The original HTML, CSS and JavaScript portfolio has been wrapped in Streamlit **without rewriting its design**. The original navigation, themes, project cards, mobile menu and updated corporate-style footer with Facebook icon are retained.

## Run locally

Requirements: Python and pip.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501.

## Deploy (free) on Streamlit Community Cloud

1. Go to **https://github.com/new** and create a **public** repository (for example `shuvo-streamlit-portfolio`).
2. Extract the ZIP and open the **shuvo_streamlit_portfolio** folder. Upload **all its contents** to the **repository root** through **Add file → Upload files**. Required: `app.py`, `requirements.txt`, `assets/` and `static/`. 
3. **Important:** The `.streamlit` directory is hidden on some computers, and GitHub's browser upload may omit hidden folders. If that happens, create `.streamlit/config.toml` manually in GitHub with:

   ```toml
   [server]
   enableStaticServing = true
   ```

   This config is required for your portfolio CV links to download properly.
4. Visit **https://share.streamlit.io** and sign in with GitHub.
5. Choose **Create app** → **Yup, I have an app**.
6. Select `mhshuvo1830/shuvo-streamlit-portfolio`, branch `main`, and **main file path `app.py`**. Optional: choose an available custom URL such as `shuvo-portfolio`.
7. Click **Deploy**. Your actual shareable URL will appear after deployment; it will end with `.streamlit.app`.

Deployment may take a few minutes. Future GitHub commits automatically update your published app.

## Folder layout

```text
shuvo_streamlit_portfolio/
├── app.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── assets/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── headshot.jpeg
└── static/
    └── resume.pdf
```

## Customize

- `assets/index.html` — website content and sections
- `assets/styles.css` — colors, layout, responsive styling and footer design
- `assets/script.js` — GitHub, LinkedIn, **Facebook**, live-demo URLs and theme toggle
- `assets/headshot.jpeg` — portrait image
- `static/resume.pdf` — downloadable CV

The CV hyperlinks use `/app/static/resume.pdf`, served by Streamlit. The site code, photo and PDF are already included. This deployment is a Streamlit-hosted portfolio, not a Python rewrite of every section.

**Privacy note:** `static/resume.pdf` contains a phone number and street-level address from your uploaded CV. This will be publicly downloadable. Review or remove the CV if you prefer to limit public personal details.

**Compatibility:** Requires Streamlit >= 1.66 because it uses `st.iframe(..., height="content")` to display a full-height interactive HTML portfolio. If your deployment shows `st.iframe` errors, make sure Streamlit actually installed from `requirements.txt` and review the app's logs.
