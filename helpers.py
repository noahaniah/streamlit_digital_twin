"""
Utility Functions for Digital Twin Dashboard
Author: INYA-OKO, RAYMOND EKUMA
Master's Thesis Project: Digital Twin Framework for CAT C4.4 Engine

NUMBERS UPDATED TO MATCH CHAPTER 4 ACTUAL KAGGLE RESULTS
Live engine state simulation added — cycles through NORMAL → DEGRADED → CRITICAL → RECOVERY
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Tuple, List
import time

# ─────────────────────────────────────────────────────────────────────────────
# ENGINE STATE SIMULATOR
# Drives realistic state transitions every 10 seconds.
# Cycle: NORMAL (30s) → DEGRADED (20s) → CRITICAL (20s) → RECOVERY (20s) → repeat
# ─────────────────────────────────────────────────────────────────────────────

STATE_CYCLE = [
    {
        'state':    'NORMAL',
        'duration': 30,
        'emoji':    '🟢',
        'color':    '#28a745',
        'sensors': {
            'oil_temperature':    (78,   2.0),
            'coolant_temperature':(87,   1.5),
            'egt':                (370,  8.0),
            'oil_pressure':       (340,  12.0),
            'fuel_pressure':      (1820, 40.0),
            'vibration':          (2.2,  0.15),
            'rpm':                (1500, 40.0),
        }
    },
    {
        'state':    'DEGRADED',
        'duration': 20,
        'emoji':    '🟠',
        'color':    '#fd7e14',
        'sensors': {
            'oil_temperature':    (98,   3.0),
            'coolant_temperature':(95,   2.0),
            'egt':                (490,  15.0),
            'oil_pressure':       (215,  18.0),
            'fuel_pressure':      (1650, 60.0),
            'vibration':          (3.8,  0.30),
            'rpm':                (1380, 70.0),
        }
    },
    {
        'state':    'CRITICAL',
        'duration': 20,
        'emoji':    '🔴',
        'color':    '#dc3545',
        'sensors': {
            'oil_temperature':    (112,  4.0),
            'coolant_temperature':(104,  3.0),
            'egt':                (560,  20.0),
            'oil_pressure':       (175,  20.0),
            'fuel_pressure':      (1480, 80.0),
            'vibration':          (5.5,  0.50),
            'rpm':                (1180, 90.0),
        }
    },
    {
        'state':    'RECOVERY',
        'duration': 20,
        'emoji':    '🔵',
        'color':    '#007bff',
        'sensors': {
            'oil_temperature':    (88,   2.5),
            'coolant_temperature':(90,   2.0),
            'egt':                (410,  10.0),
            'oil_pressure':       (290,  15.0),
            'fuel_pressure':      (1740, 50.0),
            'vibration':          (2.8,  0.20),
            'rpm':                (1460, 50.0),
        }
    },
]

TOTAL_CYCLE_DURATION = sum(s['duration'] for s in STATE_CYCLE)


def get_current_state_profile() -> dict:
    """Returns the active state profile based on Unix time modulo cycle length."""
    elapsed = int(time.time()) % TOTAL_CYCLE_DURATION
    cumulative = 0
    for state in STATE_CYCLE:
        cumulative += state['duration']
        if elapsed < cumulative:
            return state
    return STATE_CYCLE[0]


def generate_live_reading(state_profile: dict) -> dict:
    """Generate one sensor reading with noise matching the given state profile."""
    reading = {}
    for sensor, (mean, std) in state_profile['sensors'].items():
        reading[sensor] = float(np.random.normal(mean, std))
    return reading


# ─────────────────────────────────────────────────────────────────────────────
# SENSOR DATA GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

class SensorDataGenerator:
    """Generates rolling sensor history whose live tail reflects current engine state."""

    def __init__(self, seed: int = 42):
        self.seed = seed

    def generate_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """Generate initial synthetic history at startup."""
        np.random.seed(self.seed)
        time_index = pd.date_range(
            start=datetime.now() - timedelta(seconds=10 * n_samples),
            periods=n_samples, freq='10S'
        )
        t = np.linspace(0, 4 * np.pi, n_samples)

        oil_temp      = 75   + 15  * np.sin(t) + np.random.normal(0, 2,   n_samples)
        coolant_temp  = 85   + 10  * np.sin(t) + np.random.normal(0, 1.5, n_samples)
        egt           = 350  + 50  * np.sin(t) + np.random.normal(0, 10,  n_samples)
        oil_pressure  = 350  + 50  * np.cos(t) + np.random.normal(0, 15,  n_samples)
        fuel_pressure = 1800 + 200 * np.cos(t) + np.random.normal(0, 50,  n_samples)
        vibration     = 2.5  + 0.5 * np.sin(t) + np.random.normal(0, 0.2, n_samples)
        rpm           = 1500 + 300 * np.sin(t) + np.random.normal(0, 50,  n_samples)

        deg = np.linspace(0, 0.3, n_samples)
        oil_temp  += deg * 10
        egt       += deg * 30
        vibration += deg * 1.5

        return pd.DataFrame({
            'timestamp':           time_index,
            'oil_temperature':     np.clip(oil_temp,      20,  120),
            'coolant_temperature': np.clip(coolant_temp,  30,  110),
            'egt':                 np.clip(egt,           200, 650),
            'oil_pressure':        np.clip(oil_pressure,  0,   600),
            'fuel_pressure':       np.clip(fuel_pressure, 0,   2500),
            'vibration':           np.clip(vibration,     0,   50),
            'rpm':                 np.clip(rpm,           600, 2200),
        })

    def append_live_reading(self, df: pd.DataFrame, state_profile: dict) -> pd.DataFrame:
        """Append one new live reading and trim buffer to 1000 rows."""
        r = generate_live_reading(state_profile)
        new_row = pd.DataFrame([{
            'timestamp':           datetime.now(),
            'oil_temperature':     np.clip(r['oil_temperature'],     20,  120),
            'coolant_temperature': np.clip(r['coolant_temperature'], 30,  110),
            'egt':                 np.clip(r['egt'],                 200, 650),
            'oil_pressure':        np.clip(r['oil_pressure'],        0,   600),
            'fuel_pressure':       np.clip(r['fuel_pressure'],       0,   2500),
            'vibration':           np.clip(r['vibration'],           0,   50),
            'rpm':                 np.clip(r['rpm'],                 600, 2200),
        }])
        return pd.concat([df, new_row], ignore_index=True).tail(1000).reset_index(drop=True)


# ─────────────────────────────────────────────────────────────────────────────
# HEALTH STATUS CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────

class HealthStatusCalculator:

    @staticmethod
    def get_health_status(data: Dict) -> Tuple[str, float, str]:
        anomaly_count = 0
        if data.get('oil_temperature', 0) > 100: anomaly_count += 1
        if data.get('egt', 0)             > 500: anomaly_count += 1
        if data.get('vibration', 0)       > 4:   anomaly_count += 1
        if data.get('oil_pressure', 0)    < 200: anomaly_count += 1

        if   anomaly_count >= 3: return 'CRITICAL', 0.90, '🔴'
        elif anomaly_count >= 2: return 'DEGRADED', 0.60, '🟠'
        elif anomaly_count == 1: return 'DEGRADED', 0.45, '🟠'
        else:                    return 'NORMAL',   0.15, '🟢'

    @staticmethod
    def calculate_rul(anomaly_score: float) -> float:
        return max(500 * (1.0 - anomaly_score), 0)

    @staticmethod
    def get_maintenance_recommendation(rul: float) -> str:
        if   rul < 50:  return "⚠️ Immediate maintenance required"
        elif rul < 150: return "🔧 Schedule maintenance soon"
        elif rul < 300: return "📋 Monitor closely — plan ahead"
        else:           return "✅ Continue normal operation"

    @staticmethod
    def get_state_color(status: str) -> str:
        return {'NORMAL':'#28a745','DEGRADED':'#fd7e14','CRITICAL':'#dc3545','RECOVERY':'#007bff'}.get(status,'#6c757d')


# ─────────────────────────────────────────────────────────────────────────────
# ML MODEL RESULTS  — ACTUAL Chapter 4 / Kaggle values
# ─────────────────────────────────────────────────────────────────────────────

class MLModelResults:

    @staticmethod
    def get_mock_results() -> Dict:
        return {
            'random_forest': {
                'accuracy': 1.0000, 'precision': 0.0000,
                'recall':   0.0000, 'f1_score':  0.0000, 'auc_roc': None
            },
            'ann': {
                'mae': 32.0126, 'rmse': 39.9448, 'r2_score': 0.5251, 'mape': 0.0816,
                'accuracy_5h': 0.0980, 'accuracy_10h': 0.1890, 'accuracy_20h': 0.3795,
            },
            'feature_importance': {
                'oil_temperature': 0.30, 'egt': 0.25, 'vibration': 0.20,
                'oil_pressure': 0.15, 'fuel_pressure': 0.10,
            },
            'cost_benefit': {
                'conventional_annual': 240_000, 'digital_twin_annual': 78_000,
                'savings': 162_000, 'savings_percentage': 0.675,
                'fleet_annual_savings': 16_200_000,
                'payback_months': 37.0, 'payback_years': 3.1,
            }
        }


# ─────────────────────────────────────────────────────────────────────────────
# COST BENEFIT / FORMATTING
# ─────────────────────────────────────────────────────────────────────────────

class CostBenefitAnalysis:
    @staticmethod
    def calculate_savings(c: float, d: float) -> float: return max(c - d, 0)
    @staticmethod
    def savings_percentage(c: float, d: float) -> float:
        return 0 if c == 0 else CostBenefitAnalysis.calculate_savings(c, d) / c

def format_number(v: float)   -> str: return f"{v:,.2f}"
def format_percent(v: float)  -> str: return f"{v*100:.2f}%"
def format_currency(v: float) -> str: return f"€{v:,.2f}"
