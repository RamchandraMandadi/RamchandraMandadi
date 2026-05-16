"""
app.py  —  Dashboard (entry page)
Displays: KPI cards · RAG stacked bar · Projects at Risk · Health table
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.st_common import (
    setup_page, get_svc, rag_badge, rag_bg, rag_color,
    fmt_currency, RAG_ASPECTS, R_COLOR, A_COLOR, G_COLOR,
)

setup_page("Dashboard", "📊")

svc = get_svc()

# ═══════════════════════════════════════════════════════════
# KPI CARDS
# ═══════════════════════════════════════════════════════════
kpis = svc.get_kpis()
spent_pct = (kpis["spent"] / kpis["budget"] * 100) if kpis["budget"] else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Projects",  kpis["total"],  help="All active projects")
c2.metric("🔴 At Risk",      kpis["at_risk"], help="Red RAG overall")
c3.metric("🟡 Amber",        kpis["amber"],   help="Needs attention")
c4.metric("🟢 Green",        kpis["green"],   help="On track")
c5.metric("Budget Used",
          f"{spent_pct:.1f}%",
          help=f"{fmt_currency(kpis['spent'])} / {fmt_currency(kpis['budget'])}")
c6.metric("Avg Progress",    f"{kpis['avg_progress']}%", help="Across all projects")

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# MIDDLE ROW: RAG chart + Projects at risk
# ═══════════════════════════════════════════════════════════
left, right = st.columns([3, 1.2])

# ── RAG stacked bar chart ────────────────────────────────
with left:
    st.subheader("RAG Status by Aspect")
    rag_sm = svc.get_rag_summary()
    aspects = list(reversed(RAG_ASPECTS))   # bottom-up on the chart

    fig = go.Figure()
    for label, color, key in [
        ("Red",   R_COLOR, "R"),
        ("Amber", A_COLOR, "A"),
        ("Green", G_COLOR, "G"),
    ]:
        vals = [rag_sm[a][key] for a in aspects]
        fig.add_trace(go.Bar(
            name=label,
            y=aspects,
            x=vals,
            orientation="h",
            marker_color=color,
            text=[str(v) if v else "" for v in vals],
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white", size=12),
            hovertemplate=f"<b>%{{y}}</b><br>{label}: %{{x}}<extra></extra>",
        ))

    fig.update_layout(
        barmode="stack",
        height=340,
        margin=dict(l=0, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.12, x=0.3),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#eee", tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=12)),
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── Projects at Risk ─────────────────────────────────────
with right:
    st.subheader("Projects at Risk")
    risks = svc.get_projects_at_risk()
    if risks:
        for p in risks:
            red_aspects = ", ".join(p["reds"])
            st.markdown(f"""
            <div class="risk-card">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
                <span style="background:#e53935;color:white;font-weight:700;font-size:12px;
                             padding:2px 7px;border-radius:4px">R</span>
                <strong style="font-size:14px">{p['name']}</strong>
              </div>
              <div style="color:#e53935;font-size:12px;margin-bottom:2px">Red: {red_aspects}</div>
              <div style="color:#666;font-size:12px">{p['manager']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No projects currently at risk.")

# ═══════════════════════════════════════════════════════════
# PORTFOLIO HEALTH TABLE
# ═══════════════════════════════════════════════════════════
st.subheader("Portfolio Health Snapshot")
rows = svc.get_health_table()

if rows:
    df = pd.DataFrame(rows)

    def _cell_style(val):
        bg = {"R": "#fdecea", "A": "#fffbeb", "G": "#f0fdf4"}.get(str(val), "white")
        fg = {"R": "#e53935", "A": "#f59e0b", "G": "#16a34a"}.get(str(val), "#333")
        return f"background-color:{bg};color:{fg};font-weight:600;text-align:center"

    rag_cols = [c for c in df.columns if c in RAG_ASPECTS + ["overall"]]
    styled = df.style.applymap(_cell_style, subset=rag_cols)

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
        column_config={
            "name":    st.column_config.TextColumn("Project"),
            "manager": st.column_config.TextColumn("Manager"),
            "overall": st.column_config.TextColumn("Overall"),
        },
    )
else:
    st.info("No project data found.")
