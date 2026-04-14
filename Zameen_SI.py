"""
Zameen.com — Classifieds Strategic Intelligence Dashboard
100% LIVE DATA from Google Sheets. Zero hardcoded values.
Executive-grade layout. All chart layouts built inline — zero shared dict conflicts.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Zameen.com | Strategic Intelligence",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────
# DESIGN TOKENS
# ─────────────────────────────────────────────────────────────────
BG      = "#0E1117"
CARD    = "#161B22"
CARD2   = "#1C2333"
GREEN   = "#00A651"
GOLD    = "#C9A050"
CRIMSON = "#FF4B4B"
BLUE    = "#4A9EFF"
TEXT    = "#E0E0E0"
MUTED   = "#8B949E"
BORDER  = "#21262D"

# Pre-built rgba strings — no 8-char hex anywhere
G_DIM   = "rgba(0,166,81,0.10)"
G_MED   = "rgba(0,166,81,0.35)"
G_LINE  = "rgba(0,166,81,0.70)"
G_FILL  = "rgba(0,166,81,0.12)"
AU_DIM  = "rgba(201,160,80,0.10)"
AU_MED  = "rgba(201,160,80,0.40)"
AU_LINE = "rgba(201,160,80,0.80)"
R_DIM   = "rgba(255,75,75,0.10)"
B_DIM   = "rgba(33,38,45,0.50)"

# ─────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after {{ box-sizing:border-box; margin:0; padding:0; }}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {{
    background:{BG} !important;
    color:{TEXT} !important;
    font-family:'Syne', sans-serif;
}}
[data-testid="stHeader"] {{ display:none !important; }}
#MainMenu, footer, [data-testid="stToolbar"] {{ visibility:hidden; }}
.block-container {{ padding:0 2.2rem 3rem 2.2rem !important; max-width:100% !important; }}

/* Metrics */
[data-testid="metric-container"] {{
    background:{CARD} !important;
    border:1px solid {BORDER} !important;
    border-radius:12px !important;
    padding:1.2rem 1.4rem !important;
    position:relative; overflow:hidden;
}}
[data-testid="metric-container"]::after {{
    content:'';
    position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,{GREEN},transparent);
}}
[data-testid="metric-container"] label {{
    color:{MUTED} !important;
    font-size:0.62rem !important;
    letter-spacing:0.12em !important;
    text-transform:uppercase !important;
    font-weight:700 !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color:#fff !important;
    font-size:1.45rem !important;
    font-weight:700 !important;
    font-family:'JetBrains Mono', monospace !important;
    letter-spacing:-0.02em !important;
}}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
    font-size:0.72rem !important;
}}

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {{
    background:{CARD} !important;
    border-radius:10px !important;
    border:1px solid {BORDER} !important;
    padding:4px !important; gap:3px !important;
}}
[data-testid="stTabs"] [role="tab"] {{
    color:{MUTED} !important;
    background:transparent !important;
    border-radius:7px !important;
    font-size:0.78rem !important;
    font-weight:700 !important;
    padding:0.4rem 1.1rem !important;
    border:none !important;
    transition:all 0.18s !important;
}}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    background:{GREEN} !important;
    color:#fff !important;
}}

/* Select box */
div[data-baseweb="select"] > div {{
    background:{CARD2} !important;
    border:1px solid {BORDER} !important;
    border-radius:8px !important;
}}
div[data-baseweb="select"] span {{ color:{TEXT} !important; }}

/* Scrollbar */
::-webkit-scrollbar {{ width:4px; height:4px; }}
::-webkit-scrollbar-track {{ background:{BG}; }}
::-webkit-scrollbar-thumb {{ background:{BORDER}; border-radius:2px; }}

@keyframes pulse {{
    0%,100% {{ opacity:1; }}
    50%      {{ opacity:0.3; }}
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────────────────
PASSWORD = "7862"
if "auth" not in st.session_state:    st.session_state.auth  = False
if "err"  not in st.session_state:    st.session_state.err   = False

if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.05, 1])
    with col:
        st.markdown("<div style='height:14vh'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;
             padding:2.8rem;box-shadow:0 24px 64px rgba(0,0,0,0.55);text-align:center;">
          <div style="font-size:2.2rem;margin-bottom:0.4rem;">🏢</div>
          <div style="font-family:'Syne',sans-serif;font-size:1.7rem;font-weight:800;
               color:#fff;letter-spacing:-0.03em;">
               zameen<span style="color:{GREEN};">.com</span></div>
          <div style="color:{MUTED};font-size:0.65rem;letter-spacing:0.16em;
               text-transform:uppercase;margin:0.4rem 0 2rem;font-weight:700;">
               Classifieds Intelligence Platform</div>
        </div>""", unsafe_allow_html=True)

        pwd = st.text_input("", type="password",
                            placeholder="🔑  Enter access password",
                            label_visibility="collapsed")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Authenticate →", use_container_width=True, type="primary"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.session_state.err  = False
                st.rerun()
            else:
                st.session_state.err = True
        if st.session_state.err:
            st.markdown(f"""
            <div style="color:{CRIMSON};font-size:0.78rem;margin-top:0.7rem;
                 background:{R_DIM};border:1px solid rgba(255,75,75,0.3);
                 border-radius:8px;padding:0.5rem 0.9rem;text-align:center;font-weight:600;">
                 ✗  Invalid credentials — access denied</div>""",
                 unsafe_allow_html=True)
        st.markdown(f"""
        <div style="color:{MUTED};font-size:0.6rem;letter-spacing:0.1em;
             text-transform:uppercase;text-align:center;margin-top:1.6rem;font-weight:600;">
             Restricted · Internal Use Only</div>""", unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────────
# LIVE DATA LOADER
# Sheet layout (0-indexed rows after pd.read_csv with no header):
#   0     = title
#   1     = headers: B=Name, C=FC Rev, D=Jan…O=Dec, P=YTD
#   2–7   = FORECAST rows (6 initiatives)
#   8     = FORECAST totals
#   9     = blank
#   10    = title 2
#   11    = headers 2
#   12–17 = ACTUAL rows
#   18    = ACTUAL totals
#   19    = blank
#   20    = Net Variance row
#   21    = % Achievement row
# ─────────────────────────────────────────────────────────────────
SHEET_CSV = (
    "https://docs.google.com/spreadsheets/d/"
    "1gegnSeFaH84_pwSrGMc3EADTnK-SNPwpv4ymMeO9wJY"
    "/export?format=csv&gid=0"
)
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]

def to_num(v):
    """Safe cell → float. Dashes, blanks, NaN → 0."""
    if pd.isna(v): return 0.0
    s = str(v).strip().replace(",","").replace("₨","").replace("%","").strip()
    if s in ("-","","—","–"): return 0.0
    try:    return float(s)
    except: return 0.0

@st.cache_data(ttl=300, show_spinner=False)
def load():
    raw = pd.read_csv(SHEET_CSV, header=None, dtype=str)

    COL_NAME   = 1
    COL_FCREV  = 2
    COL_MON    = list(range(3, 15))   # D–O = Jan–Dec
    COL_YTD    = 15

    def block(r0, r1):
        rows = []
        for i in range(r0, r1):
            if i >= len(raw): break
            r = raw.iloc[i]
            entry = {
                "Initiative": str(r.iloc[COL_NAME]).strip(),
                "FC_Rev":     to_num(r.iloc[COL_FCREV]),
                "YTD":        to_num(r.iloc[COL_YTD]) if COL_YTD < len(r) else 0.0,
            }
            for j, m in enumerate(MONTHS):
                c = COL_MON[j]
                entry[m] = to_num(r.iloc[c]) if c < len(r) else 0.0
            rows.append(entry)
        return pd.DataFrame(rows)

    def totrow(idx):
        if idx >= len(raw): return {}
        r = raw.iloc[idx]
        out = {"FC_Rev": to_num(r.iloc[COL_FCREV]),
               "YTD":   to_num(r.iloc[COL_YTD]) if COL_YTD < len(r) else 0.0}
        for j, m in enumerate(MONTHS):
            c = COL_MON[j]
            out[m] = to_num(r.iloc[c]) if c < len(r) else 0.0
        return out

    def numrow(idx):
        if idx >= len(raw): return {}
        r = raw.iloc[idx]
        out = {}
        for j, m in enumerate(MONTHS):
            c = COL_MON[j]
            s = str(r.iloc[c]).strip().replace("%","").replace(",","") if c < len(r) else "0"
            try:    out[m] = float(s) if s not in ("-","","—") else 0.0
            except: out[m] = 0.0
        ytd_s = str(r.iloc[COL_YTD]).strip().replace("%","") if COL_YTD < len(r) else "0"
        try:    out["YTD"] = float(ytd_s) if ytd_s not in ("-","","—") else 0.0
        except: out["YTD"] = 0.0
        return out

    df_fc  = block(2,  8)
    df_act = block(12, 18)
    fc_tot = totrow(8)
    ac_tot = totrow(18)
    var_m  = numrow(20)
    pct_m  = numrow(21)
    return df_fc, df_act, fc_tot, ac_tot, var_m, pct_m

# ── Load ──────────────────────────────────────────────────────────
with st.spinner(""):
    try:
        df_fc, df_act, fc_tot, ac_tot, var_m, pct_m = load()
    except Exception as e:
        st.error(f"❌ Cannot reach Google Sheet: {e}")
        st.info("Ensure the sheet is: File → Share → Anyone with link → Viewer")
        st.stop()

# Computed series — all from live data
fc_mon  = [float(df_fc[m].sum())  for m in MONTHS]
act_mon = [float(df_act[m].sum()) for m in MONTHS]

TOTAL_FC    = fc_tot.get("FC_Rev", df_fc["FC_Rev"].sum())
TOTAL_ACT   = ac_tot.get("YTD",   sum(act_mon))

# Always compute from raw data — sheet variance/pct cells may be blank or zero
rep_temp    = [m for m in MONTHS if act_mon[MONTHS.index(m)] > 0]
FC_YTD_COMP = sum(fc_mon[MONTHS.index(m)] for m in rep_temp)
TOTAL_VAR   = TOTAL_ACT - FC_YTD_COMP
YTD_PCT     = (TOTAL_ACT / FC_YTD_COMP * 100) if FC_YTD_COMP > 0 else 0.0

rep   = [m for m in MONTHS if act_mon[MONTHS.index(m)] > 0]   # reported months
n_rep = len(rep)

# ─────────────────────────────────────────────────────────────────
# UTIL FUNCTIONS
# ─────────────────────────────────────────────────────────────────
def fmt(n, short=False, signed=False):
    """Format PKR value. signed=True prepends +/- for non-zero values."""
    if n == 0: return "—"
    neg  = n < 0
    a    = abs(n)
    sign = ("−" if neg else ("+" if signed else ""))
    if short:
        if a >= 1e9: return f"{sign}₨{a/1e9:.1f}B"
        if a >= 1e6: return f"{sign}₨{a/1e6:.1f}M"
        if a >= 1e3: return f"{sign}₨{a/1e3:.0f}K"
        return f"{sign}₨{a:.0f}"
    else:
        if a >= 1e9: return f"{sign}₨ {a/1e9:.2f}B"
        if a >= 1e6: return f"{sign}₨ {a/1e6:.2f}M"
        if a >= 1e3: return f"{sign}₨ {a/1e3:.1f}K"
        return f"{sign}₨ {a:,.0f}"

def pct_bar(pct, color):
    w = min(max(float(pct), 0), 100)
    return (f'<div style="background:{CARD2};border-radius:3px;height:4px;'
            f'width:100%;overflow:hidden;margin-top:6px;">'
            f'<div style="background:{color};height:100%;width:{w}%;'
            f'border-radius:3px;"></div></div>')

def hdr(icon, title, sub=""):
    s = f' <span style="color:{MUTED};font-size:0.68rem;font-weight:400;">{sub}</span>' if sub else ""
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin:1.6rem 0 0.9rem;">
      <div style="width:28px;height:28px;background:{G_DIM};border-radius:7px;
           border:1px solid {G_LINE}44;display:flex;align-items:center;
           justify-content:center;font-size:0.8rem;">{icon}</div>
      <span style="font-weight:700;font-size:0.92rem;color:#fff;">{title}</span>{s}
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# CHART BUILDER — builds layout dict inline, NEVER shared/reused
# so there can be NO key conflicts
# ─────────────────────────────────────────────────────────────────
def pill(label, val, color):
    return (
        f"<div>"
        f"<div style=\"font-size:0.55rem;text-transform:uppercase;letter-spacing:0.12em;"
        f"color:{MUTED};font-weight:700;margin-bottom:3px;\">{label}</div>"
        f"<div style=\"font-family:JetBrains Mono,monospace;font-size:1rem;"
        f"font-weight:600;color:{color};\">{val}</div>"
        f"</div>"
    )

def base_layout(height, title="", margin_r=20, legend=True,
                legend_y=-0.22, xside="bottom", show_x_ticks=True,
                show_y_grid=True, show_x_grid=True):
    lay = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        font=dict(family="Syne, sans-serif", color=TEXT, size=11),
        margin=dict(l=8, r=margin_r, t=46, b=8),
        title=dict(text=title, font=dict(size=11, color=MUTED, family="Syne"),
                   x=0.01, y=0.99, xanchor="left", yanchor="top"),
        xaxis=dict(
            side=xside,
            gridcolor=BORDER if show_x_grid else "rgba(0,0,0,0)",
            linecolor=BORDER,
            tickfont=dict(color=MUTED, size=10, family="JetBrains Mono"),
            tickcolor=BORDER,
            showticklabels=show_x_ticks,
        ),
        yaxis=dict(
            gridcolor=B_DIM,
            linecolor=BORDER,
            tickfont=dict(color=MUTED, size=10, family="JetBrains Mono"),
            tickformat=",.0f",
            tickcolor=BORDER,
            showgrid=show_y_grid,
        ),
    )
    if legend:
        lay["legend"] = dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=BORDER,
            borderwidth=1,
            font=dict(color=MUTED, size=10, family="Syne"),
            orientation="h",
            x=0, y=legend_y,
        )
    else:
        lay["showlegend"] = False
    return lay

# ─────────────────────────────────────────────────────────────────
# NAV BAR
# ─────────────────────────────────────────────────────────────────
col_refresh = st.button("↺", key="refresh_btn", help="Force refresh data")
if col_refresh:
    st.cache_data.clear()
    st.rerun()

st.markdown(f"""
<div style="background:{CARD};border-bottom:1px solid {BORDER};padding:0.9rem 2.2rem;
     display:flex;align-items:center;justify-content:space-between;
     margin:0 -2.2rem 1.8rem -2.2rem;">
  <div style="display:flex;align-items:center;gap:1rem;">
    <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;
         color:#fff;letter-spacing:-0.03em;">
         zameen<span style="color:{GREEN};">.com</span></div>
    <div style="width:1px;height:20px;background:{BORDER};"></div>
    <div>
      <div style="font-size:0.7rem;font-weight:700;color:{TEXT};">
           Classifieds · Strategic Initiatives</div>
      <div style="font-size:0.58rem;color:{MUTED};text-transform:uppercase;
           letter-spacing:0.1em;">Revenue Intelligence · FY 2026</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:0.8rem;">
    <div style="background:{G_DIM};border:1px solid {G_LINE}55;border-radius:20px;
         padding:3px 11px;font-size:0.58rem;font-weight:700;color:{GREEN};
         letter-spacing:0.12em;text-transform:uppercase;display:flex;
         align-items:center;gap:5px;">
      <div style="width:5px;height:5px;border-radius:50%;background:{GREEN};
           animation:pulse 2s infinite;"></div>Live · 5 min
    </div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
         color:{MUTED};background:{CARD2};border:1px solid {BORDER};
         border-radius:7px;padding:3px 10px;">
         Reported: {", ".join(rep) if rep else "None"}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# SECTION A — EXECUTIVE SCORECARDS
# ─────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5 = st.columns(5)

fc_rep_total = sum(fc_mon[MONTHS.index(m)] for m in rep) if rep else 0
run_rate     = (TOTAL_ACT / n_rep * 12) if n_rep > 0 else 0
fc_remaining = TOTAL_FC - TOTAL_ACT

with k1:
    st.metric("Full-Year FC", fmt(TOTAL_FC),
              f"{len(df_fc)} active initiatives")
with k2:
    st.metric("YTD Actual", fmt(TOTAL_ACT),
              f"{YTD_PCT:.0f}% achieved" if YTD_PCT else "—")
with k3:
    st.metric("YTD Variance", fmt(TOTAL_VAR),
              "▲ Ahead" if TOTAL_VAR >= 0 else "▼ Below plan")
with k4:
    st.metric("Annualised Run Rate", fmt(run_rate),
              f"vs FC {fmt(TOTAL_FC, short=True)}")
with k5:
    st.metric("FC Remaining (YTD)", fmt(fc_remaining),
              f"{100-YTD_PCT:.0f}% of year left" if YTD_PCT else "—")

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# SECTION B — MONTHLY PERFORMANCE CARDS
# ─────────────────────────────────────────────────────────────────
if rep:
    hdr("📅", "Monthly Performance", f"{' · '.join(rep)} · Reported Months")
    mcols = st.columns(n_rep)
    for col, m in zip(mcols, rep):
        mi     = MONTHS.index(m)
        act_v  = act_mon[mi]
        fc_v   = fc_mon[mi]
        var_v  = act_v - fc_v  # always computed — sheet cells may be blank
        pct_v  = (act_v / fc_v * 100) if fc_v > 0 else 0
        clr    = GREEN if pct_v >= 100 else (GOLD if pct_v >= 80 else CRIMSON)
        vc     = GREEN if var_v >= 0 else CRIMSON
        with col:
            st.markdown(f"""
            <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
                 padding:1.2rem;position:relative;overflow:hidden;">
              <div style="position:absolute;top:0;left:0;right:0;height:2px;
                   background:linear-gradient(90deg,{clr},transparent);"></div>
              <div style="display:flex;justify-content:space-between;align-items:flex-start;
                   margin-bottom:0.7rem;">
                <div style="font-size:0.58rem;font-weight:800;letter-spacing:0.15em;
                     text-transform:uppercase;color:{MUTED};">{m} 2026</div>
                <div style="background:{clr}22;border:1px solid {clr}55;border-radius:6px;
                     padding:2px 8px;">
                  <span style="font-family:'JetBrains Mono',monospace;font-size:0.85rem;
                        font-weight:700;color:{clr};">{pct_v:.0f}%</span>
                </div>
              </div>
              <div style="font-family:'JetBrains Mono',monospace;font-size:1.25rem;
                   font-weight:600;color:#fff;margin-bottom:2px;">{fmt(act_v)}</div>
              <div style="font-size:0.65rem;color:{MUTED};margin-bottom:0.8rem;">
                   Forecast: <span style="color:{TEXT};font-family:'JetBrains Mono',monospace;">
                   {fmt(fc_v)}</span></div>
              {pct_bar(pct_v, clr)}
              <div style="font-size:0.65rem;color:{vc};margin-top:0.6rem;
                   font-family:'JetBrains Mono',monospace;">
                {fmt(var_v, signed=True)} vs plan
              </div>
            </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Overview",
    "🎯  Initiative Drill-Down",
    "📈  Trends & Heatmap",
    "🗂  Raw Data",
])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# Two rows:
#   Row 1: [Full-year FC vs Actual bar chart (wide)] | [Donut mix]
#   Row 2: [Initiative grouped bar with labels] | [Variance table]
# ══════════════════════════════════════════════════════════════════
with tab1:

    # ── Row 1 ────────────────────────────────────────────────────
    r1a, r1b = st.columns([1.65, 1], gap="large")

    with r1a:
        hdr("📊", "Forecast vs Actual — Full Year View")

        fig = go.Figure()

        # FC bars — all 12 months
        fig.add_trace(go.Bar(
            x=MONTHS, y=fc_mon,
            name="Forecast",
            marker=dict(
                color=AU_MED,
                line=dict(color=GOLD, width=1.2),
            ),
            text=[fmt(v, short=True) if v > 0 else "" for v in fc_mon],
            textposition="outside",
            textfont=dict(color=MUTED, size=8, family="JetBrains Mono"),
        ))

        # Actual bars — reported months only
        if rep:
            act_vals = [act_mon[MONTHS.index(m)] for m in rep]
            fig.add_trace(go.Bar(
                x=rep, y=act_vals,
                name="Actual",
                marker=dict(
                    color=GREEN,
                    line=dict(color=G_LINE, width=1.2),
                ),
                text=[fmt(v, short=True) for v in act_vals],
                textposition="outside",
                textfont=dict(color=GREEN, size=9, family="JetBrains Mono"),
            ))

        lay = base_layout(320, "Monthly Revenue (PKR) · All 12 Months")
        lay["barmode"] = "overlay"
        lay["bargap"]  = 0.28
        fig.update_layout(lay)
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": False})

    with r1b:
        hdr("🍩", "Revenue Mix by Initiative")

        colors6 = [GREEN, GOLD, BLUE, CRIMSON, "#A78BFA", "#FB923C"]
        fig2 = go.Figure(go.Pie(
            labels=df_fc["Initiative"].tolist(),
            values=df_fc["FC_Rev"].tolist(),
            hole=0.60,
            marker=dict(colors=colors6,
                        line=dict(color=BG, width=3)),
            textinfo="none",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "₨ %{value:,.0f}<br>"
                "%{percent}<extra></extra>"
            ),
        ))
        fig2.add_annotation(
            text=(f"<b>{fmt(TOTAL_FC, short=True)}</b>"
                  f"<br><span style='font-size:10px'>Full-Year FC</span>"),
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color=TEXT, family="JetBrains Mono"),
            align="center",
        )
        lay2 = dict(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=320,
            font=dict(family="Syne, sans-serif", color=TEXT, size=10),
            margin=dict(l=8, r=130, t=46, b=8),
            title=dict(text="Full-Year Forecast Share",
                       font=dict(size=11, color=MUTED), x=0.01, y=0.99),
            showlegend=True,
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                bordercolor=BORDER,
                borderwidth=1,
                font=dict(size=8, color=MUTED),
                orientation="v",
                x=1.02, y=0.5,
            ),
        )
        fig2.update_layout(lay2)
        st.plotly_chart(fig2, use_container_width=True,
                        config={"displayModeBar": False})

    # ── Row 2 ────────────────────────────────────────────────────
    if rep:
        r2a, r2b = st.columns([1.5, 1], gap="large")

        with r2a:
            hdr("🌊", "Initiative Performance · FC vs Actual",
                f"Reported: {', '.join(rep)}")

            inits   = df_fc["Initiative"].tolist()
            fc_r    = [float(df_fc.loc[df_fc["Initiative"]==i, rep].values[0].sum())
                       for i in inits]
            act_r   = [float(df_act.loc[df_act["Initiative"]==i, rep].values[0].sum())
                       for i in inits]
            pct_r   = [(a/f*100) if f > 0 else 0 for a, f in zip(act_r, fc_r)]
            var_r   = [a - f for a, f in zip(act_r, fc_r)]

            fig3 = go.Figure()
            fig3.add_trace(go.Bar(
                x=inits, y=fc_r,
                name="Forecast",
                marker=dict(color=AU_MED, line=dict(color=GOLD, width=1)),
                text=[fmt(v, short=True) for v in fc_r],
                textposition="inside",
                textfont=dict(color=GOLD, size=8, family="JetBrains Mono"),
            ))
            fig3.add_trace(go.Bar(
                x=inits, y=act_r,
                name="Actual",
                marker=dict(color=G_MED, line=dict(color=GREEN, width=1)),
                text=[fmt(v, short=True) for v in act_r],
                textposition="inside",
                textfont=dict(color=GREEN, size=9, family="JetBrains Mono"),
            ))
            # % achieved as scatter on top
            pct_colors = [GREEN if p >= 100 else (GOLD if p >= 80 else CRIMSON)
                          for p in pct_r]
            fig3.add_trace(go.Scatter(
                x=inits, y=act_r,
                mode="text",
                text=[f"{p:.0f}%" for p in pct_r],
                textposition="top center",
                textfont=dict(color=[GREEN if p>=100 else (GOLD if p>=80 else CRIMSON)
                                     for p in pct_r],
                              size=11, family="JetBrains Mono"),
                showlegend=False,
            ))

            lay3 = base_layout(330, "YTD Performance by Initiative",
                               legend_y=-0.22)
            lay3["barmode"] = "group"
            lay3["bargap"]  = 0.22
            lay3["yaxis"]["tickformat"] = ",.0f"
            fig3.update_layout(lay3)
            st.plotly_chart(fig3, use_container_width=True,
                            config={"displayModeBar": False})

        with r2b:
            hdr("📋", "Initiative Scorecard")

            # Build a rich HTML scorecard table
            rows_html = ""
            sorted_inits = sorted(zip(inits, fc_r, act_r, pct_r, var_r),
                                  key=lambda x: x[3], reverse=True)
            for name, fc_v, act_v, pct_v, var_v in sorted_inits:
                clr = GREEN if pct_v >= 100 else (GOLD if pct_v >= 80 else CRIMSON)
                vc  = GREEN if var_v >= 0 else CRIMSON
                bar_w = min(pct_v, 100)
                short_name = name[:22] + "…" if len(name) > 22 else name
                rows_html += f"""
                <tr>
                  <td style="padding:0.7rem 0.8rem;border-bottom:1px solid {BORDER};">
                    <div style="font-size:0.72rem;font-weight:600;color:{TEXT};
                         margin-bottom:4px;">{short_name}</div>
                    <div style="background:{CARD2};border-radius:3px;height:4px;width:100%;">
                      <div style="background:{clr};height:100%;width:{bar_w}%;
                           border-radius:3px;"></div>
                    </div>
                  </td>
                  <td style="padding:0.7rem 0.6rem;border-bottom:1px solid {BORDER};
                       text-align:right;font-family:'JetBrains Mono',monospace;
                       font-size:0.72rem;color:{TEXT};">{fmt(act_v, short=True)}</td>
                  <td style="padding:0.7rem 0.6rem;border-bottom:1px solid {BORDER};
                       text-align:center;">
                    <span style="background:{clr}22;border:1px solid {clr}55;
                          border-radius:5px;padding:2px 7px;font-size:0.72rem;
                          font-weight:700;color:{clr};font-family:'JetBrains Mono',monospace;">
                      {pct_v:.0f}%
                    </span>
                  </td>
                  <td style="padding:0.7rem 0.6rem;border-bottom:1px solid {BORDER};
                       text-align:right;font-family:'JetBrains Mono',monospace;
                       font-size:0.7rem;color:{vc};">{fmt(var_v, short=True, signed=True)}</td>
                </tr>"""

            st.markdown(f"""
            <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
                 overflow:hidden;margin-top:2.4rem;">
              <table style="width:100%;border-collapse:collapse;">
                <thead>
                  <tr style="background:{CARD2};">
                    <th style="padding:0.6rem 0.8rem;text-align:left;color:{MUTED};
                         font-size:0.58rem;letter-spacing:0.12em;text-transform:uppercase;
                         font-weight:700;border-bottom:1px solid {BORDER};">Initiative</th>
                    <th style="padding:0.6rem 0.6rem;text-align:right;color:{MUTED};
                         font-size:0.58rem;letter-spacing:0.12em;text-transform:uppercase;
                         font-weight:700;border-bottom:1px solid {BORDER};">Actual</th>
                    <th style="padding:0.6rem 0.6rem;text-align:center;color:{MUTED};
                         font-size:0.58rem;letter-spacing:0.12em;text-transform:uppercase;
                         font-weight:700;border-bottom:1px solid {BORDER};">Ach%</th>
                    <th style="padding:0.6rem 0.6rem;text-align:right;color:{MUTED};
                         font-size:0.58rem;letter-spacing:0.12em;text-transform:uppercase;
                         font-weight:700;border-bottom:1px solid {BORDER};">Var</th>
                  </tr>
                </thead>
                <tbody>{rows_html}</tbody>
              </table>
              <div style="padding:0.55rem 0.8rem;border-top:1px solid {BORDER};
                   font-size:0.6rem;color:{MUTED};display:flex;justify-content:space-between;">
                <span>Sorted: highest → lowest achievement</span>
                <span style="font-family:'JetBrains Mono',monospace;">
                    {", ".join(rep)} reported</span>
              </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 2 — INITIATIVE DRILL-DOWN
# ══════════════════════════════════════════════════════════════════
with tab2:
    hdr("🎯", "Initiative Performance Drill-Down")

    sel = st.selectbox("", df_fc["Initiative"].tolist(),
                       label_visibility="collapsed")
    fr  = df_fc[df_fc["Initiative"] == sel].iloc[0]
    ar  = df_act[df_act["Initiative"] == sel].iloc[0]

    fc_vals  = [float(fr[m]) for m in MONTHS]
    act_vals = [float(ar[m]) for m in MONTHS]
    rep_fc   = sum(float(fr[m]) for m in rep) if rep else 0
    rep_act  = sum(float(ar[m]) for m in rep) if rep else 0
    rep_var  = rep_act - rep_fc
    rep_pct  = (rep_act / rep_fc * 100) if rep_fc > 0 else 0
    ann_run  = (rep_act / n_rep * 12) if n_rep > 0 else 0

    # 4 KPIs
    d1,d2,d3,d4 = st.columns(4)
    with d1: st.metric("Full-Year Forecast", fmt(float(fr["FC_Rev"])))
    with d2: st.metric("YTD Actual",         fmt(rep_act))
    with d3: st.metric("YTD Forecast",        fmt(rep_fc))
    with d4: st.metric("Achievement",
                        f"{rep_pct:.1f}%",
                        fmt(rep_var))

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    da, db = st.columns([1.6, 1], gap="large")

    with da:
        hdr("📈", f"{sel} · Monthly Detail")

        fig4 = go.Figure()

        # Forecast line
        fig4.add_trace(go.Scatter(
            x=MONTHS, y=fc_vals,
            name="Forecast",
            mode="lines+markers+text",
            line=dict(color=GOLD, width=2, dash="dot"),
            marker=dict(size=5, color=GOLD,
                        line=dict(color=BG, width=1)),
            fill="tozeroy",
            fillcolor=AU_DIM,
            text=[fmt(v, short=True) if v>0 else "" for v in fc_vals],
            textposition="top center",
            textfont=dict(color=MUTED, size=8, family="JetBrains Mono"),
        ))

        # Actual bars (cleaner than line for actuals)
        if rep:
            av = [act_vals[MONTHS.index(m)] for m in rep]
            fig4.add_trace(go.Bar(
                x=rep, y=av,
                name="Actual",
                marker=dict(color=G_MED, line=dict(color=GREEN, width=1.5)),
                text=[fmt(v, short=True) for v in av],
                textposition="outside",
                textfont=dict(color=GREEN, size=10, family="JetBrains Mono"),
            ))

        lay4 = base_layout(300, f"Monthly: Forecast vs Actual", legend_y=-0.25)
        lay4["barmode"] = "overlay"
        fig4.update_layout(lay4)
        st.plotly_chart(fig4, use_container_width=True,
                        config={"displayModeBar": False})

    with db:
        hdr("🎯", "Achievement Gauge")
        gc = GREEN if rep_pct >= 100 else (GOLD if rep_pct >= 75 else CRIMSON)

        fig5 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=round(rep_pct, 1),
            delta=dict(
                reference=100,
                valueformat=".1f",
                increasing=dict(color=GREEN),
                decreasing=dict(color=CRIMSON),
                suffix=" pp vs target",
            ),
            number=dict(
                suffix="%",
                font=dict(size=30, color=TEXT, family="JetBrains Mono"),
            ),
            gauge=dict(
                axis=dict(
                    range=[0, 150],
                    tickfont=dict(color=MUTED, size=8),
                    tickvals=[0, 50, 75, 100, 125, 150],
                    ticktext=["0%","50%","75%","100%","125%","150%"],
                ),
                bar=dict(color=gc, thickness=0.25),
                bgcolor="rgba(0,0,0,0)",
                bordercolor=BORDER,
                borderwidth=1,
                steps=[
                    dict(range=[0,   75],  color=R_DIM),
                    dict(range=[75,  100], color=AU_DIM),
                    dict(range=[100, 150], color=G_DIM),
                ],
                threshold=dict(
                    line=dict(color=GREEN, width=2.5),
                    thickness=0.8, value=100,
                ),
            ),
            title=dict(
                text=f"YTD Achievement · {', '.join(rep) if rep else '—'}",
                font=dict(size=10, color=MUTED),
            ),
        ))
        fig5.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Syne", color=TEXT),
            margin=dict(l=20, r=20, t=55, b=10),
            height=300,
        )
        st.plotly_chart(fig5, use_container_width=True,
                        config={"displayModeBar": False})

    # Monthly breakdown table with 3 rows: FC / Actual / Variance
    hdr("📋", "Full Monthly Breakdown")

    col_th = "".join(
        f'<th style="padding:0.55rem 0.7rem;text-align:right;color:{MUTED};'
        f'font-size:0.58rem;letter-spacing:0.1em;text-transform:uppercase;'
        f'font-weight:700;border-bottom:1px solid {BORDER};'
        f'background:{"rgba(0,166,81,0.08)" if m in rep else CARD2};">{m}</th>'
        for m in MONTHS)

    def td(val, color=TEXT, bold=False):
        fw = "700" if bold else "400"
        return (f'<td style="padding:0.55rem 0.7rem;text-align:right;color:{color};'
                f'font-family:JetBrains Mono,monospace;font-size:0.7rem;'
                f'border-bottom:1px solid {BORDER};font-weight:{fw};">{val}</td>')

    fc_tds  = "".join(td(fmt(float(fr[m]), short=True), TEXT) for m in MONTHS)
    act_tds = "".join(
        td(fmt(float(ar[m]), short=True), GREEN if float(ar[m])>0 else MUTED,
           bold=float(ar[m])>0)
        for m in MONTHS)
    var_tds = ""
    for m in MONTHS:
        v = float(ar[m]) - float(fr[m])
        if float(ar[m]) == 0:
            var_tds += td("—", MUTED)
        else:
            c = GREEN if v > 0 else (CRIMSON if v < 0 else MUTED)
            var_tds += td(fmt(v, short=True, signed=True), c, bold=True)

    row_lbl = (f'<td style="padding:0.55rem 1rem;border-bottom:1px solid {BORDER};'
               f'font-size:0.7rem;font-weight:700;white-space:nowrap;')
    st.markdown(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;overflow:hidden;">
      <div style="overflow-x:auto;">
      <table style="width:100%;border-collapse:collapse;">
        <thead><tr style="background:{CARD2};">
          <th style="padding:0.55rem 1rem;text-align:left;color:{MUTED};font-size:0.58rem;
               letter-spacing:0.1em;text-transform:uppercase;font-weight:700;
               border-bottom:1px solid {BORDER};min-width:75px;">Metric</th>{col_th}
        </tr></thead>
        <tbody>
          <tr>
            {row_lbl}color:{GOLD};">Forecast</td>{fc_tds}
          </tr>
          <tr>
            {row_lbl}color:{GREEN};">Actual</td>{act_tds}
          </tr>
          <tr>
            {row_lbl}color:{MUTED};">Variance</td>{var_tds}
          </tr>
        </tbody>
      </table>
      </div>
      <div style="padding:0.5rem 1rem;border-top:1px solid {BORDER};font-size:0.6rem;
           color:{MUTED};display:flex;gap:1rem;">
        <span style="background:{G_DIM};padding:1px 7px;border-radius:4px;
              font-family:'JetBrains Mono',monospace;">▓ Reported months highlighted</span>
      </div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 3 — TRENDS & HEATMAP
# ══════════════════════════════════════════════════════════════════
with tab3:
    ta, tb = st.columns([1,1], gap="large")

    with ta:
        hdr("📈", "Cumulative Revenue Trajectory")
        cum_fc = list(np.cumsum(fc_mon))

        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(
            x=MONTHS, y=cum_fc,
            name="Cumulative FC",
            mode="lines+markers",
            line=dict(color=GOLD, width=2, dash="dot"),
            marker=dict(size=5, color=GOLD),
            fill="tozeroy",
            fillcolor=AU_DIM,
        ))
        if rep:
            av     = [act_mon[MONTHS.index(m)] for m in rep]
            cum_act = list(np.cumsum(av))
            fig6.add_trace(go.Scatter(
                x=rep, y=cum_act,
                name="Cumulative Actual",
                mode="lines+markers+text",
                line=dict(color=GREEN, width=2.5),
                marker=dict(size=9, color=GREEN,
                            line=dict(color=BG, width=2)),
                fill="tozeroy",
                fillcolor=G_FILL,
                text=[fmt(v, short=True) for v in cum_act],
                textposition="top center",
                textfont=dict(color=GREEN, size=10, family="JetBrains Mono"),
            ))

        fig6.add_hline(
            y=TOTAL_FC,
            line_dash="dash", line_color=CRIMSON, line_width=1.2,
            annotation_text=f"Full-Year Target {fmt(TOTAL_FC, short=True)}",
            annotation_font_color=CRIMSON,
            annotation_font_size=9,
        )
        lay6 = base_layout(310, "Cumulative Revenue (PKR)")
        fig6.update_layout(lay6)
        st.plotly_chart(fig6, use_container_width=True,
                        config={"displayModeBar": False})

    with tb:
        hdr("🏆", "YTD Initiative Ranking")
        df_r = df_act.copy()
        df_r["_ytd"] = df_r[MONTHS].sum(axis=1)
        df_r = df_r[df_r["_ytd"] > 0].sort_values("_ytd", ascending=True)

        if not df_r.empty:
            n = len(df_r)
            bcolors = [GREEN if i == n-1 else (G_MED if i >= n-2 else G_DIM)
                       for i in range(n)]
            fig7 = go.Figure(go.Bar(
                x=df_r["_ytd"].astype(float),
                y=df_r["Initiative"],
                orientation="h",
                marker=dict(
                    color=bcolors,
                    line=dict(color=G_LINE, width=1),
                ),
                text=[fmt(float(v), short=True) for v in df_r["_ytd"]],
                textposition="outside",
                textfont=dict(color=TEXT, size=10, family="JetBrains Mono"),
            ))
            lay7 = base_layout(310, "YTD Actual Revenue Ranking",
                               legend=False)
            lay7["xaxis"]["showgrid"]        = False
            lay7["xaxis"]["showticklabels"]  = False
            lay7["yaxis"]["gridcolor"]       = "rgba(0,0,0,0)"
            lay7["yaxis"]["tickfont"]        = dict(color=TEXT, size=9,
                                                    family="JetBrains Mono")
            fig7.update_layout(lay7)
            st.plotly_chart(fig7, use_container_width=True,
                            config={"displayModeBar": False})
        else:
            st.info("No actual data yet.")

    # Full-width heatmap
    hdr("🔥", "Revenue Intensity Heatmap — Forecast FY2026",
        "Darker = higher revenue concentration")

    heat_z = [
        [float(df_fc.loc[df_fc["Initiative"]==init, m].values[0])
         for m in MONTHS]
        for init in df_fc["Initiative"]
    ]
    heat_text = [
        [fmt(heat_z[i][j], short=True) for j in range(12)]
        for i in range(len(df_fc))
    ]

    fig8 = go.Figure(go.Heatmap(
        z=heat_z,
        x=MONTHS,
        y=df_fc["Initiative"].tolist(),
        colorscale=[[0, CARD2],[0.25, G_DIM],[0.6, G_MED],[1, GREEN]],
        showscale=True,
        text=heat_text,
        texttemplate="%{text}",
        textfont=dict(size=9, color=TEXT, family="JetBrains Mono"),
        hovertemplate="<b>%{y}</b><br>%{x}: ₨ %{z:,.0f}<extra></extra>",
        colorbar=dict(
            tickfont=dict(color=MUTED, size=9, family="JetBrains Mono"),
            tickformat=",.0f",
            outlinecolor=BORDER,
            outlinewidth=1,
            bgcolor="rgba(0,0,0,0)",
        ),
    ))
    fig8.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        font=dict(family="Syne, sans-serif", color=TEXT, size=11),
        margin=dict(l=8, r=90, t=46, b=8),
        title=dict(text="Forecast Revenue Intensity by Initiative × Month",
                   font=dict(size=11, color=MUTED), x=0.01, y=0.99),
        xaxis=dict(
            side="top",
            tickfont=dict(color=MUTED, size=10, family="JetBrains Mono"),
            gridcolor=BORDER,
            linecolor=BORDER,
        ),
        yaxis=dict(
            gridcolor="rgba(0,0,0,0)",
            tickfont=dict(size=9.5, color=TEXT, family="JetBrains Mono"),
            linecolor=BORDER,
        ),
    )
    st.plotly_chart(fig8, use_container_width=True,
                    config={"displayModeBar": False})

# ══════════════════════════════════════════════════════════════════
# TAB 4 — RAW DATA
# ══════════════════════════════════════════════════════════════════
with tab4:
    hdr("🗂", "Source Data — Live from Google Sheets")

    view = st.selectbox("",
                        ["📅 Forecast (Full Year)",
                         "✅ Actual (YTD)",
                         "📊 Variance Summary"],
                        label_visibility="collapsed")

    if "Forecast" in view:
        display_rows = []
        for _, r in df_fc.iterrows():
            display_rows.append(
                [r["Initiative"], fmt(float(r["FC_Rev"]))] +
                [fmt(float(r[m])) for m in MONTHS] +
                [fmt(float(r["YTD"]))]
            )
        cols_h = ["Initiative","FC Rev"] + MONTHS + ["YTD FC"]

    elif "Actual" in view:
        display_rows = []
        for _, r in df_act.iterrows():
            ytd_v = float(r.get("YTD", sum(float(r[m]) for m in MONTHS)))
            display_rows.append(
                [r["Initiative"]] +
                [fmt(float(r[m])) for m in MONTHS] +
                [fmt(ytd_v)]
            )
        cols_h = ["Initiative"] + MONTHS + ["YTD Actual"]

    else:
        display_rows = []
        for init in df_fc["Initiative"]:
            fc_r  = df_fc[df_fc["Initiative"] == init].iloc[0]
            act_r = df_act[df_act["Initiative"] == init].iloc[0]
            rfc   = sum(float(fc_r[m])  for m in rep) if rep else 0
            ract  = sum(float(act_r[m]) for m in rep) if rep else 0
            vv    = ract - rfc
            pp    = f"{ract/rfc*100:.0f}%" if rfc > 0 else "N/A"
            status = "✅ On Track" if (ract/rfc*100 if rfc>0 else 0) >= 90 else "⚠️ At Risk"
            display_rows.append([
                init,
                fmt(float(fc_r["FC_Rev"])),
                fmt(rfc), fmt(ract),
                fmt(vv, signed=True),
                pp, status,
            ])
        cols_h = ["Initiative","Full-Year FC","YTD FC","YTD Actual",
                  "Variance","% Achieved","Status"]

    th_style = (f'padding:0.6rem 0.9rem;text-align:left;color:{MUTED};'
                f'font-size:0.58rem;letter-spacing:0.12em;text-transform:uppercase;'
                f'font-weight:700;border-bottom:1px solid {BORDER};white-space:nowrap;')
    td_style = (f'padding:0.6rem 0.9rem;border-bottom:1px solid {BORDER};'
                f'font-family:JetBrains Mono,monospace;font-size:0.72rem;'
                f'color:{TEXT};white-space:nowrap;')

    hdrs_html = "".join(f'<th style="{th_style}">{c}</th>' for c in cols_h)
    body_html = ""
    for row in display_rows:
        cells = "".join(f'<td style="{td_style}">{v}</td>' for v in row)
        body_html += f"<tr>{cells}</tr>" 

    st.markdown(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;overflow:hidden;">
      <div style="overflow-x:auto;">
      <table style="width:100%;border-collapse:collapse;">
        <thead><tr style="background:{CARD2};">{hdrs_html}</tr></thead>
        <tbody>{body_html}</tbody>
      </table>
      </div>
      <div style="padding:0.6rem 0.9rem;border-top:1px solid {BORDER};
           font-size:0.6rem;color:{MUTED};display:flex;justify-content:space-between;">
        <span>{len(display_rows)} initiatives</span>
        <span style="font-family:'JetBrains Mono',monospace;">
          🔴 Live · Google Sheets · auto-refresh 5 min</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # Summary bar
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    var_c = CRIMSON if TOTAL_VAR < 0 else GREEN

    st.markdown(f"""
    <div style="background:{G_DIM};border:1px solid {G_LINE}44;border-radius:10px;
         padding:0.9rem 1.4rem;display:flex;gap:2.5rem;align-items:center;flex-wrap:wrap;">
      {pill("Full-Year FC",   fmt(TOTAL_FC),          GOLD)}
      <div style="width:1px;height:30px;background:{BORDER};"></div>
      {pill("YTD Actual",     fmt(TOTAL_ACT),         GREEN)}
      <div style="width:1px;height:30px;background:{BORDER};"></div>
      {pill("YTD Variance",   fmt(TOTAL_VAR, signed=True), var_c)}
      <div style="width:1px;height:30px;background:{BORDER};"></div>
      {pill("Achievement",    f"{YTD_PCT:.0f}%",      TEXT)}
      <div style="width:1px;height:30px;background:{BORDER};"></div>
      {pill("Run Rate (Ann.)", fmt(run_rate),          BLUE)}
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="border-top:1px solid {BORDER};margin-top:3rem;padding:1rem 0;
     display:flex;justify-content:space-between;align-items:center;
     font-size:0.58rem;color:{MUTED};letter-spacing:0.05em;">
  <span>zameen.com · Classifieds Strategic Intelligence · FY2026</span>
  <span style="font-family:'JetBrains Mono',monospace;">
    🔴 Live · Google Sheets · st.cache_data(ttl=300) · Password protected
  </span>
</div>""", unsafe_allow_html=True)
