import sys
import time

content = open('app.py', 'r', encoding='utf-8').read()

c1 = '''# ── ANOMALY ──
data["anomaly"] = detect_anomalies(data)
latest = data.iloc[-1]
anomaly = bool(latest["anomaly"] == 1)'''
r1 = '''# ── ANOMALY ──
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
anomaly = bool(latest["anomaly"] == 1)'''
content = content.replace(c1, r1)

c2 = '''    energy_total = st.slider("Total Energy Budget", 50, 200, 100)
    energy = EnergyManager(energy_total)'''
r2 = '''    energy_total = st.slider("Total Energy Budget", 50, 200, 100)
    if "manager" not in st.session_state or st.session_state.get("last_total") != energy_total:
        st.session_state.manager = EnergyManager(energy_total)
        st.session_state.last_total = energy_total
    energy = st.session_state.manager

    if st.button("⚡ Recharge Battery", use_container_width=True):
        st.session_state.manager = EnergyManager(energy_total)
        energy = st.session_state.manager
    
    is_streaming = st.checkbox("🟢 Enable Real-Time Telemetry", value=False)
    if is_streaming:
        st.session_state.step += 1'''
content = content.replace(c2, r2)

c3 = '''    <b style='color:#C9A84C;'>Records</b>&nbsp;&nbsp;&nbsp;&nbsp;{len(data):,}<br>
    <b style='color:#C9A84C;'>Features</b>&nbsp;&nbsp;&nbsp;{data.shape[1]-1}'''
r3 = '''    <b style='color:#C9A84C;'>Records</b>&nbsp;&nbsp;&nbsp;&nbsp;{current_idx+1:,}<br>
    <b style='color:#C9A84C;'>Features</b>&nbsp;&nbsp;&nbsp;{data.shape[1]-1}'''
content = content.replace(c3, r3)

c4 = '''c4.metric("📊 Dataset Size", f"{len(data):,}")'''
r4 = '''c4.metric("📊 Dataset Size", f"{current_idx+1:,}")'''
content = content.replace(c4, r4)

c5 = '''with st.expander("📋 Dataset Preview", expanded=False):
    st.dataframe(data.head(10), width="stretch")'''
r5 = '''with st.expander("📋 Dataset Preview", expanded=False):
    st.dataframe(window_data.tail(10), width="stretch")'''
content = content.replace(c5, r5)

c6 = '''COSTS = {"Fault Detection": 20, "Vision": 15, "Navigation": 10}
if st.button(f"▶ Execute {selected}  ·  Cost: {COSTS[selected]} Units"):
    if energy.allocate(COSTS[selected]):
        st.success(f"✓ {selected} executed successfully — {COSTS[selected]} energy units consumed.")
    else:
        st.error("✗ Insufficient energy reserves to execute module.")'''
r6 = '''COSTS = {"Fault Detection": 20, "Vision": 15, "Navigation": 10}
st.button(f"▶ Execute {selected}  ·  Cost: {COSTS[selected]} Units", 
          on_click=execute_module, args=(COSTS[selected], selected))

if "last_exec_success" in st.session_state:
    if st.session_state.last_exec_success:
        st.success(f"✓ {st.session_state.last_name} executed locally on Edge AI node — {st.session_state.last_cost} energy units consumed.")
        st.info("📡 **Edge vs Cloud Communication:** Processed 12.5 MB of raw sensor telemetry on-board. Transmitted only 4 KB of actionable intelligence to the Ground Station. **Bandwidth saved: 99.96%**.")
    else:
        st.error("✗ Insufficient energy reserves to execute module. Edge processing aborted.")
    del st.session_state["last_exec_success"]'''
content = content.replace(c6, r6)

c7 = '''    normal = data[data["anomaly"] == 0]
    flagged = data[data["anomaly"] == 1]'''
r7 = '''    normal = window_data[window_data["anomaly"] == 0]
    flagged = window_data[window_data["anomaly"] == 1]'''
content = content.replace(c7, r7)

c8 = '''with col_d:
    anom_counts = data["anomaly"].value_counts().reset_index()'''
r8 = '''with col_d:
    anom_counts = window_data["anomaly"].value_counts().reset_index()'''
content = content.replace(c8, r8)

c9 = '''# ── MULTI-SENSOR TIMELINE ──
st.markdown("### 📡 Multi-Sensor Timeline")
sensor_cols = [c for c in data.columns if c != "anomaly"][:4]
fig_multi = go.Figure()
palette = ["#C9A84C","#E8763A","#4A9EBF","#9B7FD4"]
for i, col in enumerate(sensor_cols):
    fig_multi.add_trace(go.Scatter(
        x=data.index, y=data[col], name=col,'''
r9 = '''# ── MULTI-SENSOR TIMELINE ──
st.markdown("### 📡 Multi-Sensor Timeline")
sensor_cols = [c for c in window_data.columns if c != "anomaly"][:4]
fig_multi = go.Figure()
palette = ["#C9A84C","#E8763A","#4A9EBF","#9B7FD4"]
for i, col in enumerate(sensor_cols):
    fig_multi.add_trace(go.Scatter(
        x=window_data.index, y=window_data[col], name=col,'''
content = content.replace(c9, r9)

c10 = '''# ── FOOTER ──
st.markdown('<div class="gold-rule"></div>', unsafe_allow_html=True)'''
r10 = '''# ── FOOTER ──
if is_streaming:
    time.sleep(1.0)
    st.rerun()

st.markdown('<div class="gold-rule"></div>', unsafe_allow_html=True)'''
content = content.replace(c10, r10)

open('app.py', 'w', encoding='utf-8').write(content)
print('Done!')
