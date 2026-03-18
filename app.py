"""
Digital Twin Dashboard - CAT C4.4 Engine
Master's Thesis Project: Predictive Maintenance Framework
Author: INYA-OKO, RAYMOND EKUMA
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))
from helpers import (
    SensorDataGenerator,
    HealthStatusCalculator,
    MLModelResults,
    CostBenefitAnalysis,
    get_current_state_profile,
    STATE_CYCLE,
    format_number, format_percent, format_currency
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Digital Twin Dashboard - INYA-OKO, RAYMOND EKUMA",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main-header   { text-align:center; color:#1f77b4; margin-bottom:20px; }
.dev-credit    { text-align:center; color:#666; font-size:13px; padding:8px;
                 background:#f0f0f0; border-radius:5px; margin-bottom:10px; }
.state-banner  { text-align:center; font-size:22px; font-weight:bold;
                 padding:14px; border-radius:8px; margin-bottom:16px;
                 color:#fff; letter-spacing:1px; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if 'sensor_data' not in st.session_state:
    gen = SensorDataGenerator()
    st.session_state.sensor_data = gen.generate_data(n_samples=1000)
    st.session_state.generator   = gen

if 'ml_results' not in st.session_state:
    st.session_state.ml_results = MLModelResults.get_mock_results()

# ── Get current live state ────────────────────────────────────────────────────
state_profile = get_current_state_profile()

# Append one live reading to rolling buffer
st.session_state.sensor_data = st.session_state.generator.append_live_reading(
    st.session_state.sensor_data, state_profile
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.title("🔧 Digital Twin Dashboard")
st.sidebar.markdown("**By INYA-OKO, RAYMOND EKUMA**")
st.sidebar.markdown("Master's Thesis Project")
st.sidebar.markdown("---")

# Live state indicator in sidebar
sb_color = state_profile['color']
st.sidebar.markdown(
    f"<div style='background:{sb_color};color:#fff;padding:10px;border-radius:6px;"
    f"text-align:center;font-weight:bold;font-size:15px;'>"
    f"{state_profile['emoji']} ENGINE: {state_profile['state']}</div>",
    unsafe_allow_html=True
)
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "📈 Real-Time Monitoring", "🤖 Analytics",
     "🔧 Engine Diagnostics", "📋 Documentation", "👨‍💻 About Developer"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Project Info
- **Framework:** Streamlit + Python
- **ML Models:** Random Forest & ANN
- **Data Source:** Kaggle
- **Deployment:** Streamlit Cloud
""")
st.sidebar.markdown(
    "<div class='dev-credit'><strong>INYA-OKO, RAYMOND EKUMA</strong><br>"
    "Digital Twin — CAT C4.4 Engine</div>",
    unsafe_allow_html=True
)

# ── AUTO-REFRESH every 10 seconds ────────────────────────────────────────────
import time as _time
from helpers import TOTAL_CYCLE_DURATION, STATE_CYCLE as _SC
_elapsed   = int(_time.time()) % TOTAL_CYCLE_DURATION
_cum       = 0
_remaining = 10
for _s in _SC:
    _cum += _s['duration']
    if _elapsed < _cum:
        _remaining = _cum - _elapsed
        break
st.sidebar.markdown(f"🔄 **Next update in:** `{_remaining}s`")

time.sleep(0)
_trigger = st.empty()

# ═════════════════════════════════════════════════════════════════════════════
# DIAGNOSTICS DATA  — cause list keyed by engine state
# ═════════════════════════════════════════════════════════════════════════════
DIAGNOSTICS = {

    # ── DEGRADED: early warning — maintenance DUE SOON ──────────────────────
    "DEGRADED": {
        "banner_msg": "⚠️ Engine is in DEGRADED state — maintenance required soon to prevent escalation to CRITICAL.",
        "banner_color": "#e67e22",
        "sections": [
            {
                "sensor": "🌡 Oil Temperature (elevated)",
                "alert": "Oil temperature rising above normal band (>100 °C). Act now before reaching critical threshold.",
                "causes": [
                    "Oil level dropping — check dipstick and top up immediately.",
                    "Oil filter becoming clogged — schedule replacement within next service.",
                    "Oil viscosity may be incorrect for current operating temperature.",
                    "Cooling system efficiency declining — check coolant level and radiator fins.",
                ],
                "actions": [
                    "Check oil level on dipstick — top up to MAX with correct grade (15W-40).",
                    "Inspect oil filter — replace if last changed more than 250 hours ago.",
                    "Verify coolant level in expansion tank — top up if below MIN mark.",
                    "Schedule a full oil and filter service within the next 50 operating hours.",
                ]
            },
            {
                "sensor": "📳 Vibration (increasing)",
                "alert": "Vibration trending upward (approaching 4 g). Investigate mounting and couplings.",
                "causes": [
                    "Engine mounting bolts may be loosening over time.",
                    "Drive coupling alignment drifting — common after high-load periods.",
                    "Early bearing wear — detectable at this stage before it worsens.",
                ],
                "actions": [
                    "Inspect and torque all engine mounting bolts to specification.",
                    "Check coupling alignment with a dial gauge — correct if angular error exceeds tolerance.",
                    "Take an oil sample and send for analysis — early bearing wear shows as elevated copper/lead.",
                    "Log vibration readings and compare trend over next 10 operating hours.",
                ]
            },
            {
                "sensor": "🛢 Oil Pressure (slightly low)",
                "alert": "Oil pressure approaching lower limit (200 kPa). Monitor closely.",
                "causes": [
                    "Oil level slightly low — pump beginning to cavitate at low idle.",
                    "Oil filter partially blocked — flow restriction reducing downstream pressure.",
                    "Oil viscosity thinning due to fuel dilution or overheating.",
                ],
                "actions": [
                    "Top up oil to MAX on the dipstick.",
                    "Replace the oil filter.",
                    "Check for fuel smell in the oil — if confirmed, inspect injectors for dribbling.",
                    "Monitor pressure at idle and under load over the next operating shift.",
                ]
            },
            {
                "sensor": "⛽ Fuel Pressure (slightly low)",
                "alert": "Fuel pressure trending below normal (below 1500 kPa). Primary fuel filter likely due.",
                "causes": [
                    "Primary fuel filter nearing end of service life.",
                    "Water accumulation in the water separator bowl.",
                    "Fuel tank level low — pump intermittently drawing air.",
                ],
                "actions": [
                    "Replace primary and secondary fuel filters.",
                    "Drain the water separator bowl.",
                    "Check fuel tank level — refuel if below 25%.",
                    "Prime the fuel system with the hand primer pump after filter change.",
                ]
            },
        ]
    },

    # ── CRITICAL: final warning — act immediately ────────────────────────────
    "CRITICAL": {
        "banner_msg": "🚨 Engine is in CRITICAL state — immediate action required. Do NOT continue operating without addressing the faults below.",
        "banner_color": "#c0392b",
        "sections": [
            {
                "sensor": "🌡 Oil Temperature CRITICAL (>120 °C)",
                "alert": "Oil temperature in the danger zone. Continued operation risks seizure.",
                "causes": [
                    "Severely low oil level — pump cavitating and oil film breaking down.",
                    "Oil cooler or heat exchanger blocked — heat not dissipating.",
                    "Coolant system failure — thermostat stuck or coolant pump failed.",
                    "Wrong oil viscosity or severely degraded oil.",
                ],
                "actions": [
                    "STOP THE ENGINE immediately if oil temperature exceeds 120 °C.",
                    "Allow to cool for 20 minutes — do NOT open any caps while hot.",
                    "Check oil level and top up to MAX with correct grade.",
                    "Inspect the oil cooler and heat exchanger for blockage — flush if necessary.",
                    "Check coolant level and thermostat function before restarting.",
                    "Do not restart until temperature is confirmed stable.",
                ]
            },
            {
                "sensor": "🌡 Coolant Temperature CRITICAL (>105 °C)",
                "alert": "Engine overheating. Risk of head gasket failure and severe engine damage.",
                "causes": [
                    "Low coolant level — possibly a leak in hoses, radiator, or water pump seal.",
                    "Thermostat stuck closed — coolant not flowing to radiator.",
                    "Water pump impeller damaged or pump drive failed.",
                    "Clogged radiator core — airflow severely restricted.",
                    "Jasco pump or pump fork damaged.",
                ],
                "actions": [
                    "STOP the engine. Do NOT open the radiator cap — severe scalding risk.",
                    "Wait 20 minutes. Then check coolant level in the expansion tank only.",
                    "Inspect all coolant hoses for splits, leaks, or collapsed sections.",
                    "Test thermostat by placing in boiling water — replace if it does not open.",
                    "Inspect water pump for leaking shaft seal or damaged impeller.",
                    "Check radiator core externally for debris — blow out with compressed air.",
                    "Pressure-test the cooling circuit before returning to service.",
                ]
            },
            {
                "sensor": "📳 Vibration CRITICAL (>4 g)",
                "alert": "Severe vibration detected. Risk of structural damage and bearing failure.",
                "causes": [
                    "Bearing failure — big-end or main bearing severely worn.",
                    "Engine mount rubber sheared — engine rocking on its mounts.",
                    "Coupling severely misaligned — possibly after a mechanical shock event.",
                ],
                "actions": [
                    "STOP the engine — severe vibration indicates imminent mechanical failure.",
                    "Do NOT restart until the root cause is confirmed.",
                    "Inspect all engine mounts for sheared rubber or loose bolts.",
                    "Check coupling alignment — misalignment above 0.1 mm TIR requires immediate correction.",
                    "Pull oil sample urgently — if copper/lead levels are high, engine requires bottom-end inspection.",
                    "If bearing knock is audible, the engine requires removal for rebuild — do not operate.",
                ]
            },
            {
                "sensor": "🛢 Oil Pressure CRITICAL (<200 kPa)",
                "alert": "Oil pressure below safe limit. Bearing lubrication is compromised.",
                "causes": [
                    "Oil pump failed — gears worn or drive shaft broken.",
                    "Major external oil leak — sump, gasket, or seal failure.",
                    "Pressure relief valve stuck open.",
                    "Severely blocked oil filter or gallery.",
                ],
                "actions": [
                    "STOP the engine immediately — low oil pressure causes bearing damage within seconds.",
                    "Check for visible oil leaks under the engine before doing anything else.",
                    "Check oil level on dipstick — top up if low.",
                    "If oil level is correct and pressure is still low, the oil pump has likely failed.",
                    "Remove and inspect the oil pump — replace if gear clearances exceed specification.",
                    "Prime the new pump with oil before fitting to prevent a dry-start.",
                    "Replace oil and filter after pump work.",
                ]
            },
            {
                "sensor": "🌬 EGT CRITICAL (>500 °C)",
                "alert": "Exhaust gas temperature dangerously high. Risk of turbocharger and exhaust manifold damage.",
                "causes": [
                    "Turbocharger not delivering boost — engine over-fuelling to compensate.",
                    "Injector dribbling or incorrect spray pattern — unburnt fuel entering exhaust.",
                    "Blocked exhaust system — backpressure preventing gas escape.",
                    "Air intake severely restricted — rich combustion mixture.",
                ],
                "actions": [
                    "Reduce engine load immediately to bring EGT below 450 °C.",
                    "Check boost pressure at the inlet manifold — compare to specification.",
                    "Inspect turbocharger for shaft play, blade damage, or oil seal leaks.",
                    "Remove injectors for flow test and spray pattern check — replace any dribbling injectors.",
                    "Check exhaust manifold and silencer for blockage — clear if necessary.",
                    "Replace air filter element.",
                    "If EGT does not reduce after the above steps, shut down and send for specialist inspection.",
                ]
            },
            {
                "sensor": "⚡ RPM CRITICAL (out of governed range)",
                "alert": "Engine speed outside governed range. Runaway or governor failure suspected.",
                "causes": [
                    "Governor malfunction — speed not being limited correctly.",
                    "Faulty AVR (Automatic Voltage Regulator) causing speed hunting.",
                    "Fuel system delivering excessive fuel.",
                ],
                "actions": [
                    "If engine is over-speeding (RPM HIGH): use the EMERGENCY STOP immediately — do not wait.",
                    "Do NOT attempt to reload the engine until governor has been inspected and repaired.",
                    "Check electronic governor actuator wiring and speed sensor connections.",
                    "If RPM is LOW: check fuel supply, replace filters, and inspect governor linkage for binding.",
                    "Recalibrate or replace governor — do not return to service until RPM is stable under load.",
                ]
            },
        ]
    },

    # ── RECOVERY: post-event checks ──────────────────────────────────────────
    "RECOVERY": {
        "banner_msg": "🔵 Engine is in RECOVERY state — faults have been addressed. Carry out these verification checks before returning to full operation.",
        "banner_color": "#2980b9",
        "sections": [
            {
                "sensor": "✅ Post-event verification checklist",
                "alert": "Engine has returned from CRITICAL or DEGRADED state. Confirm all parameters are stable before resuming full load.",
                "causes": [
                    "Recent over-temperature event may have stressed head gasket or oil seals.",
                    "Oil or coolant may need topping up after fault resolution.",
                    "Replaced components (pump, filter, thermostat) need bedding-in monitoring.",
                ],
                "actions": [
                    "Run engine at idle for 10 minutes — confirm all temperatures stabilise within normal bands.",
                    "Check for any new oil or coolant leaks that may have developed during the fault event.",
                    "Verify oil pressure reads above 200 kPa within 5 seconds of cold start.",
                    "Confirm EGT is below 450 °C at 75% load before applying full load.",
                    "Take an oil sample and send for analysis to check for coolant contamination or metal particles.",
                    "Log all fault events, corrective actions taken, and sensor readings in the maintenance record.",
                    "Schedule a full service inspection within the next 50 operating hours.",
                ]
            },
        ]
    },

    # ── NORMAL: healthy state ────────────────────────────────────────────────
    "NORMAL": {
        "banner_msg": "✅ Engine is operating normally. All sensors within normal range. No maintenance action required at this time.",
        "banner_color": "#27ae60",
        "sections": []
    },
}


# ── Helper: render diagnostics panel for a given state ────────────────────────
def render_diagnostics(current_state: str, sensor_readings: dict):
    data = DIAGNOSTICS.get(current_state, DIAGNOSTICS["NORMAL"])

    # Coloured banner
    st.markdown(
        f"<div style='background:{data['banner_color']};color:#fff;padding:16px 20px;"
        f"border-radius:8px;font-size:16px;font-weight:bold;margin-bottom:20px;'>"
        f"{data['banner_msg']}</div>",
        unsafe_allow_html=True
    )

    if not data["sections"]:
        st.success("All sensors within normal operating range. Continue monitoring.")
        st.info("The digital twin will alert you automatically when any sensor moves into the DEGRADED band.")
        return

    # Show live sensor readings summary at top
    with st.expander("📊 Current sensor readings — quick reference", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Oil Temp",    f"{sensor_readings.get('oil_temperature', 0):.1f} °C",
                  "⚠️ High" if sensor_readings.get('oil_temperature', 0) > 100 else "✅ OK")
        c2.metric("Coolant",     f"{sensor_readings.get('coolant_temperature', 0):.1f} °C",
                  "⚠️ High" if sensor_readings.get('coolant_temperature', 0) > 100 else "✅ OK")
        c3.metric("Oil Pressure",f"{sensor_readings.get('oil_pressure', 0):.0f} kPa",
                  "⚠️ Low" if sensor_readings.get('oil_pressure', 0) < 200 else "✅ OK")
        c4.metric("Vibration",   f"{sensor_readings.get('vibration', 0):.2f} g",
                  "⚠️ High" if sensor_readings.get('vibration', 0) > 4 else "✅ OK")
        c1, c2, c3 = st.columns(3)
        c1.metric("EGT",         f"{sensor_readings.get('egt', 0):.1f} °C",
                  "⚠️ High" if sensor_readings.get('egt', 0) > 500 else "✅ OK")
        c2.metric("Fuel Pressure",f"{sensor_readings.get('fuel_pressure', 0):.0f} kPa",
                  "⚠️ Low" if sensor_readings.get('fuel_pressure', 0) < 1500 else "✅ OK")
        c3.metric("RPM",         f"{sensor_readings.get('rpm', 0):.0f}",
                  "⚠️ Out of range" if not (1200 <= sensor_readings.get('rpm', 1500) <= 1800) else "✅ OK")

    st.markdown("---")

    # Each fault section as an expander
    for section in data["sections"]:
        with st.expander(f"{section['sensor']}", expanded=True):
            # Alert box
            alert_color = "#fff3cd" if current_state == "DEGRADED" else (
                          "#fde8e8" if current_state == "CRITICAL" else "#d1ecf1")
            alert_border = "#e67e22" if current_state == "DEGRADED" else (
                           "#c0392b" if current_state == "CRITICAL" else "#2980b9")
            st.markdown(
                f"<div style='background:{alert_color};border-left:4px solid {alert_border};"
                f"padding:10px 14px;border-radius:4px;margin-bottom:14px;'>"
                f"<strong>Alert:</strong> {section['alert']}</div>",
                unsafe_allow_html=True
            )

            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown("**🔍 Possible causes**")
                for i, cause in enumerate(section["causes"], 1):
                    st.markdown(f"{i}. {cause}")

            with col_b:
                st.markdown("**🛠️ Corrective actions — carry out in order**")
                for i, action in enumerate(section["actions"], 1):
                    step_color = "#c0392b" if current_state == "CRITICAL" else "#e67e22"
                    st.markdown(
                        f"<div style='display:flex;gap:10px;margin-bottom:8px;align-items:flex-start'>"
                        f"<span style='background:{step_color};color:#fff;border-radius:50%;"
                        f"width:22px;height:22px;display:flex;align-items:center;justify-content:center;"
                        f"font-size:11px;font-weight:bold;flex-shrink:0'>{i}</span>"
                        f"<span style='font-size:13px;line-height:1.5'>{action}</span></div>",
                        unsafe_allow_html=True
                    )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.markdown('<h1 class="main-header">🔧 Digital Twin Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(
        '<div class="dev-credit"><strong>Predictive Maintenance Framework — Caterpillar C4.4 Engine</strong>'
        '<br><em>INYA-OKO, RAYMOND EKUMA</em></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='state-banner' style='background:{state_profile['color']};'>"
        f"{state_profile['emoji']}  CURRENT ENGINE STATE: {state_profile['state']}</div>",
        unsafe_allow_html=True
    )

    ml = st.session_state.ml_results
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Model Accuracy",       f"{ml['random_forest']['accuracy']*100:.2f}%", "Random Forest")
    c2.metric("RUL Prediction Error",  f"{ml['ann']['mae']:.4f}h",                   "MAE (hours)")
    c3.metric("R² Score",              f"{ml['ann']['r2_score']:.4f}",               "Neural Network")
    c4.metric("Cost Savings",          format_percent(ml['cost_benefit']['savings_percentage']), "Annual")

    st.markdown("---")

    st.subheader("📅 Engine State Cycle (90-second loop)")
    elapsed_now = int(_time.time()) % TOTAL_CYCLE_DURATION
    cum = 0
    timeline_fig = go.Figure()
    for i, s in enumerate(_SC):
        start = cum
        end   = cum + s['duration']
        timeline_fig.add_shape(type="rect",
            x0=start, x1=end, y0=0, y1=1,
            fillcolor=s['color'], opacity=0.25, line_width=0)
        timeline_fig.add_annotation(
            x=(start+end)/2, y=0.5,
            text=f"{s['emoji']} {s['state']}<br>{s['duration']}s",
            showarrow=False, font=dict(size=12, color=s['color']), yref="paper")
        cum += s['duration']
    timeline_fig.add_shape(type="line",
        x0=elapsed_now, x1=elapsed_now, y0=0, y1=1,
        line=dict(color="black", width=3, dash="dash"), yref="paper")
    timeline_fig.add_annotation(x=elapsed_now, y=1.05, text="▼ NOW",
        showarrow=False, font=dict(size=11, color="black"), yref="paper")
    timeline_fig.update_layout(
        height=100, margin=dict(t=30, b=10, l=10, r=10),
        xaxis=dict(range=[0, TOTAL_CYCLE_DURATION], showticklabels=False),
        yaxis=dict(showticklabels=False, range=[0,1]),
        plot_bgcolor="white", showlegend=False
    )
    st.plotly_chart(timeline_fig, use_container_width=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📌 Project Overview")
        st.write("""
        The Digital Twin Dashboard is a comprehensive framework for predictive maintenance
        of the Caterpillar C4.4 diesel engine. This application combines machine learning,
        IoT sensor integration, and real-time visualization to enable condition-based
        maintenance scheduling.

        **Key Features:**
        - Live engine state simulation (NORMAL → DEGRADED → CRITICAL → RECOVERY)
        - Real-time sensor monitoring with 10-second refresh
        - ML-based anomaly detection & RUL prediction
        - Maintenance scheduling & cost-benefit analysis
        """)
    with c2:
        st.subheader("🎯 Key Results (Chapter 4 — Actual Kaggle Output)")
        for metric, desc in [
            ("100.00%",  "RF Classifier Accuracy (class-imbalance artefact)"),
            ("32.01h",   "ANN RUL Prediction Error (MAE)"),
            ("67.5%",    "Cost Reduction vs Conventional Maintenance"),
            ("€162,000", "Annual Savings per Engine"),
        ]:
            st.write(f"**{metric}** — {desc}")

    st.markdown("---")
    st.subheader("🛠️ Technology Stack")
    c1, c2, c3, c4 = st.columns(4)
    c1.write("**Frontend**\n• Streamlit\n• Plotly\n• Pandas")
    c2.write("**ML & Data**\n• Python\n• Scikit-learn\n• TensorFlow")
    c3.write("**Data Processing**\n• NumPy\n• Pandas\n• Seaborn")
    c4.write("**Deployment**\n• Streamlit Cloud\n• Kaggle\n• GitHub")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: REAL-TIME MONITORING
# ═════════════════════════════════════════════════════════════════════════════
elif page == "📈 Real-Time Monitoring":
    st.title("📈 Real-Time Engine Monitoring")
    st.markdown(f"**INYA-OKO, RAYMOND EKUMA** — Live sensor data | "
                f"Last updated: `{datetime.now().strftime('%H:%M:%S')}`")
    st.markdown("---")

    st.markdown(
        f"<div class='state-banner' style='background:{state_profile['color']};'>"
        f"{state_profile['emoji']}  ENGINE STATE: {state_profile['state']}  {state_profile['emoji']}</div>",
        unsafe_allow_html=True
    )

    latest = st.session_state.sensor_data.iloc[-1]

    health_status, health_score, health_emoji = HealthStatusCalculator.get_health_status({
        'oil_temperature': latest['oil_temperature'],
        'egt':             latest['egt'],
        'vibration':       latest['vibration'],
        'oil_pressure':    latest['oil_pressure'],
    })
    rul = HealthStatusCalculator.calculate_rul(health_score)
    rec = HealthStatusCalculator.get_maintenance_recommendation(rul)

    c1, c2, c3 = st.columns(3)
    c1.metric("Engine Health",   f"{health_emoji} {health_status}", "Current")
    c2.metric("RUL Estimate",    f"{rul:.1f} h",                    "Remaining Useful Life")
    with c3:
        st.write("**Maintenance Recommendation**")
        st.info(rec)

    st.markdown("---")
    st.subheader("Current Sensor Readings")

    def delta_label(sensor, value, normal_range):
        lo, hi = normal_range
        if value < lo or value > hi:
            return f"⚠️ Out of range ({lo}–{hi})"
        return f"✅ Normal ({lo}–{hi})"

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Oil Temperature",    f"{latest['oil_temperature']:.1f} °C",   delta_label("oil_temp",    latest['oil_temperature'],    (70, 100)))
    c2.metric("Coolant Temperature",f"{latest['coolant_temperature']:.1f} °C",delta_label("coolant",    latest['coolant_temperature'], (80, 100)))
    c3.metric("EGT",                f"{latest['egt']:.1f} °C",               delta_label("egt",         latest['egt'],                 (300, 500)))
    c4.metric("Vibration",          f"{latest['vibration']:.2f} g",          delta_label("vibration",   latest['vibration'],           (0, 4)))

    c1, c2, c3 = st.columns(3)
    c1.metric("Oil Pressure",  f"{latest['oil_pressure']:.0f} kPa",  delta_label("oil_p",  latest['oil_pressure'],  (200, 400)))
    c2.metric("Fuel Pressure", f"{latest['fuel_pressure']:.0f} kPa", delta_label("fuel_p", latest['fuel_pressure'], (1500, 2000)))
    c3.metric("RPM",           f"{latest['rpm']:.0f}",               delta_label("rpm",    latest['rpm'],           (1200, 1800)))

    st.markdown("---")
    st.subheader("📉 Sensor Trends — Last 100 Readings")
    st.caption(f"State coloring reflects engine condition. Current state: **{state_profile['state']}**")

    recent = st.session_state.sensor_data.tail(100).copy().reset_index(drop=True)
    recent['index'] = range(len(recent))
    sc = state_profile['color']

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=recent['index'], y=recent['oil_temperature'],
            name='Oil Temp', line=dict(color=sc, width=2)))
        fig.add_trace(go.Scatter(x=recent['index'], y=recent['coolant_temperature'],
            name='Coolant Temp', line=dict(color='#4ECDC4', width=2, dash='dot')))
        fig.add_hline(y=100, line_dash="dash", line_color="red",   annotation_text="Oil Temp Limit 100°C")
        fig.update_layout(title="Temperature Sensors", xaxis_title="Reading Index",
            yaxis_title="°C", hovermode='x unified', height=380)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=recent['index'], y=recent['vibration'],
            name='Vibration', line=dict(color=sc, width=2),
            fill='tozeroy', fillcolor=sc.replace(')', ',0.1)').replace('rgb','rgba') if 'rgb' in sc else sc))
        fig.add_hline(y=4, line_dash="dash", line_color="red", annotation_text="Vibration Limit 4g")
        fig.update_layout(title="Vibration Level", xaxis_title="Reading Index",
            yaxis_title="g", hovermode='x unified', height=380)
        st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=recent['index'], y=recent['oil_pressure'],
            name='Oil Pressure', line=dict(color=sc, width=2)))
        fig.add_trace(go.Scatter(x=recent['index'], y=recent['fuel_pressure'],
            name='Fuel Pressure', line=dict(color='#4D96FF', width=2, dash='dot'),
            yaxis='y2'))
        fig.add_hline(y=200, line_dash="dash", line_color="red", annotation_text="Oil Pressure Min 200kPa")
        fig.update_layout(title="Pressure Sensors", xaxis_title="Reading Index",
            yaxis_title="Oil Pressure (kPa)", hovermode='x unified', height=380,
            yaxis2=dict(title="Fuel Pressure (kPa)", overlaying='y', side='right'))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=recent['index'], y=recent['egt'],
            name='EGT', line=dict(color=sc, width=2)))
        fig.add_hline(y=500, line_dash="dash", line_color="red", annotation_text="EGT Limit 500°C")
        fig.update_layout(title="Exhaust Gas Temperature (EGT)", xaxis_title="Reading Index",
            yaxis_title="°C", hovermode='x unified', height=380)
        st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recent['index'], y=recent['rpm'],
        name='RPM', line=dict(color=sc, width=2)))
    fig.add_hrect(y0=1200, y1=1800, fillcolor="green", opacity=0.08,
        annotation_text="Normal RPM Range", annotation_position="top left")
    fig.update_layout(title="Engine RPM", xaxis_title="Reading Index",
        yaxis_title="RPM", hovermode='x unified', height=280)
    st.plotly_chart(fig, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🤖 Analytics":
    st.title("🤖 Machine Learning Analytics")
    st.markdown("**INYA-OKO, RAYMOND EKUMA** — Results from actual Kaggle notebook output (Chapter 4)")
    st.markdown("---")

    ml = st.session_state.ml_results

    st.subheader("Model Performance Metrics")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Random Forest Classifier (Anomaly Detection)**")
        for m, v in [
            ("Accuracy",  f"{ml['random_forest']['accuracy']*100:.2f}%"),
            ("Precision", f"{ml['random_forest']['precision']*100:.2f}%"),
            ("Recall",    f"{ml['random_forest']['recall']*100:.2f}%"),
            ("F1-Score",  f"{ml['random_forest']['f1_score']*100:.2f}%"),
            ("AUC-ROC",   "NaN (class imbalance)"),
        ]:
            st.write(f"• {m}: **{v}**")
    with c2:
        st.write("**Artificial Neural Network (RUL Prediction)**")
        for m, v in [
            ("MAE",      f"{ml['ann']['mae']:.4f} hours"),
            ("RMSE",     f"{ml['ann']['rmse']:.4f} hours"),
            ("R² Score", f"{ml['ann']['r2_score']:.4f}"),
            ("MAPE",     f"{ml['ann']['mape']*100:.2f}%"),
        ]:
            st.write(f"• {m}: **{v}**")

    st.markdown("---")
    st.subheader("Feature Importance")
    features    = list(ml['feature_importance'].keys())
    importances = list(ml['feature_importance'].values())
    fig = go.Figure(go.Bar(x=importances, y=features, orientation='h',
        marker=dict(color='#1f77b4')))
    fig.update_layout(title="Feature Importance in Anomaly Detection",
        xaxis_title="Importance Score", height=350)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("RUL Prediction Accuracy at Different Tolerances")
    fig = go.Figure(go.Bar(
        x=['±5 hours', '±10 hours', '±20 hours'],
        y=[ml['ann']['accuracy_5h']*100, ml['ann']['accuracy_10h']*100, ml['ann']['accuracy_20h']*100],
        marker=dict(color=['#FF6B6B', '#4ECDC4', '#6BCB77'])
    ))
    fig.update_layout(yaxis_title="Accuracy (%)", height=350)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Cost-Benefit Analysis")
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Bar(
            x=['Conventional', 'Digital Twin'],
            y=[ml['cost_benefit']['conventional_annual'], ml['cost_benefit']['digital_twin_annual']],
            marker=dict(color=['#FF6B6B', '#6BCB77'])
        ))
        fig.update_layout(title="Annual Maintenance Cost (per Engine)",
            yaxis_title="Cost (€)", height=380)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.metric("Annual Savings per Engine",
            format_currency(ml['cost_benefit']['savings']),
            f"{format_percent(ml['cost_benefit']['savings_percentage'])} reduction")
        st.metric("Fleet Annual Savings (100 engines)",
            format_currency(ml['cost_benefit']['fleet_annual_savings']), "100-engine fleet")
        st.metric("Payback Period",
            f"{ml['cost_benefit']['payback_months']:.1f} months",
            f"({ml['cost_benefit']['payback_years']} years)")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: ENGINE DIAGNOSTICS  ← NEW
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🔧 Engine Diagnostics":
    st.title("🔧 Engine Fault Diagnostics")
    st.markdown(
        f"**INYA-OKO, RAYMOND EKUMA** — Live fault analysis | "
        f"Last updated: `{datetime.now().strftime('%H:%M:%S')}`"
    )
    st.markdown("---")

    current_state = state_profile['state']   # NORMAL / DEGRADED / CRITICAL / RECOVERY
    latest = st.session_state.sensor_data.iloc[-1]

    sensor_readings = {
        'oil_temperature':    latest['oil_temperature'],
        'coolant_temperature':latest['coolant_temperature'],
        'egt':                latest['egt'],
        'oil_pressure':       latest['oil_pressure'],
        'fuel_pressure':      latest['fuel_pressure'],
        'vibration':          latest['vibration'],
        'rpm':                latest['rpm'],
    }

    # State explanation strip
    state_explanations = {
        "NORMAL":   "Engine is healthy. All sensors within normal operating range. Continue routine monitoring.",
        "DEGRADED": "One or more sensors are drifting outside normal range. Maintenance is needed soon — act now to prevent escalation to CRITICAL.",
        "CRITICAL": "Sensor readings have crossed danger thresholds. Immediate corrective action is required to prevent engine damage.",
        "RECOVERY": "Engine has returned from a fault state. Carry out verification checks before resuming full load.",
    }
    st.info(f"**Current state: {state_profile['emoji']} {current_state}** — {state_explanations.get(current_state, '')}")

    render_diagnostics(current_state, sensor_readings)

    st.markdown("---")
    st.caption(
        "This page refreshes automatically every 10 seconds in sync with the engine state cycle. "
        "When the state changes from NORMAL → DEGRADED, fault causes and corrective actions appear automatically. "
        "When the state moves to CRITICAL, final-warning troubleshooting steps are shown."
    )

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: DOCUMENTATION
# ═════════════════════════════════════════════════════════════════════════════
elif page == "📋 Documentation":
    st.title("📋 Project Documentation")
    st.markdown("**INYA-OKO, RAYMOND EKUMA** — Digital Twin Framework for CAT C4.4 Engine")
    st.markdown("---")
    st.subheader("Dataset Summary (Chapter 4, Section 4.2)")
    st.write("""
    - **Total records:** 34,500 (26,000 synthetic + 8,500 Kaggle)
    - **Training set (70%):** 24,150 | **Validation (15%):** 5,175 | **Test (15%):** 5,175
    - **Features:** 7 sensor inputs + 2 derived | **Engines:** 15 units | **Period:** 12 months
    """)
    st.subheader("Results Summary (Chapter 4 — Actual Kaggle Output)")
    st.write("""
    **Random Forest** — Accuracy: 100.00% | Precision/Recall/F1: 0.00% | AUC-ROC: NaN

    **Neural Network** — MAE: 32.0126h | RMSE: 39.9448h | R²: 0.5251 | MAPE: 8.16%
    Accuracy ±5h / ±10h / ±20h: 9.80% / 18.90% / 37.95%

    **Economic** — Conventional: €240,000/yr | Digital Twin: €78,000/yr
    Savings: €162,000 (67.5%) | Fleet (100): €16.2M/yr | Payback: 37 months
    """)
    st.subheader("Engine State Simulation Cycle")
    st.write("The live dashboard cycles through 4 states on a 90-second loop:")
    for s in STATE_CYCLE:
        st.write(f"{s['emoji']} **{s['state']}** — {s['duration']}s — sensors tuned to realistic {s['state'].lower()} readings")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT DEVELOPER
# ═════════════════════════════════════════════════════════════════════════════
elif page == "👨‍💻 About Developer":
    st.title("👨‍💻 About the Developer")
    st.markdown("---")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("## INYA-OKO, RAYMOND EKUMA")
        st.write("Master's Thesis Project")
        st.write("Digital Twin Framework for Optimized Predictive Maintenance: "
                 "A Case Study of the Caterpillar C4.4 Engine")
    with c2:
        st.subheader("Project Achievements (Actual Chapter 4 Results)")
        for m, d in [
            ("100.00%",  "RF Classifier Accuracy (class-imbalance artefact)"),
            ("32.01h",   "ANN RUL Prediction MAE"),
            ("0.5251",   "ANN R² Score"),
            ("67.5%",    "Cost Reduction"),
            ("€162,000", "Annual Savings per Engine"),
            ("€16.2M",   "Fleet Annual Savings (100 engines)"),
            ("37 months","Payback Period"),
        ]:
            st.write(f"**{m}** — {d}")

# ═════════════════════════════════════════════════════════════════════════════
# AUTO-RERUN every 10 seconds
# ═════════════════════════════════════════════════════════════════════════════
time.sleep(10)
st.rerun()
