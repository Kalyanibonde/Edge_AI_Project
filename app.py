import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Edge AI Negotiation System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&display=swap');

/* ── ROOT TOKENS ── */
:root {
    --gold:        #C9A84C;
    --gold-bright: #F0C755;
    --orange:      #E8763A;
    --red:         #C0392B;
    --bg:          #060810;
    --surface:     #0D1117;
    --surface2:    #131926;
    --border:      rgba(201,168,76,0.20);
    --text:        #E8DCC8;
    --muted:       #8A7A60;
    --font-serif:  'Times New Roman', Times, serif;
    --font-display:'Cinzel', 'Times New Roman', serif;
}

/* ── RESET ── */
html, body, .stApp { font-family: var(--font-serif) !important; }
/* Protect Material Icons universally */
span[class*="material"], .stIconMaterial, .material-symbols-rounded, [data-testid="stSidebarCollapseButton"] * {
    font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
}

.stApp { background: var(--bg) !important; color: var(--text) !important; }
[data-testid="stHeader"] { display: none !important; }

/* scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--gold); border-radius: 3px; }

/* ── SPLASH OVERLAY ── */
#splash-overlay {
    position: fixed; inset: 0; z-index: 9999;
    background: radial-gradient(ellipse at 50% 40%, #1a0a00 0%, #060810 70%);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    animation: fadeOutSplash 1s ease 3s forwards;
}
@keyframes fadeOutSplash {
    to { opacity: 0; visibility: hidden; }
}

#splash-overlay img {
    width: min(680px, 90vw);
    border-radius: 12px;
    box-shadow: 0 0 80px rgba(201,168,76,0.35), 0 0 160px rgba(232,118,58,0.15);
    animation: pulseGlow 3s ease-in-out infinite;
}
@keyframes pulseGlow {
    0%,100% { box-shadow: 0 0 60px rgba(201,168,76,0.3), 0 0 120px rgba(232,118,58,0.12); }
    50%      { box-shadow: 0 0 100px rgba(201,168,76,0.55), 0 0 200px rgba(232,118,58,0.25); }
}

#splash-title {
    font-family: var(--font-display) !important;
    font-size: clamp(1.6rem, 4vw, 2.8rem);
    color: var(--gold-bright);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 2rem;
    text-shadow: 0 0 30px rgba(201,168,76,0.6);
    animation: fadeUp 1.2s ease forwards;
}
#splash-sub {
    font-family: var(--font-serif) !important;
    font-size: 1rem;
    color: var(--muted);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-top: 0.6rem;
    animation: fadeUp 1.6s ease forwards;
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:translateY(0); }
}

#splash-bar-wrap {
    width: min(400px, 80vw);
    height: 3px;
    background: rgba(201,168,76,0.15);
    border-radius: 2px;
    margin-top: 2.5rem;
    overflow: hidden;
}
#splash-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, var(--gold), var(--gold-bright));
    border-radius: 2px;
    animation: loadBar 2.8s cubic-bezier(.4,0,.2,1) forwards;
}
@keyframes loadBar { to { width: 100%; } }

#splash-status {
    font-family: var(--font-serif) !important;
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-top: 0.8rem;
    animation: blink 1.5s step-end infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── MAIN CONTENT (hidden until splash gone) ── */
#main-content { animation: revealMain 0.8s ease 3.2s both; }
@keyframes revealMain { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }

/* ── HEADER ── */
.page-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.page-header h1 {
    font-family: var(--font-display) !important;
    font-size: clamp(1.6rem, 3.5vw, 2.6rem) !important;
    color: var(--gold-bright) !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    text-shadow: 0 0 24px rgba(201,168,76,0.4);
    margin: 0 !important;
}
.page-header p {
    font-family: var(--font-serif) !important;
    color: var(--muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-size: 0.78rem;
    margin-top: 0.4rem !important;
}

/* ── SECTION HEADINGS ── */
h2, h3 { font-family: var(--font-display) !important; color: var(--gold) !important; letter-spacing: 0.08em; }

/* ── METRIC CARDS ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface2) 100%) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 1.2rem 1.5rem !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(201,168,76,0.08);
    transition: transform .2s, box-shadow .2s;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(201,168,76,0.12);
}
[data-testid="stMetricLabel"] {
    font-family: var(--font-serif) !important;
    color: var(--muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-size: 0.75rem !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    color: var(--gold-bright) !important;
    font-size: 1.8rem !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0e18 0%, #060810 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] *:not(.stIconMaterial):not([class*="material"]) { font-family: var(--font-serif) !important; color: var(--text) !important; }
[data-testid="stSidebarCollapseButton"] * { font-family: "Material Symbols Rounded" !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
    font-family: var(--font-display) !important;
    color: var(--gold) !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.stSlider > div > div > div { background: var(--gold) !important; }
.stSlider > div > div { background: rgba(201,168,76,0.2) !important; }

/* ── BUTTONS ── */
.stButton > button {
    font-family: var(--font-display) !important;
    background: linear-gradient(135deg, #1a1200, #2a1e00) !important;
    color: var(--gold-bright) !important;
    border: 1px solid var(--gold) !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-radius: 6px !important;
    padding: 0.6rem 1.6rem !important;
    transition: all .25s;
    box-shadow: 0 0 0 rgba(201,168,76,0);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2a1e00, #3d2c00) !important;
    box-shadow: 0 0 20px rgba(201,168,76,0.3) !important;
    transform: translateY(-1px);
}

/* ── ALERTS ── */
.stSuccess { background: rgba(22,55,22,0.6) !important; border-left: 3px solid #4CAF50 !important; }
.stError   { background: rgba(55,22,22,0.6) !important; border-left: 3px solid var(--red) !important; }
.stSuccess *, .stError * { font-family: var(--font-serif) !important; }

/* ── DATAFRAME ── */
.stDataFrame { border: 1px solid var(--border) !important; border-radius: 8px; overflow: hidden; }

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* ── STATUS BADGE ── */
.status-badge {
    display: inline-block;
    padding: 0.25rem 1rem;
    border-radius: 20px;
    font-family: var(--font-serif) !important;
    font-size: 0.78rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.badge-ok  { background: rgba(76,175,80,0.15); border:1px solid #4CAF50; color:#4CAF50; }
.badge-warn{ background: rgba(192,57,43,0.15);  border:1px solid var(--red); color:#E74C3C; }

/* ── GOLD RULE ── */
.gold-rule {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 1.5rem 0;
}

/* ── ORBIT DECORATION ── */
.orbit-deco {
    text-align: center;
    font-size: 0.65rem;
    letter-spacing: 0.4em;
    color: var(--muted);
    text-transform: uppercase;
    margin: 0.5rem 0 2rem;
}
</style>
""", unsafe_allow_html=True)

# ── SPLASH SCREEN ──
# Encode the uploaded solar system image to base64
import base64, os

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

SPLASH_IMG = ""
try:
    img_path = "/mnt/user-data/uploads/1777534463970_image.png"
    if os.path.exists(img_path):
        SPLASH_IMG = img_to_base64(img_path)
except Exception:
    pass

if SPLASH_IMG:
    img_tag = f'<img src="data:image/png;base64,{SPLASH_IMG}" alt="Solar System"/>'
else:
    img_tag = '<div style="font-size:6rem;">🌌</div>'

st.markdown(f"""
<div id="splash-overlay">
    {img_tag}
    <div id="splash-title">Edge AI Negotiation System</div>
    <div id="splash-sub">Energy-Aware Spacecraft Intelligence</div>
    <div id="splash-bar-wrap"><div id="splash-bar"></div></div>
    <div id="splash-status">Initialising Systems…</div>
</div>
""", unsafe_allow_html=True)

# ── STUB IMPORTS (replace with real modules) ──
class EnergyManager:
    def __init__(self, total):
        self.total = total
        self.remaining = total
    def allocate(self, cost):
        if self.remaining >= cost:
            self.remaining -= cost
            return True
        return False

def calculate_scores(anomaly):
    if anomaly:
        return {"Fault Detection": 0.92, "Vision": 0.61, "Navigation": 0.44}
    return {"Fault Detection": 0.38, "Vision": 0.74, "Navigation": 0.85}

def select_module(scores):
    return max(scores, key=scores.get)

def detect_anomalies(df):
    import numpy as np
    col = df.iloc[:, 0]
    return ((col - col.mean()).abs() > 2 * col.std()).astype(int)

# ── LOAD DATA ──
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/opssat.csv")
        df = df.select_dtypes(include=['float64','int64'])
        df = df.ffill().fillna(0).head(1000)
        return df
    except Exception:
        import numpy as np
        rng = np.random.default_rng(42)
        n = 500
        df = pd.DataFrame({
            "Sensor_A": rng.normal(0.5, 0.1, n),
            "Sensor_B": rng.normal(1.2, 0.3, n),
            "Sensor_C": rng.normal(0.8, 0.15, n),
            "Power_mW": rng.normal(45, 8, n),
        })
        df.iloc[120, 0] = 2.5
        df.iloc[340, 1] = 4.1
        return df

data = load_data()
if data is None or data.empty:
    st.stop()

# ── ANOMALY ──
data["anomaly"] = detect_anomalies(data)

if "step" not in st.session_state:
    st.session_state.step = 0

def execute_module(cost, name):
    if st.session_state.manager.allocate(cost):
        st.session_state.last_exec_success = True
        st.session_state.last_cost = cost
        st.session_state.last_name = name
    else:
        st.session_state.last_exec_success = False

current_idx = st.session_state.step % len(data)
window_data = data.iloc[max(0, current_idx-150) : current_idx+1]
if len(window_data) == 0:
    window_data = data.iloc[[0]]

latest = window_data.iloc[-1]
anomaly = bool(latest["anomaly"] == 1)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("## 🔋 Energy Console")
    st.markdown('<div class="gold-rule"></div>', unsafe_allow_html=True)
    energy_total = st.slider("Total Energy Budget", 50, 200, 100)
    if "manager" not in st.session_state or st.session_state.get("last_total") != energy_total:
        st.session_state.manager = EnergyManager(energy_total)
        st.session_state.last_total = energy_total
    energy = st.session_state.manager

    if st.button("⚡ Recharge Battery", use_container_width=True):
        st.session_state.manager = EnergyManager(energy_total)
        energy = st.session_state.manager
    
    is_streaming = st.checkbox("🟢 Enable Real-Time Telemetry", value=False)
    if is_streaming:
        st.session_state.step += 1
    st.markdown('<div class="gold-rule"></div>', unsafe_allow_html=True)

    pct = energy.remaining / energy.total
    st.markdown(f"**Remaining:** {energy.remaining} / {energy.total}")

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=energy.remaining,
        gauge={
            "axis": {"range":[0, energy.total], "tickcolor":"#8A7A60"},
            "bar":  {"color": "#C9A84C"},
            "bgcolor": "#0D1117",
            "steps": [
                {"range":[0, energy.total*0.25], "color":"#2a0a0a"},
                {"range":[energy.total*0.25, energy.total*0.6], "color":"#1a1a0a"},
                {"range":[energy.total*0.6, energy.total], "color":"#0a1a0a"},
            ],
            "threshold": {"line":{"color":"#F0C755","width":2}, "value": energy.total*0.2}
        },
        number={"font":{"color":"#F0C755","size":28}},
        domain={"x":[0,1],"y":[0,1]}
    ))
    fig_gauge.update_layout(
        height=180, margin=dict(l=20,r=20,t=20,b=10),
        paper_bgcolor="rgba(0,0,0,0)", font_color="#8A7A60"
    )
    st.plotly_chart(fig_gauge, width="stretch")

    st.markdown('<div class="gold-rule"></div>', unsafe_allow_html=True)
    st.markdown("### ⚙️ System Info")
    st.markdown(f"""
    <div style='font-size:.82rem; line-height:2; color:#8A7A60;'>
    <b style='color:#C9A84C;'>Platform</b>&nbsp;&nbsp;&nbsp;OPS-SAT<br>
    <b style='color:#C9A84C;'>Model</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Edge AI v2.1<br>
    <b style='color:#C9A84C;'>Records</b>&nbsp;&nbsp;&nbsp;&nbsp;{current_idx+1:,}<br>
    <b style='color:#C9A84C;'>Features</b>&nbsp;&nbsp;&nbsp;{data.shape[1]-1}
    </div>
    """, unsafe_allow_html=True)

# ── HEADER ──
st.markdown("""
<div class="page-header">
    <h1>🚀 Edge AI Negotiation System</h1>
    <p>Energy-Aware Spacecraft Intelligence Platform</p>
</div>
<div class="orbit-deco">◆ &nbsp; Operational &nbsp; ◆ &nbsp; OPS-SAT Mission &nbsp; ◆ &nbsp; Real-Time Analysis &nbsp; ◆</div>
""", unsafe_allow_html=True)

# ── STATUS CARDS ──
c1, c2, c3, c4 = st.columns(4)
c1.metric("📡 Primary Sensor", round(float(latest.iloc[0]), 4))
c2.metric("⚠️ Anomaly Status", "DETECTED" if anomaly else "NOMINAL")
c3.metric("🔋 Energy", f"{energy.remaining} U")
c4.metric("📊 Dataset Size", f"{current_idx+1:,}")

badge_cls = "badge-warn" if anomaly else "badge-ok"
badge_txt = "⚠ Anomaly Detected" if anomaly else "✓ All Systems Nominal"
st.markdown(f'<div style="text-align:right;margin-top:0.5rem;"><span class="status-badge {badge_cls}">{badge_txt}</span></div>', unsafe_allow_html=True)

st.markdown('<div class="gold-rule"></div>', unsafe_allow_html=True)

# ── DATA PREVIEW ──
with st.expander("📋 Dataset Preview", expanded=False):
    st.dataframe(window_data.tail(10), width="stretch")

# ── NEGOTIATION ──
scores = calculate_scores(anomaly)
selected = select_module(scores)

st.markdown("### 🧠 AI Module Negotiation")

plotly_theme = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(13,17,23,0.8)",
    font=dict(family="Times New Roman", color="#8A7A60"),
    title_font=dict(family="Cinzel, Times New Roman", color="#C9A84C", size=14),
    xaxis=dict(gridcolor="rgba(201,168,76,0.08)", zerolinecolor="rgba(201,168,76,0.15)"),
    yaxis=dict(gridcolor="rgba(201,168,76,0.08)", zerolinecolor="rgba(201,168,76,0.15)"),
    margin=dict(t=50, b=30, l=30, r=30),
)

col_a, col_b = st.columns([3, 2])

with col_a:
    df_scores = pd.DataFrame({"Module": list(scores.keys()), "Score": list(scores.values())})
    colors = ["#F0C755" if m == selected else "#C9A84C" for m in df_scores["Module"]]
    fig_scores = go.Figure(go.Bar(
        x=df_scores["Module"], y=df_scores["Score"],
        marker=dict(color=colors, line=dict(color="rgba(201,168,76,0.4)", width=1)),
        text=[f"{v:.0%}" for v in df_scores["Score"]],
        textposition="outside", textfont=dict(color="#F0C755", family="Times New Roman"),
    ))
    fig_scores.update_layout(title="Module Priority Scores", showlegend=False, **plotly_theme)
    fig_scores.update_yaxes(range=[0, 1.15])
    st.plotly_chart(fig_scores, width="stretch")

with col_b:
    fig_radar = go.Figure(go.Scatterpolar(
        r=list(scores.values()) + [list(scores.values())[0]],
        theta=list(scores.keys()) + [list(scores.keys())[0]],
        fill="toself",
        fillcolor="rgba(201,168,76,0.12)",
        line=dict(color="#C9A84C", width=2),
        marker=dict(color="#F0C755", size=8),
    ))
    fig_radar.update_layout(
        title="Capability Radar",
        polar=dict(
            bgcolor="rgba(13,17,23,0.8)",
            radialaxis=dict(visible=True, range=[0,1], gridcolor="rgba(201,168,76,0.15)",
                            tickfont=dict(color="#8A7A60")),
            angularaxis=dict(gridcolor="rgba(201,168,76,0.15)", tickfont=dict(color="#C9A84C")),
        ),
        **{k:v for k,v in plotly_theme.items() if k not in ("xaxis","yaxis")}
    )
    st.plotly_chart(fig_radar, width="stretch")

# ── DECISION ──
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #0d1117, #131926);
    border: 1px solid rgba(201,168,76,0.3);
    border-left: 4px solid #C9A84C;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin: 1rem 0 1.5rem;
    display: flex; align-items: center; gap: 1rem;
">
    <span style="font-size:1.8rem;">🚀</span>
    <div>
        <div style="font-family:'Cinzel',serif;color:#8A7A60;font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;">Selected Module</div>
        <div style="font-family:'Cinzel',serif;color:#F0C755;font-size:1.3rem;letter-spacing:.08em;">{selected}</div>
    </div>
</div>
""", unsafe_allow_html=True)

COSTS = {"Fault Detection": 20, "Vision": 15, "Navigation": 10}
st.button(f"▶ Execute {selected}  ·  Cost: {COSTS[selected]} Units", 
          on_click=execute_module, args=(COSTS[selected], selected))

if "last_exec_success" in st.session_state:
    if st.session_state.last_exec_success:
        name = st.session_state.last_name
        st.success(f"✓ {name} executed locally on Edge AI node — {st.session_state.last_cost} energy units consumed.")
        
        if name == "Vision":
            msg = "Processed 24 MB of raw optical imagery on-board. Transmitted a 12 KB compressed feature map to Earth."
            save = "99.95%"
        elif name == "Fault Detection":
            msg = "Analyzed 10,000 system logs (15 MB) locally. Transmitted a 2 KB anomaly alert to Earth."
            save = "99.98%"
        else:
            msg = "Computed 5,000 trajectory matrices (8 MB) locally. Transmitted the 1 KB final vector to Earth."
            save = "99.99%"
            
        st.info(f"📡 **Edge vs Cloud Communication:** {msg} **Bandwidth saved: {save}**")
    else:
        st.error("✗ Insufficient energy reserves to execute module. Edge processing aborted.")
    del st.session_state["last_exec_success"]

st.markdown('<div class="gold-rule"></div>', unsafe_allow_html=True)

# ── ANOMALY VISUALISATION ──
st.markdown("### 📈 Anomaly Detection Analysis")
col_c, col_d = st.columns(2)

with col_c:
    plot_col = data.columns[0]
    fig_anom = go.Figure()
    normal = window_data[window_data["anomaly"] == 0]
    flagged = window_data[window_data["anomaly"] == 1]
    fig_anom.add_trace(go.Scatter(
        x=normal.index, y=normal[plot_col],
        mode="markers", name="Normal",
        marker=dict(color="#4CAF50", size=4, opacity=0.6)
    ))
    fig_anom.add_trace(go.Scatter(
        x=flagged.index, y=flagged[plot_col],
        mode="markers", name="Anomaly",
        marker=dict(color="#E74C3C", size=9, symbol="x", line=dict(width=2, color="#FF6B6B"))
    ))
    fig_anom.update_layout(title=f"Sensor Readings — {plot_col}", **plotly_theme,
                            legend=dict(font=dict(family="Times New Roman", color="#8A7A60")))
    st.plotly_chart(fig_anom, width="stretch")

with col_d:
    anom_counts = window_data["anomaly"].value_counts().reset_index()
    anom_counts.columns = ["Type", "Count"]
    anom_counts["Label"] = anom_counts["Type"].map({0:"Normal",1:"Anomaly"})
    fig_pie = go.Figure(go.Pie(
        labels=anom_counts["Label"],
        values=anom_counts["Count"],
        hole=0.55,
        marker=dict(colors=["#4CAF50","#E74C3C"],
                    line=dict(color=["#2d6e2d","#8b2020"], width=2)),
        textfont=dict(family="Times New Roman", color="#E8DCC8"),
    ))
    fig_pie.update_layout(
        title="Anomaly Distribution",
        legend=dict(font=dict(family="Times New Roman", color="#8A7A60")),
        **{k:v for k,v in plotly_theme.items() if k not in ("xaxis","yaxis")}
    )
    st.plotly_chart(fig_pie, width="stretch")

# ── MULTI-SENSOR TIMELINE ──
st.markdown("### 📡 Multi-Sensor Timeline")
sensor_cols = [c for c in window_data.columns if c != "anomaly"][:4]
fig_multi = go.Figure()
palette = ["#C9A84C","#E8763A","#4A9EBF","#9B7FD4"]
for i, col in enumerate(sensor_cols):
    fig_multi.add_trace(go.Scatter(
        x=window_data.index, y=window_data[col], name=col,
        line=dict(color=palette[i % len(palette)], width=1.5),
        mode="lines"
    ))
fig_multi.update_layout(title="Sensor Streams — Last 1000 Samples",
    legend=dict(font=dict(family="Times New Roman",color="#8A7A60")), **plotly_theme)
st.plotly_chart(fig_multi, width="stretch")

# ── ENERGY USAGE ──
st.markdown('<div class="gold-rule"></div>', unsafe_allow_html=True)
st.markdown("### 🔋 Energy Budget Overview")

used = energy.total - energy.remaining
fig_energy = go.Figure(go.Pie(
    labels=["Consumed","Remaining"],
    values=[used, energy.remaining],
    hole=0.65,
    marker=dict(colors=["#E8763A","#1a2a1a"],
                line=dict(color=["#C0392B","#2d5a2d"], width=2)),
    textfont=dict(family="Times New Roman", color="#E8DCC8"),
))
fig_energy.update_layout(
    title="Energy Distribution",
    annotations=[dict(text=f"{energy.remaining}U<br>Left",
                      font=dict(size=16, family="Cinzel", color="#F0C755"),
                      showarrow=False)],
    legend=dict(font=dict(family="Times New Roman", color="#8A7A60")),
    **{k:v for k,v in plotly_theme.items() if k not in ("xaxis","yaxis")}
)
st.plotly_chart(fig_energy, width="stretch")

# ── FOOTER ──
if is_streaming:
    time.sleep(1.0)
    st.rerun()

st.markdown('<div class="gold-rule"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding: 1.5rem 0 2rem; color:#8A7A60;">
    <div style="font-family:'Cinzel',serif; color:#C9A84C; letter-spacing:.2em; font-size:.85rem; text-transform:uppercase;">
        Edge AI · Spacecraft Simulation · Energy-Aware Intelligence
    </div>
    <div style="font-size:.72rem; letter-spacing:.3em; margin-top:.5rem; text-transform:uppercase;">
        ◆ &nbsp; OPS-SAT Mission Platform &nbsp; ◆
    </div>
</div>
""", unsafe_allow_html=True)