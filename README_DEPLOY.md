# Deploy Portfolio Manager to Streamlit Community Cloud

## Step 1 — Push to GitHub

```bash
cd pm8_web
git init
git add .
git commit -m "Initial Streamlit web app"
```

Create a new **public or private** repository on github.com, then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/portfolio-manager.git
git push -u origin main
```

## Step 2 — Deploy on Streamlit Community Cloud (free)

1. Go to **https://share.streamlit.io**
2. Click **"New app"**
3. Select your GitHub repository
4. Set:
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **Deploy**

Your app will be live at:
```
https://YOUR_USERNAME-portfolio-manager-app-XXXXX.streamlit.app
```

Share that URL with your team — anyone with the link can access it.

## Step 3 — Data persistence (important)

The app reads/writes `input/project_data.xlsx` on the server.

| Scenario | What happens |
|---|---|
| User edits data in the app | ✅ Saves immediately to the xlsx on the server |
| App restarts (Streamlit sleeps after inactivity) | ⚠️ Edits since last git push **may be lost** |
| New deployment pushed | ⚠️ The xlsx resets to what's in GitHub |

**For a small team where the data doesn't change constantly**, this is fine — you can always push an updated xlsx to GitHub to sync data.

**For production use**, replace the Excel backend with Google Sheets or Supabase:

```
# Google Sheets option (free)
pip install gspread gspread-dataframe
# → ask for the Google Sheets migration guide
```

## Local development

```bash
pip install -r requirements.txt
streamlit run app.py
# Opens in browser at http://localhost:8501
```

## File structure

```
pm8_web/
├── app.py                    ← Dashboard (entry point)
├── requirements.txt
├── .streamlit/
│   └── config.toml           ← Theme and server settings
├── config/
│   └── settings.py           ← Unchanged from desktop app
├── services/
│   └── portfolio_service.py  ← Unchanged from desktop app
├── repository/
│   └── excel_repository.py   ← Unchanged from desktop app
├── input/
│   └── project_data.xlsx     ← Your data file
├── assets/
│   └── kmg-logo.png          ← KMG logo (appears in topbar)
├── utils/
│   └── st_common.py          ← Shared page setup + helpers
└── pages/
    ├── 1_Portfolio.py         ← Portfolio view + CRUD
    ├── 2_RAG_Summary.py       ← RAG table + edit
    ├── 3_Timeline.py          ← Gantt chart + task CRUD
    └── 4_Project_Status.py    ← Status cards + task breakdown
```
