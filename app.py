"""
Digital Twin Dashboard - CAT C4.4 Engine
Master's Thesis Project: Predictive Maintenance Framework
Author: INYA-OKO, RAYMOND EKUMA
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))
from helpers import (
    SensorDataGenerator, 
    HealthStatusCalculator, 
    MLModelResults,
    CostBenefitAnalysis,
    format_number,
    format_percent,
    format_currency
)

# Page configuration
st.set_page_config(
    page_title="Digital Twin Dashboard - INYA-OKO, RAYMOND EKUMA",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .developer-credit {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-top: 10px;
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
    .status-normal {
        color: #28a745;
        font-weight: bold;
    }
    .status-degraded {
        color: #ffc107;
        font-weight: bold;
    }
    .status-critical {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'sensor_data' not in st.session_state:
    generator = SensorDataGenerator()
    st.session_state.sensor_data = generator.generate_data(n_samples=1000)

if 'ml_results' not in st.session_state:
    st.session_state.ml_results = MLModelResults.get_mock_results()

# Sidebar navigation
st.sidebar.markdown("---")
st.sidebar.title("🔧 Digital Twin Dashboard")
st.sidebar.markdown("**By INYA-OKO, RAYMOND EKUMA**")
st.sidebar.markdown("Master's Thesis Project")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "📈 Real-Time Monitoring", "🤖 Analytics", "📋 Documentation", "👨‍💻 About Developer"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Project Information
- **Framework:** Streamlit + Python
- **ML Models:** Random Forest & Neural Network
- **Data Source:** Kaggle
- **Deployment:** Streamlit Cloud
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="developer-credit">
    <p><strong>Built by INYA-OKO, RAYMOND EKUMA</strong></p>
    <p>Digital Twin Framework for CAT C4.4 Engine</p>
</div>
""", unsafe_allow_html=True)

# Page: Dashboard
if page == "📊 Dashboard":
    st.markdown("""
    <h1 class="main-header">🔧 Digital Twin Dashboard</h1>
    <div class="developer-credit">
        <strong>Predictive Maintenance Framework for Caterpillar C4.4 Engine</strong><br>
        <em>Built by INYA-OKO, RAYMOND EKUMA</em>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Metrics — pulled live from helpers (Chapter 4 actual values)
    col1, col2, col3, col4 = st.columns(4)
    
    ml_results = st.session_state.ml_results
    
    with col1:
        st.metric(
            "Model Accuracy",
            f"{ml_results['random_forest']['accuracy']*100:.2f}%",
            "Random Forest"
        )
    
    with col2:
        st.metric(
            "RUL Prediction Error",
            f"{ml_results['ann']['mae']:.4f}h",
            "MAE (hours)"
        )
    
    with col3:
        st.metric(
            "R² Score",
            f"{ml_results['ann']['r2_score']:.4f}",
            "Neural Network"
        )
    
    with col4:
        st.metric(
            "Cost Savings",
            f"{format_percent(ml_results['cost_benefit']['savings_percentage'])}",
            "Annual"
        )
    
    st.markdown("---")
    
    # Project Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📌 Project Overview")
        st.write("""
        The Digital Twin Dashboard is a comprehensive framework for predictive maintenance 
        of the Caterpillar C4.4 diesel engine. This application combines machine learning, 
        IoT sensor integration, and real-time visualization to enable condition-based 
        maintenance scheduling.
        
        **Key Features:**
        - Real-time sensor monitoring
        - ML-based anomaly detection
        - RUL prediction
        - Maintenance scheduling
        - Cost-benefit analysis
        """)
    
    with col2:
        st.subheader("🎯 Key Results (Chapter 4 — Actual Kaggle Output)")
        # ── All numbers from Chapter 4 Tables 4.2, 4.3, and Section 4.4 ──
        achievements = [
            ("100.00%", "RF Classifier Accuracy (class-imbalance artefact)"),
            ("32.01h",  "ANN RUL Prediction Error (MAE)"),
            ("67.5%",   "Cost Reduction vs Conventional Maintenance"),
            ("€162,000","Annual Savings per Engine"),
        ]
        for metric, description in achievements:
            st.write(f"**{metric}** — {description}")
        
        st.caption(
            "⚠️ RF Precision/Recall/F1 = 0% due to class imbalance "
            "(Normal 70%, Degraded 25%, Critical 5%). "
            "See Chapter 4.6.1 for discussion."
        )
    
    st.markdown("---")
    
    # Technology Stack
    st.subheader("🛠️ Technology Stack")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("**Frontend**")
        st.write("• Streamlit")
        st.write("• Plotly")
        st.write("• Pandas")
    
    with col2:
        st.write("**ML & Data**")
        st.write("• Python")
        st.write("• Scikit-learn")
        st.write("• TensorFlow")
    
    with col3:
        st.write("**Data Processing**")
        st.write("• NumPy")
        st.write("• Pandas")
        st.write("• Seaborn")
    
    with col4:
        st.write("**Deployment**")
        st.write("• Streamlit Cloud")
        st.write("• Kaggle")
        st.write("• GitHub")

# Page: Real-Time Monitoring
elif page == "📈 Real-Time Monitoring":
    st.title("📈 Real-Time Engine Monitoring")
    st.markdown("**Built by INYA-OKO, RAYMOND EKUMA** - Live sensor data and health status")
    st.markdown("---")
    
    # Get latest sensor data
    latest_data = st.session_state.sensor_data.iloc[-1]
    
    # Health Status
    health_status, health_score, health_emoji = HealthStatusCalculator.get_health_status({
        'oil_temperature': latest_data['oil_temperature'],
        'egt': latest_data['egt'],
        'vibration': latest_data['vibration'],
        'oil_pressure': latest_data['oil_pressure'],
    })
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Engine Health Status", f"{health_emoji} {health_status}", "Current")
    
    with col2:
        rul = HealthStatusCalculator.calculate_rul(health_score)
        st.metric("RUL Estimate", f"{rul:.1f}h", "Remaining Hours")
    
    with col3:
        maintenance_rec = HealthStatusCalculator.get_maintenance_recommendation(rul)
        st.write(f"**Maintenance:** {maintenance_rec}")
    
    st.markdown("---")
    
    # Sensor Readings
    st.subheader("Current Sensor Readings")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Oil Temperature", f"{latest_data['oil_temperature']:.1f}°C", "Normal: 70-90°C")
    
    with col2:
        st.metric("Coolant Temperature", f"{latest_data['coolant_temperature']:.1f}°C", "Normal: 80-95°C")
    
    with col3:
        st.metric("EGT", f"{latest_data['egt']:.1f}°C", "Normal: 300-450°C")
    
    with col4:
        st.metric("Vibration", f"{latest_data['vibration']:.2f}g", "Normal: 0-3g")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Oil Pressure", f"{latest_data['oil_pressure']:.0f}kPa", "Normal: 250-400kPa")
    
    with col2:
        st.metric("Fuel Pressure", f"{latest_data['fuel_pressure']:.0f}kPa", "Normal: 1500-2000kPa")
    
    with col3:
        st.metric("RPM", f"{latest_data['rpm']:.0f}", "Normal: 1200-1800")
    
    st.markdown("---")
    
    # Time Series Charts
    st.subheader("Sensor Trends (Last 100 readings)")
    
    recent_data = st.session_state.sensor_data.tail(100).copy()
    recent_data['index'] = range(len(recent_data))
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=recent_data['index'],
            y=recent_data['oil_temperature'],
            name='Oil Temp',
            line=dict(color='#FF6B6B')
        ))
        fig.add_trace(go.Scatter(
            x=recent_data['index'],
            y=recent_data['coolant_temperature'],
            name='Coolant Temp',
            line=dict(color='#4ECDC4')
        ))
        fig.update_layout(
            title="Temperature Sensors",
            xaxis_title="Time Index",
            yaxis_title="Temperature (°C)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=recent_data['index'],
            y=recent_data['vibration'],
            name='Vibration',
            line=dict(color='#FFD93D')
        ))
        fig.update_layout(
            title="Vibration Levels",
            xaxis_title="Time Index",
            yaxis_title="Vibration (g)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=recent_data['index'],
            y=recent_data['oil_pressure'],
            name='Oil Pressure',
            line=dict(color='#6BCB77')
        ))
        fig.add_trace(go.Scatter(
            x=recent_data['index'],
            y=recent_data['fuel_pressure'],
            name='Fuel Pressure',
            line=dict(color='#4D96FF')
        ))
        fig.update_layout(
            title="Pressure Sensors",
            xaxis_title="Time Index",
            yaxis_title="Pressure (kPa)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=recent_data['index'],
            y=recent_data['rpm'],
            name='RPM',
            line=dict(color='#9B59B6')
        ))
        fig.update_layout(
            title="Engine RPM",
            xaxis_title="Time Index",
            yaxis_title="RPM",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# Page: Analytics
elif page == "🤖 Analytics":
    st.title("🤖 Machine Learning Analytics")
    st.markdown("**Built by INYA-OKO, RAYMOND EKUMA** — Results from actual Kaggle notebook output (Chapter 4)")
    st.markdown("---")
    
    ml_results = st.session_state.ml_results
    
    # Model Performance
    st.subheader("Model Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Random Forest Classifier (Anomaly Detection)**")
        # Chapter 4, Table 4.2 — ACTUAL RESULTS
        metrics_rf = [
            ("Accuracy",  f"{ml_results['random_forest']['accuracy']*100:.2f}%"),
            ("Precision", f"{ml_results['random_forest']['precision']*100:.2f}%"),
            ("Recall",    f"{ml_results['random_forest']['recall']*100:.2f}%"),
            ("F1-Score",  f"{ml_results['random_forest']['f1_score']*100:.2f}%"),
            ("AUC-ROC",   "NaN (undefined — class imbalance)"),
        ]
        for metric, value in metrics_rf:
            st.write(f"• {metric}: **{value}**")

    
    with col2:
        st.write("**Artificial Neural Network (RUL Prediction)**")
        # Chapter 4, Table 4.3 — ACTUAL RESULTS
        metrics_ann = [
            ("MAE",   f"{ml_results['ann']['mae']:.4f} hours"),
            ("RMSE",  f"{ml_results['ann']['rmse']:.4f} hours"),
            ("R² Score", f"{ml_results['ann']['r2_score']:.4f}"),
            ("MAPE",  f"{ml_results['ann']['mape']*100:.2f}%"),
        ]
        for metric, value in metrics_ann:
            st.write(f"• {metric}: **{value}**")
    
    st.markdown("---")
    
    # Feature Importance
    st.subheader("Feature Importance Analysis")
    
    features = list(ml_results['feature_importance'].keys())
    importances = list(ml_results['feature_importance'].values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=importances,
            y=features,
            orientation='h',
            marker=dict(color='#1f77b4')
        )
    ])
    fig.update_layout(
        title="Feature Importance in Anomaly Detection",
        xaxis_title="Importance Score",
        yaxis_title="Feature",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Prediction Accuracy — Chapter 4, Table 4.3 actual values
    st.subheader("RUL Prediction Accuracy")
    
    accuracy_data = {
        'Tolerance': ['±5 hours', '±10 hours', '±20 hours'],
        'Accuracy': [
            ml_results['ann']['accuracy_5h'] * 100,   # 9.80%
            ml_results['ann']['accuracy_10h'] * 100,  # 18.90%
            ml_results['ann']['accuracy_20h'] * 100   # 37.95%
        ]
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=accuracy_data['Tolerance'],
            y=accuracy_data['Accuracy'],
            marker=dict(color=['#FF6B6B', '#4ECDC4', '#6BCB77'])
        )
    ])
    fig.update_layout(
        title="RUL Prediction Accuracy at Different Tolerances (Chapter 4, Table 4.3)",
        yaxis_title="Accuracy (%)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Cost-Benefit Analysis — Chapter 4, Section 4.4.1 actual values
    st.subheader("Cost-Benefit Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        costs = {
            'Conventional': ml_results['cost_benefit']['conventional_annual'],  # €240,000
            'Digital Twin': ml_results['cost_benefit']['digital_twin_annual']   # €78,000
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(costs.keys()),
                y=list(costs.values()),
                marker=dict(color=['#FF6B6B', '#6BCB77'])
            )
        ])
        fig.update_layout(
            title="Annual Maintenance Cost Comparison (per Engine)",
            yaxis_title="Cost (€)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Economic Impact (Chapter 4, Section 4.4)**")
        st.metric(
            "Annual Savings per Engine",
            format_currency(ml_results['cost_benefit']['savings']),           # €162,000
            f"{format_percent(ml_results['cost_benefit']['savings_percentage'])} reduction"  # 67.5%
        )
        st.metric(
            "Fleet Annual Savings (100 engines)",
            format_currency(ml_results['cost_benefit']['fleet_annual_savings']),  # €16,200,000
            "100-engine fleet"
        )
        st.metric(
            "Payback Period",
            f"{ml_results['cost_benefit']['payback_months']:.1f} months",   # 37.0 months
            f"({ml_results['cost_benefit']['payback_years']} years)"         # 3.1 years
        )

# Page: Documentation
elif page == "📋 Documentation":
    st.title("📋 Project Documentation")
    st.markdown("**Built by INYA-OKO, RAYMOND EKUMA** — Digital Twin Framework for CAT C4.4 Engine")
    st.markdown("---")

    st.subheader("Dataset Summary (Chapter 4, Section 4.2)")
    st.write("""
    - **Total records:** 34,500 (26,000 synthetic + 8,500 Kaggle)
    - **Training set (70%):** 24,150 records
    - **Validation set (15%):** 5,175 records
    - **Test set (15%):** 5,175 records
    - **Features per record:** 7 sensor inputs + 2 derived features
    - **Engines represented:** 15 distinct units
    - **Temporal coverage:** 12 months
    """)

    st.subheader("Results Summary (Chapter 4 — Actual Kaggle Output)")
    st.write("""
    **Random Forest Classifier**
    - Accuracy: 100.00% *(class-imbalance artefact — see Chapter 4.6.1)*
    - Precision / Recall / F1: 0.00% *(model predicts majority class only)*
    - AUC-ROC: NaN

    **Neural Network (RUL Prediction)**
    - MAE: 32.0126 hours
    - RMSE: 39.9448 hours
    - R²: 0.5251 (explains 52.51% of variance)
    - MAPE: 8.16%
    - Accuracy ±5h / ±10h / ±20h: 9.80% / 18.90% / 37.95%

    **Economic Impact**
    - Conventional maintenance: €240,000/year per engine
    - Digital Twin maintenance: €78,000/year per engine
    - Annual savings: €162,000 (67.5%)
    - Fleet savings (100 engines): €16,200,000/year
    - Payback period: 37.0 months (3.1 years)
    """)

# Page: About Developer
elif page == "👨‍💻 About Developer":
    st.title("👨‍💻 About the Developer")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("## INYA-OKO, RAYMOND EKUMA")
        st.write("Master's Thesis Project")
        st.write("Digital Twin Framework for Optimized Predictive Maintenance: A Case Study of the Caterpillar C4.4 Engine")

    with col2:
        st.subheader("Project Achievements (Actual Chapter 4 Results)")
        achievements = [
            ("100.00%", "RF Classifier Accuracy (class-imbalance artefact)"),
            ("32.01h",  "ANN RUL Prediction MAE"),
            ("0.5251",  "ANN R² Score"),
            ("67.5%",   "Cost Reduction"),
            ("€162,000","Annual Savings per Engine"),
            ("€16.2M",  "Fleet Annual Savings (100 engines)"),
            ("37 months","Payback Period"),
        ]
        for metric, description in achievements:
            st.write(f"**{metric}** — {description}")