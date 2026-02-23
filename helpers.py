"""
Utility Functions for Digital Twin Dashboard
Author: INYA-OKO, RAYMOND EKUMA
Master's Thesis Project: Digital Twin Framework for CAT C4.4 Engine

"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Tuple, List

# -------------------------------
# Sensor Data Generator
# -------------------------------
class SensorDataGenerator:
    """Generate realistic synthetic sensor data for CAT C4.4 engine"""
    
    def __init__(self, seed: int = 42):
        self.seed = seed
        np.random.seed(seed)
    
    def generate_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """Generate synthetic sensor data"""
        time_index = pd.date_range(start='2025-01-01', periods=n_samples, freq='10S')
        
        # Generate sensor data with realistic patterns
        t = np.linspace(0, 4*np.pi, n_samples)
        
        # Temperature sensors
        oil_temp = 75 + 15*np.sin(t) + np.random.normal(0, 2, n_samples)
        coolant_temp = 85 + 10*np.sin(t) + np.random.normal(0, 1.5, n_samples)
        egt = 350 + 50*np.sin(t) + np.random.normal(0, 10, n_samples)
        
        # Pressure sensors
        oil_pressure = 350 + 50*np.cos(t) + np.random.normal(0, 15, n_samples)
        fuel_pressure = 1800 + 200*np.cos(t) + np.random.normal(0, 50, n_samples)
        
        # Vibration and RPM
        vibration = 2.5 + 0.5*np.sin(t) + np.random.normal(0, 0.2, n_samples)
        rpm = 1500 + 300*np.sin(t) + np.random.normal(0, 50, n_samples)
        
        # Add degradation trend
        degradation_factor = np.linspace(0, 0.3, n_samples)
        oil_temp += degradation_factor * 10
        egt += degradation_factor * 30
        vibration += degradation_factor * 1.5
        
        # Clip to realistic ranges (from Chapter 4 Table 4.1)
        oil_temp = np.clip(oil_temp, 20, 120)
        coolant_temp = np.clip(coolant_temp, 30, 110)
        egt = np.clip(egt, 200, 650)
        oil_pressure = np.clip(oil_pressure, 0, 600)
        fuel_pressure = np.clip(fuel_pressure, 0, 2500)
        vibration = np.clip(vibration, 0, 50)
        rpm = np.clip(rpm, 600, 2200)
        
        # Create DataFrame
        df = pd.DataFrame({
            'timestamp': time_index,
            'oil_temperature': oil_temp,
            'coolant_temperature': coolant_temp,
            'egt': egt,
            'oil_pressure': oil_pressure,
            'fuel_pressure': fuel_pressure,
            'vibration': vibration,
            'rpm': rpm
        })
        
        return df

# -------------------------------
# Health Status Calculator
# -------------------------------
class HealthStatusCalculator:
    """Calculate engine health status based on sensor readings"""
    
    @staticmethod
    def get_health_status(data: Dict) -> Tuple[str, float, str]:
        """
        Determine health status based on sensor readings
        Returns: (status, score, emoji)
        """
        anomaly_count = 0
        
        if data.get('oil_temperature', 0) > 100:
            anomaly_count += 1
        if data.get('egt', 0) > 500:
            anomaly_count += 1
        if data.get('vibration', 0) > 4:
            anomaly_count += 1
        if data.get('oil_pressure', 0) < 200:
            anomaly_count += 1
        
        if anomaly_count >= 3:
            return 'CRITICAL', 0.9, '🔴'
        elif anomaly_count >= 2:
            return 'DEGRADED', 0.6, '🟠'
        else:
            return 'NORMAL', 0.2, '🟢'
    
    @staticmethod
    def calculate_rul(anomaly_score: float, degradation_rate: float = 0.5) -> float:
        """
        Calculate Remaining Useful Life (RUL) in hours
        based on anomaly score and degradation rate.
        """
        base_rul = 500  # hours
        rul = base_rul - (anomaly_score * degradation_rate)
        return max(rul, 0)

    @staticmethod
    def get_maintenance_recommendation(rul: float) -> str:
        """Return maintenance recommendation based on RUL"""
        if rul < 50:
            return "⚠️ Immediate maintenance required"
        elif rul < 100:
            return "🔧 Schedule maintenance soon"
        else:
            return "✅ Continue normal operation"

# -------------------------------
# ML Model Results — ACTUAL Chapter 4 / Kaggle Results
# -------------------------------
class MLModelResults:
    """Provide ML results matching actual Kaggle notebook output (Chapter 4)"""
    
    @staticmethod
    def get_mock_results() -> Dict:
        return {
            # ── Random Forest Classifier ──────────────────────────────────────
            # Chapter 4, Table 4.2: ACTUAL KAGGLE RESULTS
            # Note: 100% accuracy is due to class imbalance (Normal: 70%, Degraded: 25%, Critical: 5%)
            # Precision/Recall/F1 = 0% because model predicts majority class only
            'random_forest': {
                'accuracy': 1.0000,    # 100.00% — majority-class prediction artefact
                'precision': 0.0000,   # 0.00%   — class imbalance issue
                'recall': 0.0000,      # 0.00%   — class imbalance issue
                'f1_score': 0.0000,    # 0.00%   — class imbalance issue
                'auc_roc': None        # NaN     — undefined due to single-class prediction
            },

            # ── Artificial Neural Network (RUL Prediction) ────────────────────
            # Chapter 4, Table 4.3: ACTUAL KAGGLE RESULTS
            'ann': {
                'mae': 32.0126,        # Mean Absolute Error (hours)
                'rmse': 39.9448,       # Root Mean Square Error (hours)
                'r2_score': 0.5251,    # R² Score (explains 52.51% of variance)
                'mape': 0.0816,        # MAPE = 8.16%
                'accuracy_5h': 0.0980, # 9.80%  of predictions within ±5 hours
                'accuracy_10h': 0.1890,# 18.90% of predictions within ±10 hours
                'accuracy_20h': 0.3795 # 37.95% of predictions within ±20 hours
            },

            # ── Feature Importance ────────────────────────────────────────────
            # Relative importance scores for anomaly detection model
            'feature_importance': {
                'oil_temperature': 0.30,
                'egt': 0.25,
                'vibration': 0.20,
                'oil_pressure': 0.15,
                'fuel_pressure': 0.10
            },

            # ── Cost-Benefit Analysis ─────────────────────────────────────────
            # Chapter 4, Section 4.4.1: ACTUAL KAGGLE RESULTS
            # Per-engine annual costs:
            #   Conventional Maintenance: €240,000
            #   Digital Twin Maintenance:  €78,000
            #   Annual Savings:           €162,000 (67.5%)
            # Fleet savings (100 engines): €16,200,000
            # Payback period: 37.0 months (3.1 years)
            'cost_benefit': {
                'conventional_annual': 240_000,      # €240,000
                'digital_twin_annual': 78_000,        # €78,000
                'savings': 162_000,                   # €162,000
                'savings_percentage': 0.675,          # 67.5%
                'fleet_annual_savings': 16_200_000,   # €16,200,000 (100-engine fleet)
                'payback_months': 37.0,               # 37.0 months
                'payback_years': 3.1                  # 3.1 years
            }
        }

# -------------------------------
# Cost Benefit Analysis
# -------------------------------
class CostBenefitAnalysis:
    """Perform cost-benefit calculations for digital twin"""

    @staticmethod
    def calculate_savings(conventional_cost: float, digital_twin_cost: float) -> float:
        return max(conventional_cost - digital_twin_cost, 0)

    @staticmethod
    def savings_percentage(conventional_cost: float, digital_twin_cost: float) -> float:
        if conventional_cost == 0:
            return 0
        return CostBenefitAnalysis.calculate_savings(conventional_cost, digital_twin_cost) / conventional_cost

# -------------------------------
# Formatting Utilities
# -------------------------------
def format_number(value: float) -> str:
    return f"{value:,.2f}"

def format_percent(value: float) -> str:
    return f"{value*100:.2f}%"

def format_currency(value: float) -> str:
    return f"€{value:,.2f}"