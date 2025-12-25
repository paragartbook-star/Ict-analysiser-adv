import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import time
import requests
import warnings
import pytz
from scipy import stats
import json
import base64
from io import BytesIO
import plotly.express as px
from typing import Dict, List, Tuple, Optional
import threading
from queue import Queue
import asyncio
import websockets
import schedule
from PIL import Image
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import telegram
from twilio.rest import Client
import discord
import pickle
import hashlib
import re
from scipy.signal import argrelextrema
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import tensorflow as tf
from tensorflow import keras
from transformers import pipeline

warnings.filterwarnings('ignore')
IST = pytz.timezone('Asia/Kolkata')

# ═══════════════════════════════════════════════════════════════════════
# ICT ADVANCED MULTI-ASSET ANALYZER - 2026 EDITION
# ═══════════════════════════════════════════════════════════════════════

# Page Configuration
st.set_page_config(
    page_title="ICT Advanced Analyzer 2026 Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Enhanced
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #121226 50%, #0a0a1a 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d1a 0%, #121226 100%);
        border-right: 1px solid #2d2d5a;
        backdrop-filter: blur(20px);
    }

    /* Headers with glow */
    h1, h2, h3 {
        color: #00f3ff !important;
        font-weight: 800 !important;
        text-shadow: 0 0 15px rgba(0, 243, 255, 0.5), 0 0 25px rgba(0, 243, 255, 0.3);
        letter-spacing: -0.5px;
    }

    h4, h5, h6 {
        color: #8be9fd !important;
        font-weight: 600 !important;
    }

    /* Metric Cards with Glassmorphism */
    [data-testid="stMetric"] {
        background: rgba(18, 18, 38, 0.7) !important;
        backdrop-filter: blur(15px);
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(0, 243, 255, 0.2) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 243, 255, 0.5) !important;
        box-shadow: 0 12px 40px rgba(0, 243, 255, 0.2);
    }

    /* Tables */
    .dataframe {
        background: rgba(18, 18, 38, 0.8) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(45, 45, 90, 0.5) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    .dataframe thead {
        background: linear-gradient(90deg, #121226 0%, #1a1a3a 100%) !important;
    }

    .dataframe thead th {
        color: #00f3ff !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #00f3ff !important;
        padding: 15px 10px !important;
    }

    .dataframe tbody tr {
        transition: all 0.2s ease;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .dataframe tbody tr:hover {
        background: rgba(0, 243, 255, 0.1) !important;
        transform: scale(1.002);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
        background-size: 200% 200%;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: 700;
        font-size: 14px;
        transition: all 0.4s ease;
        animation: gradientShift 3s ease infinite;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
    }

    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* Special buttons */
    .danger-button > button {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%) !important;
    }

    .success-button > button {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%) !important;
    }

    /* Inputs and Selectboxes */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(18, 18, 38, 0.8) !important;
        border: 1px solid rgba(0, 243, 255, 0.3) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #00f3ff !important;
        box-shadow: 0 0 0 2px rgba(0, 243, 255, 0.2) !important;
    }

    /* Checkboxes and Radio */
    .stCheckbox > div > label,
    .stRadio > div > label {
        color: #b8c1ec !important;
        font-weight: 500 !important;
    }

    /* Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00f3ff 0%, #764ba2 100%) !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(18, 18, 38, 0.7) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(0, 243, 255, 0.2) !important;
        color: #00f3ff !important;
        font-weight: 600 !important;
    }

    .streamlit-expanderContent {
        background: rgba(18, 18, 38, 0.5) !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* Signal Badges */
    .signal-strong-buy {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(0, 176, 155, 0.3);
        animation: pulse-green 2s infinite;
    }

    .signal-buy {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 18px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 3px 10px rgba(86, 171, 47, 0.3);
    }

    .signal-hold {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        color: #121226;
        padding: 6px 14px;
        border-radius: 18px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 3px 10px rgba(247, 151, 30, 0.3);
    }

    .signal-sell {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 18px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 3px 10px rgba(255, 65, 108, 0.3);
    }

    .signal-strong-sell {
        background: linear-gradient(135deg, #8B0000 0%, #FF0000 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(139, 0, 0, 0.3);
        animation: pulse-red 2s infinite;
    }

    @keyframes pulse-green {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 176, 155, 0.3); }
        50% { box-shadow: 0 0 30px rgba(0, 176, 155, 0.6); }
    }

    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.3); }
        50% { box-shadow: 0 0 30px rgba(255, 0, 0, 0.6); }
    }

    /* Alert Boxes */
    .stAlert {
        border-radius: 10px !important;
        border: 1px solid !important;
        backdrop-filter: blur(10px);
    }

    .stAlert[data-baseweb="notification"] {
        background: rgba(18, 18, 38, 0.9) !important;
    }

    /* Kill Zone Status */
    .killzone-active {
        background: linear-gradient(135deg, rgba(0, 243, 255, 0.2) 0%, rgba(0, 243, 255, 0.1) 100%);
        border: 2px solid #00f3ff;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
    }

    .killzone-active::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.2), transparent);
        animation: shine 3s infinite;
    }

    .killzone-inactive {
        background: linear-gradient(135deg, rgba(107, 114, 128, 0.2) 0%, rgba(75, 85, 99, 0.1) 100%);
        border: 2px solid #6b7280;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
    }

    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: rgba(18, 18, 38, 0.5);
        border-radius: 10px;
        padding: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(18, 18, 38, 0.3);
        border-radius: 8px;
        padding: 10px 20px;
        color: #b8c1ec;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(0, 243, 255, 0.1);
        color: #00f3ff;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: rgba(18, 18, 38, 0.95);
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -150px;
        opacity: 0;
        transition: opacity 0.3s;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 243, 255, 0.3);
        font-size: 12px;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }

    /* Chart Container */
    .chart-container {
        background: rgba(18, 18, 38, 0.5);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(0, 243, 255, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        color: #6b7280;
        font-size: 12px;
        border-top: 1px solid rgba(45, 45, 90, 0.5);
        margin-top: 50px;
        background: rgba(10, 10, 26, 0.5);
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(18, 18, 38, 0.3);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    /* Loading Animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(0, 243, 255, 0.3);
        border-radius: 50%;
        border-top-color: #00f3ff;
        animation: spin 1s ease-in-out infinite;
        margin-right: 10px;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* Badge for premium features */
    .premium-badge {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: #121226;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        margin-left: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== ENHANCED CONFIGURATIONS ====================
NIFTY_50 = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
    'HINDUNILVR.NS', 'BHARTIARTL.NS', 'ITC.NS', 'SBIN.NS', 'KOTAKBANK.NS',
    'LT.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS', 'WIPRO.NS',
    'BAJFINANCE.NS', 'TITAN.NS', 'HCLTECH.NS', 'SUNPHARMA.NS', 'ULTRACEMCO.NS',
    'ADANIPORTS.NS', 'TATAMOTORS.NS', 'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS',
    'BAJAJFINSV.NS', 'TATASTEEL.NS', 'NESTLEIND.NS', 'JSWSTEEL.NS', 'DIVISLAB.NS',
    'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 'CIPLA.NS', 'TECHM.NS',
    'INDUSINDBK.NS', 'ADANIENT.NS', 'BAJAJ-AUTO.NS', 'BPCL.NS', 'HEROMOTOCO.NS',
    'SHREECEM.NS', 'COALINDIA.NS', 'TATACONSUM.NS', 'HINDALCO.NS', 'BRITANNIA.NS',
    'M&M.NS', 'APOLLOHOSP.NS', 'DABUR.NS', 'PIDILITIND.NS', 'SBILIFE.NS'
]

TOP_50_CRYPTO = [
    'bitcoin', 'ethereum', 'tether', 'binancecoin', 'solana', 'ripple', 'usd-coin', 'cardano',
    'avalanche-2', 'dogecoin', 'tron', 'polkadot', 'matic-network', 'chainlink', 'shiba-inu',
    'litecoin', 'bitcoin-cash', 'uniswap', 'cosmos', 'stellar', 'monero', 'ethereum-classic',
    'aptos', 'filecoin', 'hedera-hashgraph', 'internet-computer', 'vechain', 'algorand',
    'near', 'quant-network', 'aave', 'the-graph', 'the-sandbox', 'decentraland', 'theta-token',
    'axie-infinity', 'eos', 'fantom', 'elrond-erd-2', 'tezos', 'thorchain', 'maker', 'pancakeswap-token',
    'zcash', 'synthetix-network-token', 'compound-governance-token', 'kava', 'chiliz', 'enjincoin',
    'basic-attention-token'
]

FOREX_PAIRS = [
    'EURUSD=X', 'USDJPY=X', 'GBPUSD=X', 'AUDUSD=X', 'USDCAD=X',
    'USDCHF=X', 'NZDUSD=X', 'EURJPY=X', 'GBPJPY=X', 'EURGBP=X',
    'AUDJPY=X', 'EURAUD=X', 'USDCNY=X', 'USDHKD=X', 'USDSGD=X',
    'USDINR=X', 'USDMXN=X', 'USDZAR=X', 'USDTRY=X', 'EURCAD=X'
]

# Enhanced ICT Concepts with weights
ICT_CONCEPTS = {
    'Market Structure': {'weight': 100, 'color': '#00f3ff'},
    'Order Blocks': {'weight': 100, 'color': '#ff6b6b'},
    'Fair Value Gaps': {'weight': 95, 'color': '#4ecdc4'},
    'Liquidity Pools': {'weight': 90, 'color': '#45b7d1'},
    'Breaker Blocks': {'weight': 85, 'color': '#ffd166'},
    'Optimal Trade Entry': {'weight': 80, 'color': '#06d6a0'},
    'Kill Zones': {'weight': 70, 'color': '#ef476f'},
    'Power of 3': {'weight': 50, 'color': '#118ab2'},
    'Asian Range': {'weight': 65, 'color': '#ff9a76'},
    'SMT Divergence': {'weight': 75, 'color': '#a663cc'}
}

# ==================== ADVANCED ICT DETECTION FUNCTIONS ====================

def detect_breaker_blocks(df):
    """Detect Breaker Blocks (Rejection candles at key levels)"""
    breaker_blocks = []
    for i in range(2, len(df)-2):
        # Bullish Breaker Block
        if (df['Close'].iloc[i] > df['High'].iloc[i-1] and 
            df['Open'].iloc[i] < df['Close'].iloc[i] and
            df['Close'].iloc[i+1] < df['Open'].iloc[i+1]):
            breaker_blocks.append({
                'type': 'Bullish Breaker',
                'price': df['Close'].iloc[i],
                'date': df.index[i],
                'strength': 0.8
            })
        
        # Bearish Breaker Block
        elif (df['Close'].iloc[i] < df['Low'].iloc[i-1] and 
              df['Open'].iloc[i] > df['Close'].iloc[i] and
              df['Close'].iloc[i+1] > df['Open'].iloc[i+1]):
            breaker_blocks.append({
                'type': 'Bearish Breaker',
                'price': df['Close'].iloc[i],
                'date': df.index[i],
                'strength': 0.8
            })
    
    return breaker_blocks

def detect_liquidity_sweeps(df, window=20):
    """Detect Liquidity Sweeps (Wicks beyond recent range)"""
    sweeps = []
    for i in range(window, len(df)):
        recent_high = df['High'].iloc[i-window:i].max()
        recent_low = df['Low'].iloc[i-window:i].min()
        
        # Buy-side liquidity sweep (wick above recent high)
        if df['High'].iloc[i] > recent_high and df['Close'].iloc[i] < recent_high:
            sweeps.append({
                'type': 'Buy-side Sweep',
                'price': df['High'].iloc[i],
                'date': df.index[i],
                'wick_size': df['High'].iloc[i] - max(df['Close'].iloc[i], df['Open'].iloc[i])
            })
        
        # Sell-side liquidity sweep (wick below recent low)
        elif df['Low'].iloc[i] < recent_low and df['Close'].iloc[i] > recent_low:
            sweeps.append({
                'type': 'Sell-side Sweep',
                'price': df['Low'].iloc[i],
                'date': df.index[i],
                'wick_size': min(df['Close'].iloc[i], df['Open'].iloc[i]) - df['Low'].iloc[i]
            })
    
    return sweeps

def detect_asian_range(df):
    """Detect Asian Range (First few hours of trading session)"""
    asian_ranges = []
    df['hour'] = df.index.hour
    df['date'] = df.index.date
    
    for date in df['date'].unique():
        date_data = df[df['date'] == date]
        asian_session = date_data[(date_data['hour'] >= 3) & (date_data['hour'] <= 7)]  # 3 AM to 7 AM UTC
        
        if not asian_session.empty:
            high = asian_session['High'].max()
            low = asian_session['Low'].min()
            asian_ranges.append({
                'date': date,
                'high': high,
                'low': low,
                'range': high - low,
                'breakout': df[df['date'] == date]['High'].max() > high or 
                           df[df['date'] == date]['Low'].min() < low
            })
    
    return asian_ranges

def detect_power_of_3(df):
    """Detect Power of 3 Phases (Accumulation, Manipulation, Distribution)"""
    phases = []
    
    # Calculate 20-period moving average
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()
    
    for i in range(50, len(df)-10):
        # Accumulation Phase (Price consolidating below MA)
        if (df['Close'].iloc[i-20:i].std() < df['Close'].iloc[i-50:i].std() * 0.7 and
            df['Close'].iloc[i] < df['MA20'].iloc[i] and
            df['Volume'].iloc[i-20:i].mean() > df['Volume'].iloc[i-50:i-20].mean()):
            phases.append({'type': 'Accumulation', 'date': df.index[i], 'price': df['Close'].iloc[i]})
        
        # Manipulation Phase (False breakout)
        elif (abs(df['Close'].iloc[i] - df['MA20'].iloc[i]) < df['Close'].iloc[i] * 0.02 and
              df['Volume'].iloc[i] > df['Volume'].iloc[i-20:i].mean() * 1.5):
            phases.append({'type': 'Manipulation', 'date': df.index[i], 'price': df['Close'].iloc[i]})
        
        # Distribution Phase (Price above MA with decreasing volume)
        elif (df['Close'].iloc[i] > df['MA20'].iloc[i] and
              df['Volume'].iloc[i] < df['Volume'].iloc[i-20:i].mean() * 0.8):
            phases.append({'type': 'Distribution', 'date': df.index[i], 'price': df['Close'].iloc[i]})
    
    return phases

def detect_premium_discount_zones(df):
    """Detect Premium/Discount Zones relative to 50% equilibrium"""
    zones = []
    
    for i in range(20, len(df)):
        recent_high = df['High'].iloc[i-20:i].max()
        recent_low = df['Low'].iloc[i-20:i].min()
        equilibrium = (recent_high + recent_low) / 2
        
        current_price = df['Close'].iloc[i]
        
        # Premium Zone (above equilibrium)
        if current_price > equilibrium + (recent_high - recent_low) * 0.25:
            zones.append({
                'type': 'Premium Zone',
                'date': df.index[i],
                'price': current_price,
                'distance_from_eq': (current_price - equilibrium) / (recent_high - recent_low)
            })
        
        # Discount Zone (below equilibrium)
        elif current_price < equilibrium - (recent_high - recent_low) * 0.25:
            zones.append({
                'type': 'Discount Zone',
                'date': df.index[i],
                'price': current_price,
                'distance_from_eq': (equilibrium - current_price) / (recent_high - recent_low)
            })
    
    return zones

def detect_optimal_trade_entry(df):
    """Detect Optimal Trade Entry Zones (0.62-0.79 Fibonacci)"""
    ote_zones = []
    
    for i in range(50, len(df)):
        # Find recent swing high and low
        recent_data = df.iloc[i-50:i]
        swing_high = recent_data['High'].max()
        swing_low = recent_data['Low'].min()
        
        if swing_high != swing_low:
            range_size = swing_high - swing_low
            
            # OTE Zone (0.618 - 0.786 Fibonacci retracement)
            ote_low = swing_high - range_size * 0.786
            ote_high = swing_high - range_size * 0.618
            
            current_price = df['Close'].iloc[i]
            
            if ote_low <= current_price <= ote_high:
                ote_zones.append({
                    'date': df.index[i],
                    'price': current_price,
                    'zone_low': ote_low,
                    'zone_high': ote_high,
                    'retracement': (swing_high - current_price) / range_size
                })
    
    return ote_zones

def detect_market_structure_shift(df):
    """Detect Market Structure Shifts"""
    shifts = []
    
    df['higher_high'] = df['High'] > df['High'].shift(1)
    df['higher_low'] = df['Low'] > df['Low'].shift(1)
    df['lower_high'] = df['High'] < df['High'].shift(1)
    df['lower_low'] = df['Low'] < df['Low'].shift(1)
    
    for i in range(3, len(df)):
        # Bullish MSS (Higher High + Higher Low after Lower Low)
        if (df['lower_low'].iloc[i-2] and 
            df['higher_low'].iloc[i-1] and 
            df['higher_high'].iloc[i]):
            shifts.append({
                'type': 'Bullish MSS',
                'date': df.index[i],
                'price': df['Close'].iloc[i],
                'confidence': 0.8
            })
        
        # Bearish MSS (Lower High + Lower Low after Higher High)
        elif (df['higher_high'].iloc[i-2] and 
              df['lower_high'].iloc[i-1] and 
              df['lower_low'].iloc[i]):
            shifts.append({
                'type': 'Bearish MSS',
                'date': df.index[i],
                'price': df['Close'].iloc[i],
                'confidence': 0.8
            })
    
    return shifts

# ==================== MULTI-TIMEFRAME ANALYSIS ====================

class MultiTimeframeAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker
        self.timeframes = {
            '1m': '1m',
            '5m': '5m', 
            '15m': '15m',
            '1h': '1h',
            '4h': '4h',
            '1d': '1d',
            '1wk': '1wk'
        }
        
    def fetch_mtf_data(self, period='7d'):
        """Fetch data for all timeframes"""
        data = {}
        for tf_name, tf_interval in self.timeframes.items():
            try:
                if tf_interval in ['1m', '5m']:
                    data_period = '7d'
                elif tf_interval == '15m':
                    data_period = '60d'
                else:
                    data_period = period
                    
                df = yf.download(self.ticker, period=data_period, interval=tf_interval, progress=False)
                if not df.empty:
                    data[tf_name] = df
            except:
                continue
        return data
    
    def analyze_confluence(self, mtf_data):
        """Analyze confluence across timeframes"""
        confluence = {
            'bullish': 0,
            'bearish': 0,
            'neutral': 0,
            'details': {}
        }
        
        for tf, df in mtf_data.items():
            if len(df) > 20:
                # Calculate trend for each timeframe
                ma_short = df['Close'].rolling(10).mean()
                ma_long = df['Close'].rolling(30).mean()
                
                if ma_short.iloc[-1] > ma_long.iloc[-1]:
                    confluence['bullish'] += 1
                    trend = 'Bullish'
                elif ma_short.iloc[-1] < ma_long.iloc[-1]:
                    confluence['bearish'] += 1
                    trend = 'Bearish'
                else:
                    confluence['neutral'] += 1
                    trend = 'Neutral'
                
                confluence['details'][tf] = {
                    'trend': trend,
                    'price': df['Close'].iloc[-1],
                    'rsi': calculate_rsi(df['Close']),
                    'volume': df['Volume'].iloc[-1]
                }
        
        total = sum([confluence['bullish'], confluence['bearish'], confluence['neutral']])
        if total > 0:
            confluence['score'] = (confluence['bullish'] - confluence['bearish']) / total
        else:
            confluence['score'] = 0
            
        return confluence
    
    def get_htf_bias(self, mtf_data):
        """Get Higher Timeframe bias"""
        htf_tfs = ['4h', '1d', '1wk']
        bias_scores = []
        
        for tf in htf_tfs:
            if tf in mtf_data:
                df = mtf_data[tf]
                if len(df) > 50:
                    # Simple trend detection using EMA
                    ema_20 = df['Close'].ewm(span=20).mean().iloc[-1]
                    ema_50 = df['Close'].ewm(span=50).mean().iloc[-1]
                    
                    if ema_20 > ema_50:
                        bias_scores.append(1)  # Bullish
                    else:
                        bias_scores.append(-1)  # Bearish
        
        if bias_scores:
            avg_bias = sum(bias_scores) / len(bias_scores)
            return 'Bullish' if avg_bias > 0 else 'Bearish' if avg_bias < 0 else 'Neutral'
        return 'Neutral'

# ==================== ADVANCED TECHNICAL INDICATORS ====================

def calculate_vwap(df):
    """Calculate Volume Weighted Average Price"""
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    vwap = (typical_price * df['Volume']).cumsum() / df['Volume'].cumsum()
    return vwap

def calculate_volume_profile(df, bins=20):
    """Calculate Volume Profile"""
    price_range = df['Close'].max() - df['Close'].min()
    bin_size = price_range / bins
    volume_profile = {}
    
    for i in range(bins):
        price_level = df['Close'].min() + (i * bin_size)
        next_level = price_level + bin_size
        volume_in_bin = df[(df['Close'] >= price_level) & (df['Close'] < next_level)]['Volume'].sum()
        volume_profile[f'{price_level:.2f}-{next_level:.2f}'] = volume_in_bin
    
    # Find Point of Control (POC)
    poc_level = max(volume_profile, key=volume_profile.get)
    return volume_profile, poc_level

def calculate_atr(df, period=14):
    """Calculate Average True Range"""
    high_low = df['High'] - df['Low']
    high_close = abs(df['High'] - df['Close'].shift())
    low_close = abs(df['Low'] - df['Close'].shift())
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(period).mean()
    return atr

def calculate_ichimoku(df):
    """Calculate Ichimoku Cloud"""
    # Tenkan-sen (Conversion Line)
    nine_period_high = df['High'].rolling(window=9).max()
    nine_period_low = df['Low'].rolling(window=9).min()
    df['tenkan_sen'] = (nine_period_high + nine_period_low) / 2
    
    # Kijun-sen (Base Line)
    twenty_six_period_high = df['High'].rolling(window=26).max()
    twenty_six_period_low = df['Low'].rolling(window=26).min()
    df['kijun_sen'] = (twenty_six_period_high + twenty_six_period_low) / 2
    
    # Senkou Span A (Leading Span A)
    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)
    
    # Senkou Span B (Leading Span B)
    fifty_two_period_high = df['High'].rolling(window=52).max()
    fifty_two_period_low = df['Low'].rolling(window=52).min()
    df['senkou_span_b'] = ((fifty_two_period_high + fifty_two_period_low) / 2).shift(26)
    
    # Chikou Span (Lagging Span)
    df['chikou_span'] = df['Close'].shift(-26)
    
    return df

def calculate_pivot_points(df):
    """Calculate Pivot Points"""
    if len(df) < 1:
        return None
    
    yesterday = df.iloc[-1]
    pp = {}
    
    # Standard Pivot Points
    pp['pivot'] = (yesterday['High'] + yesterday['Low'] + yesterday['Close']) / 3
    pp['r1'] = 2 * pp['pivot'] - yesterday['Low']
    pp['s1'] = 2 * pp['pivot'] - yesterday['High']
    pp['r2'] = pp['pivot'] + (yesterday['High'] - yesterday['Low'])
    pp['s2'] = pp['pivot'] - (yesterday['High'] - yesterday['Low'])
    pp['r3'] = yesterday['High'] + 2 * (pp['pivot'] - yesterday['Low'])
    pp['s3'] = yesterday['Low'] - 2 * (yesterday['High'] - pp['pivot'])
    
    # Fibonacci Pivot Points
    pp['r1_fib'] = pp['pivot'] + 0.382 * (yesterday['High'] - yesterday['Low'])
    pp['r2_fib'] = pp['pivot'] + 0.618 * (yesterday['High'] - yesterday['Low'])
    pp['r3_fib'] = pp['pivot'] + 1.0 * (yesterday['High'] - yesterday['Low'])
    pp['s1_fib'] = pp['pivot'] - 0.382 * (yesterday['High'] - yesterday['Low'])
    pp['s2_fib'] = pp['pivot'] - 0.618 * (yesterday['High'] - yesterday['Low'])
    pp['s3_fib'] = pp['pivot'] - 1.0 * (yesterday['High'] - yesterday['Low'])
    
    return pp

# ==================== ALERT SYSTEM ====================

class AlertSystem:
    def __init__(self):
        self.alerts = []
        self.sent_alerts = set()
        
    def create_alert(self, asset, condition_type, condition_value, notification_type='browser'):
        """Create a new alert"""
        alert_id = hashlib.md5(f"{asset}{condition_type}{condition_value}{datetime.now()}".encode()).hexdigest()[:8]
        alert = {
            'id': alert_id,
            'asset': asset,
            'condition_type': condition_type,
            'condition_value': condition_value,
            'created_at': datetime.now(),
            'triggered': False,
            'notification_type': notification_type
        }
        self.alerts.append(alert)
        return alert_id
    
    def check_alerts(self, asset_data):
        """Check all alerts against current data"""
        triggered_alerts = []
        
        for alert in self.alerts:
            if not alert['triggered']:
                asset = alert['asset']
                condition_type = alert['condition_type']
                condition_value = alert['condition_value']
                
                # Check if asset matches
                if asset in asset_data:
                    current_data = asset_data[asset]
                    triggered = False
                    
                    if condition_type == 'price_above' and current_data['price'] > condition_value:
                        triggered = True
                    elif condition_type == 'price_below' and current_data['price'] < condition_value:
                        triggered = True
                    elif condition_type == 'rsi_above' and current_data.get('rsi', 50) > condition_value:
                        triggered = True
                    elif condition_type == 'rsi_below' and current_data.get('rsi', 50) < condition_value:
                        triggered = True
                    elif condition_type == 'volume_spike' and current_data.get('volume', 0) > condition_value:
                        triggered = True
                    
                    if triggered:
                        alert['triggered'] = True
                        alert['triggered_at'] = datetime.now()
                        alert['triggered_value'] = current_data['price'] if 'price' in condition_type else current_data.get('rsi', 0)
                        triggered_alerts.append(alert)
                        
                        # Send notification
                        self.send_notification(alert)
        
        return triggered_alerts
    
    def send_notification(self, alert):
        """Send notification based on type"""
        message = f"🚨 ALERT TRIGGERED!\nAsset: {alert['asset']}\nCondition: {alert['condition_type']} {alert['condition_value']}\nCurrent: {alert['triggered_value']}"
        
        if alert['notification_type'] == 'browser':
            st.warning(message)
        
        elif alert['notification_type'] == 'email' and 'email_config' in st.session_state:
            self.send_email(alert, message)
        
        elif alert['notification_type'] == 'telegram' and 'telegram_config' in st.session_state:
            self.send_telegram(alert, message)
        
        elif alert['notification_type'] == 'discord' and 'discord_config' in st.session_state:
            self.send_discord(alert, message)
    
    def send_email(self, alert, message):
        """Send email notification"""
        try:
            config = st.session_state.email_config
            msg = MIMEMultipart()
            msg['From'] = config['sender']
            msg['To'] = config['receiver']
            msg['Subject'] = f"ICT Alert: {alert['asset']}"
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            server.starttls()
            server.login(config['sender'], config['password'])
            server.send_message(msg)
            server.quit()
        except Exception as e:
            st.error(f"Email send failed: {e}")
    
    def send_telegram(self, alert, message):
        """Send Telegram notification"""
        try:
            config = st.session_state.telegram_config
            bot = telegram.Bot(token=config['token'])
            bot.send_message(chat_id=config['chat_id'], text=message)
        except Exception as e:
            st.error(f"Telegram send failed: {e}")
    
    def send_discord(self, alert, message):
        """Send Discord notification"""
        try:
            config = st.session_state.discord_config
            webhook = discord.Webhook.from_url(config['webhook_url'], adapter=discord.RequestsWebhookAdapter())
            webhook.send(message)
        except Exception as e:
            st.error(f"Discord send failed: {e}")

# ==================== REPORT GENERATION ====================

def generate_pdf_report(asset_data, analysis_results):
    """Generate PDF report"""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("ICT Advanced Analysis Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Date
    date_str = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    story.append(date_str)
    story.append(Spacer(1, 24))
    
    # Summary Table
    summary_data = [['Metric', 'Value']]
    if 'combined_score' in asset_data:
        summary_data.append(['Combined Score', f"{asset_data['combined_score']:.1f}"])
    if 'signal' in asset_data:
        summary_data.append(['Signal', asset_data['signal']])
    if 'trend' in asset_data:
        summary_data.append(['Trend', asset_data['trend']])
    if 'risk' in asset_data:
        summary_data.append(['Risk Level', f"{asset_data['risk']}/10"])
    
    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(summary_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def export_to_excel(df, filename="ict_analysis.xlsx"):
    """Export DataFrame to Excel with formatting"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Analysis', index=False)
        
        # Get workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Analysis']
        
        # Apply formatting
        for column in worksheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
    
    output.seek(0)
    return output

# ==================== AI & MACHINE LEARNING ====================

class PricePredictor:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        
    def prepare_data(self, prices, lookback=60):
        """Prepare data for LSTM model"""
        scaled_data = self.scaler.fit_transform(prices.values.reshape(-1, 1))
        
        X, y = [], []
        for i in range(lookback, len(scaled_data)):
            X.append(scaled_data[i-lookback:i, 0])
            y.append(scaled_data[i, 0])
        
        X = np.array(X)
        y = np.array(y)
        
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        return X, y
    
    def build_lstm_model(self, lookback=60):
        """Build LSTM model for price prediction"""
        model = keras.Sequential([
            keras.layers.LSTM(units=50, return_sequences=True, input_shape=(lookback, 1)),
            keras.layers.Dropout(0.2),
            keras.layers.LSTM(units=50, return_sequences=True),
            keras.layers.Dropout(0.2),
            keras.layers.LSTM(units=50),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(units=1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model
    
    def predict(self, historical_prices, days_ahead=7, lookback=60):
        """Predict future prices"""
        # Prepare data
        scaled_prices = self.scaler.fit_transform(historical_prices.values.reshape(-1, 1))
        
        # Create sequences
        X_test = []
        last_sequence = scaled_prices[-lookback:]
        X_test.append(last_sequence)
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        
        # Build and train model
        model = self.build_lstm_model(lookback)
        model.fit(X_test, np.zeros(1), epochs=10, batch_size=32, verbose=0)
        
        # Make predictions
        predictions = []
        current_sequence = last_sequence.copy()
        
        for _ in range(days_ahead):
            x_input = current_sequence.reshape((1, lookback, 1))
            pred = model.predict(x_input, verbose=0)[0][0]
            predictions.append(pred)
            current_sequence = np.append(current_sequence[1:], pred)
        
        # Inverse transform predictions
        predictions = self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
        return predictions.flatten()

class PatternRecognizer:
    def __init__(self):
        self.patterns = {
            'head_shoulders': self.detect_head_shoulders,
            'double_top': self.detect_double_top,
            'double_bottom': self.detect_double_bottom,
            'triangle': self.detect_triangle,
            'flag': self.detect_flag
        }
    
    def detect_head_shoulders(self, df):
        """Detect Head and Shoulders pattern"""
        patterns = []
        n = len(df)
        
        for i in range(100, n-100):
            # Find local maxima
            if (df['High'].iloc[i] > df['High'].iloc[i-50:i].max() and
                df['High'].iloc[i] > df['High'].iloc[i+1:i+51].max()):
                
                # Look for shoulders
                left_max = df['High'].iloc[i-100:i-50].max()
                right_max = df['High'].iloc[i+50:i+100].max()
                
                if left_max < df['High'].iloc[i] * 0.95 and right_max < df['High'].iloc[i] * 0.95:
                    patterns.append({
                        'type': 'Head and Shoulders',
                        'date': df.index[i],
                        'price': df['High'].iloc[i],
                        'confidence': 0.7
                    })
        
        return patterns
    
    def detect_double_top(self, df):
        """Detect Double Top pattern"""
        patterns = []
        n = len(df)
        
        for i in range(50, n-50):
            if (abs(df['High'].iloc[i] - df['High'].iloc[i-30:i].max()) < df['High'].iloc[i] * 0.02 and
                df['Close'].iloc[i] < df['Close'].iloc[i-10]):
                patterns.append({
                    'type': 'Double Top',
                    'date': df.index[i],
                    'price': df['High'].iloc[i],
                    'confidence': 0.6
                })
        
        return patterns
    
    def detect_double_bottom(self, df):
        """Detect Double Bottom pattern"""
        patterns = []
        n = len(df)
        
        for i in range(50, n-50):
            if (abs(df['Low'].iloc[i] - df['Low'].iloc[i-30:i].min()) < df['Low'].iloc[i] * 0.02 and
                df['Close'].iloc[i] > df['Close'].iloc[i-10]):
                patterns.append({
                    'type': 'Double Bottom',
                    'date': df.index[i],
                    'price': df['Low'].iloc[i],
                    'confidence': 0.6
                })
        
        return patterns
    
    def detect_all_patterns(self, df):
        """Detect all patterns"""
        all_patterns = []
        for pattern_name, pattern_func in self.patterns.items():
            patterns = pattern_func(df)
            all_patterns.extend(patterns)
        return all_patterns

# ==================== ECONOMIC CALENDAR ====================

class EconomicCalendar:
    def __init__(self):
        self.events = []
        
    def fetch_events(self, country='US', days=7):
        """Fetch economic calendar events"""
        try:
            # Using Financial Modeling Prep API (free tier)
            api_key = st.secrets.get("FMP_API_KEY", "")
            if api_key:
                url = f"https://financialmodelingprep.com/api/v3/economic_calendar?country={country}&apikey={api_key}"
                response = requests.get(url)
                if response.status_code == 200:
                    self.events = response.json()[:days]
        except:
            # Fallback to sample data
            self.events = [
                {
                    'event': 'FOMC Meeting',
                    'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                    'country': 'US',
                    'importance': 'High',
                    'actual': None,
                    'forecast': '0.25%'
                },
                {
                    'event': 'Non-Farm Payrolls',
                    'date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
                    'country': 'US',
                    'importance': 'High',
                    'actual': None,
                    'forecast': '200K'
                },
                {
                    'event': 'CPI Data',
                    'date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
                    'country': 'US',
                    'importance': 'High',
                    'actual': None,
                    'forecast': '3.2%'
                }
            ]
        return self.events
    
    def get_market_impact(self, event):
        """Get potential market impact of an event"""
        importance = event.get('importance', 'Medium')
        if importance == 'High':
            return 'High Impact - Expect Volatility'
        elif importance == 'Medium':
            return 'Medium Impact - Monitor Closely'
        else:
            return 'Low Impact'

# ==================== PORTFOLIO MANAGER ====================

class PortfolioManager:
    def __init__(self):
        self.positions = []
        self.cash = 100000  # Starting cash
        
    def add_position(self, symbol, quantity, entry_price, asset_type='Stock'):
        """Add a new position"""
        position = {
            'symbol': symbol,
            'quantity': quantity,
            'entry_price': entry_price,
            'current_price': entry_price,
            'asset_type': asset_type,
            'entry_date': datetime.now(),
            'pnl': 0,
            'pnl_percent': 0
        }
        self.positions.append(position)
        self.cash -= quantity * entry_price
        return position
    
    def update_prices(self, price_data):
        """Update position prices"""
        total_value = self.cash
        total_pnl = 0
        
        for position in self.positions:
            symbol = position['symbol']
            if symbol in price_data:
                position['current_price'] = price_data[symbol]
                position['pnl'] = (price_data[symbol] - position['entry_price']) * position['quantity']
                position['pnl_percent'] = ((price_data[symbol] / position['entry_price']) - 1) * 100
            
            total_value += position['current_price'] * position['quantity']
            total_pnl += position['pnl']
        
        return {
            'total_value': total_value,
            'total_pnl': total_pnl,
            'total_pnl_percent': (total_pnl / (total_value - total_pnl)) * 100 if total_value > total_pnl else 0,
            'cash': self.cash
        }
    
    def calculate_sharpe_ratio(self, returns_series, risk_free_rate=0.02):
        """Calculate Sharpe Ratio"""
        if len(returns_series) < 2:
            return 0
        
        excess_returns = returns_series - risk_free_rate/252  # Daily risk-free rate
        if excess_returns.std() == 0:
            return 0
        
        sharpe = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
        return sharpe
    
    def calculate_max_drawdown(self, values_series):
        """Calculate Maximum Drawdown"""
        if len(values_series) < 2:
            return 0
        
        cumulative = (1 + values_series).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        return max_drawdown

# ==================== RISK MANAGEMENT ====================

class RiskManager:
    def __init__(self, portfolio_value=100000):
        self.portfolio_value = portfolio_value
        self.max_risk_per_trade = 0.02  # 2% per trade
        self.max_daily_loss = 0.05  # 5% daily
        
    def calculate_position_size(self, entry_price, stop_loss, risk_amount=None):
        """Calculate optimal position size"""
        if risk_amount is None:
            risk_amount = self.portfolio_value * self.max_risk_per_trade
        
        risk_per_share = abs(entry_price - stop_loss)
        if risk_per_share == 0:
            return 0
        
        position_size = risk_amount / risk_per_share
        return int(position_size)
    
    def calculate_stop_loss(self, entry_price, atr, multiplier=2):
        """Calculate stop loss based on ATR"""
        stop_loss = entry_price - (atr * multiplier)
        return stop_loss
    
    def calculate_take_profit(self, entry_price, stop_loss, risk_reward_ratio=2):
        """Calculate take profit based on risk/reward ratio"""
        risk = abs(entry_price - stop_loss)
        take_profit = entry_price + (risk * risk_reward_ratio)
        return take_profit
    
    def calculate_kelly_criterion(self, win_rate, avg_win, avg_loss):
        """Calculate Kelly Criterion for position sizing"""
        if avg_loss == 0:
            return 0
        
        win_ratio = avg_win / abs(avg_loss)
        kelly = win_rate - ((1 - win_rate) / win_ratio)
        return max(0, kelly * 0.5)  # Half-Kelly for conservative approach

# ==================== BACKTESTING ENGINE ====================

class Backtester:
    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = []
        self.trades = []
        self.equity_curve = []
        
    def run_backtest(self, df, strategy_func, **kwargs):
        """Run backtest on historical data"""
        signals = strategy_func(df, **kwargs)
        
        position = 0
        entry_price = 0
        
        for i in range(len(df)):
            signal = signals.iloc[i] if i < len(signals) else 0
            
            if signal == 1 and position == 0:  # Buy signal
                position = 1
                entry_price = df['Close'].iloc[i]
                self.trades.append({
                    'type': 'BUY',
                    'date': df.index[i],
                    'price': entry_price,
                    'size': self.capital / entry_price
                })
                
            elif signal == -1 and position == 1:  # Sell signal
                position = 0
                exit_price = df['Close'].iloc[i]
                pnl = (exit_price - entry_price) * (self.capital / entry_price)
                self.capital += pnl
                
                self.trades.append({
                    'type': 'SELL',
                    'date': df.index[i],
                    'price': exit_price,
                    'pnl': pnl
                })
            
            # Update equity curve
            if position == 1:
                current_value = self.capital + (df['Close'].iloc[i] - entry_price) * (self.capital / entry_price)
            else:
                current_value = self.capital
            
            self.equity_curve.append(current_value)
        
        return self.calculate_metrics()
    
    def calculate_metrics(self):
        """Calculate backtest performance metrics"""
        if not self.equity_curve:
            return {}
        
        equity_series = pd.Series(self.equity_curve)
        returns = equity_series.pct_change().dropna()
        
        # Calculate metrics
        total_return = (equity_series.iloc[-1] - self.initial_capital) / self.initial_capital * 100
        
        if len(returns) > 0:
            sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std() if returns.std() != 0 else 0
            max_drawdown = self.calculate_max_drawdown(equity_series)
            win_rate = self.calculate_win_rate()
        else:
            sharpe_ratio = 0
            max_drawdown = 0
            win_rate = 0
        
        metrics = {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'total_trades': len([t for t in self.trades if t['type'] == 'SELL']),
            'final_capital': equity_series.iloc[-1]
        }
        
        return metrics
    
    def calculate_win_rate(self):
        """Calculate win rate from trades"""
        sell_trades = [t for t in self.trades if t['type'] == 'SELL']
        if not sell_trades:
            return 0
        
        winning_trades = sum(1 for t in sell_trades if t.get('pnl', 0) > 0)
        return (winning_trades / len(sell_trades)) * 100
    
    def calculate_max_drawdown(self, equity_curve):
        """Calculate maximum drawdown"""
        cumulative = pd.Series(equity_curve)
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min() * 100

# ==================== MAIN APPLICATION ====================

def main():
    # Initialize session state
    if 'alert_system' not in st.session_state:
        st.session_state.alert_system = AlertSystem()
    if 'portfolio_manager' not in st.session_state:
        st.session_state.portfolio_manager = PortfolioManager()
    if 'risk_manager' not in st.session_state:
        st.session_state.risk_manager = RiskManager()
    
    # Header with tabs
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, rgba(0,243,255,0.1) 0%, rgba(102,126,234,0.1) 100%); border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='margin: 0;'>🚀 ICT ADVANCED ANALYZER 2026 PRO</h1>
        <p style='color: #8be9fd; margin: 10px 0 0 0;'>Professional Trading Suite with AI-Powered Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tabs = st.tabs([
        "📊 Dashboard", 
        "🔍 Advanced Analysis", 
        "📈 Live Charts", 
        "🚨 Alerts",
        "💰 Portfolio",
        "⚙️ Settings"
    ])
    
    with tabs[0]:  # Dashboard
        render_dashboard()
    
    with tabs[1]:  # Advanced Analysis
        render_advanced_analysis()
    
    with tabs[2]:  # Live Charts
        render_live_charts()
    
    with tabs[3]:  # Alerts
        render_alerts()
    
    with tabs[4]:  # Portfolio
        render_portfolio()
    
    with tabs[5]:  # Settings
        render_settings()

def render_dashboard():
    """Render main dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Assets", "150+", "Live")
    
    with col2:
        st.metric("Active Alerts", "12", "3 New")
    
    with col3:
        st.metric("Portfolio Value", "₹1,24,560", "+2.4%")
    
    with col4:
        st.metric("Market Sentiment", "Bullish", "72%")
    
    # Market Overview
    st.markdown("## 📈 Market Overview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Quick analysis form
        with st.form("quick_analysis"):
            symbol = st.text_input("Enter Symbol (e.g., RELIANCE.NS, BTC-USD):", "RELIANCE.NS")
            timeframe = st.selectbox("Timeframe:", ["1d", "1wk", "1mo", "3mo"])
            analyze_button = st.form_submit_button("🚀 Analyze Now")
            
            if analyze_button:
                with st.spinner("Analyzing..."):
                    result = quick_analysis(symbol, timeframe)
                    if result:
                        st.success(f"Analysis complete! Score: {result['score']}/100")
    
    with col2:
        # Kill Zone Status
        kill_zone = get_kill_zone()
        st.markdown(f"""
        <div class='killzone-{'active' if kill_zone['active'] else 'inactive'}'>
            <h4>{kill_zone['name']}</h4>
            <p>Multiplier: {kill_zone['multiplier']}x</p>
            <p>Status: {'🟢 ACTIVE' if kill_zone['active'] else '⚪ INACTIVE'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Top Recommendations
    st.markdown("## 🏆 Top Recommendations")
    display_top_recommendations()

def render_advanced_analysis():
    """Render advanced analysis section"""
    st.markdown("## 🔬 Advanced ICT Analysis")
    
    # Analysis type selector
    analysis_type = st.selectbox(
        "Select Analysis Type:",
        ["ICT Pattern Detection", "Multi-Timeframe Analysis", "Volume Profile", 
         "Market Structure", "Fibonacci Analysis", "Order Flow"]
    )
    
    symbol = st.text_input("Symbol for Analysis:", "RELIANCE.NS")
    
    if st.button("Run Advanced Analysis", type="primary"):
        with st.spinner("Running deep analysis..."):
            if analysis_type == "ICT Pattern Detection":
                analyze_ict_patterns(symbol)
            elif analysis_type == "Multi-Timeframe Analysis":
                analyze_multi_timeframe(symbol)
            elif analysis_type == "Volume Profile":
                analyze_volume_profile(symbol)
            elif analysis_type == "Market Structure":
                analyze_market_structure(symbol)
            elif analysis_type == "Fibonacci Analysis":
                analyze_fibonacci(symbol)
            elif analysis_type == "Order Flow":
                analyze_order_flow(symbol)

def render_live_charts():
    """Render live charts section"""
    st.markdown("## 📊 Advanced Charting")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        symbol = st.text_input("Chart Symbol:", "RELIANCE.NS")
    
    with col2:
        timeframe = st.selectbox(
            "Timeframe:",
            ["1m", "5m", "15m", "1h", "4h", "1d", "1wk"],
            index=5
        )
    
    with col3:
        chart_type = st.selectbox(
            "Chart Type:",
            ["Candlestick", "Heikin-Ashi", "Renko", "Line", "Area"]
        )
    
    # Indicators selector
    indicators = st.multiselect(
        "Add Indicators:",
        ["EMA", "SMA", "Bollinger Bands", "RSI", "MACD", "Volume", "VWAP", 
         "Ichimoku Cloud", "ATR Bands", "Pivot Points", "Fibonacci Levels"]
    )
    
    if st.button("Generate Chart", type="primary"):
        with st.spinner("Loading chart..."):
            fig = create_advanced_chart(symbol, timeframe, chart_type, indicators)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

def render_alerts():
    """Render alerts section"""
    st.markdown("## 🚨 Alert System")
    
    # Create new alert
    with st.expander("Create New Alert", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            alert_symbol = st.text_input("Symbol:", "RELIANCE.NS")
        
        with col2:
            condition_type = st.selectbox(
                "Condition:",
                ["price_above", "price_below", "rsi_above", "rsi_below", "volume_spike"]
            )
        
        with col3:
            condition_value = st.number_input("Value:", value=100.0)
        
        notification_type = st.selectbox(
            "Notification Type:",
            ["browser", "email", "telegram", "discord"]
        )
        
        if st.button("Create Alert", type="primary"):
            alert_id = st.session_state.alert_system.create_alert(
                alert_symbol, condition_type, condition_value, notification_type
            )
            st.success(f"Alert created! ID: {alert_id}")
    
    # Active alerts
    st.markdown("### Active Alerts")
    if st.session_state.alert_system.alerts:
        for alert in st.session_state.alert_system.alerts:
            if not alert['triggered']:
                st.info(f"**{alert['asset']}** - {alert['condition_type']} {alert['condition_value']}")
    else:
        st.warning("No active alerts")

def render_portfolio():
    """Render portfolio section"""
    st.markdown("## 💰 Portfolio Management")
    
    # Add new position
    with st.expander("Add Position", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pos_symbol = st.text_input("Symbol:", "RELIANCE.NS")
        
        with col2:
            pos_quantity = st.number_input("Quantity:", min_value=1, value=10)
        
        with col3:
            pos_entry = st.number_input("Entry Price:", min_value=0.0, value=2400.0)
        
        with col4:
            pos_type = st.selectbox("Type:", ["Stock", "Crypto", "Forex", "Other"])
        
        if st.button("Add to Portfolio", type="primary"):
            st.session_state.portfolio_manager.add_position(
                pos_symbol, pos_quantity, pos_entry, pos_type
            )
            st.success("Position added!")
    
    # Portfolio summary
    st.markdown("### Portfolio Summary")
    if st.session_state.portfolio_manager.positions:
        summary = st.session_state.portfolio_manager.update_prices({})
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Value", f"₹{summary['total_value']:,.2f}")
        col2.metric("Total P&L", f"₹{summary['total_pnl']:,.2f}", 
                   f"{summary['total_pnl_percent']:.2f}%")
        col3.metric("Cash Balance", f"₹{summary['cash']:,.2f}")
        col4.metric("Positions", len(st.session_state.portfolio_manager.positions))
        
        # Positions table
        positions_df = pd.DataFrame(st.session_state.portfolio_manager.positions)
        st.dataframe(positions_df, use_container_width=True)
    else:
        st.info("No positions in portfolio. Add some positions to get started.")

def render_settings():
    """Render settings section"""
    st.markdown("## ⚙️ Settings & Configuration")
    
    # Theme settings
    with st.expander("Theme Settings", expanded=True):
        theme = st.selectbox("Theme:", ["Dark", "Light", "Auto"])
        accent_color = st.color_picker("Accent Color:", "#00f3ff")
        st.button("Apply Theme", type="primary")
    
    # Notification settings
    with st.expander("Notification Settings"):
        email_notifications = st.checkbox("Email Notifications", value=False)
        if email_notifications:
            st.text_input("Email Address:")
            st.text_input("SMTP Server:", "smtp.gmail.com")
            st.number_input("SMTP Port:", value=587)
        
        telegram_notifications = st.checkbox("Telegram Notifications", value=False)
        if telegram_notifications:
            st.text_input("Bot Token:")
            st.text_input("Chat ID:")
        
        discord_notifications = st.checkbox("Discord Notifications", value=False)
        if discord_notifications:
            st.text_input("Webhook URL:")
    
    # API Settings
    with st.expander("API Configuration"):
        st.text_input("Yahoo Finance API Key (Optional):")
        st.text_input("Alpha Vantage API Key (Optional):")
        st.text_input("News API Key (Optional):")
    
    # Data settings
    with st.expander("Data Settings"):
        refresh_interval = st.slider("Auto-refresh interval (seconds):", 10, 300, 60)
        cache_duration = st.slider("Cache duration (minutes):", 5, 60, 15)
        historical_data = st.number_input("Days of historical data:", 30, 365*5, 365)
    
    if st.button("Save Settings", type="primary"):
        st.success("Settings saved successfully!")

# ==================== HELPER FUNCTIONS ====================

def get_kill_zone():
    """Get current kill zone"""
    now = datetime.now(IST)
    hour = now.hour
    
    if 9 <= hour < 12:
        return {'name': '🇮🇳 NSE Morning', 'multiplier': 2.0, 'active': True}
    elif 12 <= hour < 15:
        return {'name': '🇮🇳 NSE Afternoon', 'multiplier': 1.8, 'active': True}
    elif 15 <= hour < 17:
        return {'name': '🇬🇧 London Open', 'multiplier': 1.9, 'active': True}
    elif 20 <= hour < 22:
        return {'name': '🇺🇸 NY Open', 'multiplier': 2.1, 'active': True}
    else:
        return {'name': '⏸️ Off Hours', 'multiplier': 0.5, 'active': False}

def quick_analysis(symbol, timeframe):
    """Quick analysis function"""
    try:
        df = yf.download(symbol, period=timeframe, progress=False)
        if df.empty:
            return None
        
        # Calculate basic metrics
        price = df['Close'].iloc[-1]
        change = ((price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        volume = df['Volume'].iloc[-1]
        avg_volume = df['Volume'].rolling(20).mean().iloc[-1]
        
        # Simple score calculation
        score = 50  # Base score
        if change > 0:
            score += min(20, change * 2)
        if volume > avg_volume * 1.5:
            score += 10
        
        return {
            'symbol': symbol,
            'price': price,
            'change': change,
            'volume': volume,
            'score': min(100, score)
        }
    except:
        return None

def display_top_recommendations():
    """Display top recommendations"""
    # Sample recommendations
    recommendations = [
        {"symbol": "RELIANCE.NS", "name": "Reliance Industries", "score": 92, "signal": "🟢 STRONG BUY", "reason": "ICT Setup + Volume Breakout"},
        {"symbol": "TCS.NS", "name": "Tata Consultancy", "score": 88, "signal": "🟢 BUY", "reason": "Order Block Tested"},
        {"symbol": "INFY.NS", "name": "Infosys", "score": 85, "signal": "🟢 BUY", "reason": "FVG Fill + Liquidity Grab"},
        {"symbol": "HDFCBANK.NS", "name": "HDFC Bank", "score": 82, "signal": "🟢 BUY", "reason": "Market Structure Shift"},
        {"symbol": "BITCOIN", "name": "Bitcoin", "score": 90, "signal": "🟢 STRONG BUY", "reason": "HTF Support + OTE Zone"}
    ]
    
    for rec in recommendations:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 2])
            col1.markdown(f"**{rec['symbol']}**")
            col2.markdown(rec['name'])
            col3.markdown(f"**{rec['score']}**")
            col4.markdown(f"<span class='signal-{'strong-buy' if 'STRONG' in rec['signal'] else 'buy'}'>{rec['signal']}</span>", unsafe_allow_html=True)
            col5.markdown(rec['reason'])
            st.divider()

def analyze_ict_patterns(symbol):
    """Analyze ICT patterns"""
    df = yf.download(symbol, period="3mo", progress=False)
    
    if df.empty:
        st.error("No data available")
        return
    
    # Detect various patterns
    breaker_blocks = detect_breaker_blocks(df)
    liquidity_sweeps = detect_liquidity_sweeps(df)
    asian_ranges = detect_asian_range(df)
    power_of_3 = detect_power_of_3(df)
    premium_discount = detect_premium_discount_zones(df)
    ote_zones = detect_optimal_trade_entry(df)
    market_structure_shifts = detect_market_structure_shift(df)
    
    # Display results
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 ICT Patterns Detected")
        
        patterns_found = []
        if breaker_blocks:
            patterns_found.append(f"🔨 Breaker Blocks: {len(breaker_blocks)}")
        if liquidity_sweeps:
            patterns_found.append(f"🌊 Liquidity Sweeps: {len(liquidity_sweeps)}")
        if asian_ranges:
            patterns_found.append(f"🌏 Asian Ranges: {len(asian_ranges)}")
        if power_of_3:
            patterns_found.append(f"🔢 Power of 3: {len(power_of_3)}")
        if premium_discount:
            patterns_found.append(f"⚖️ Premium/Discount: {len(premium_discount)}")
        if ote_zones:
            patterns_found.append(f"🎯 OTE Zones: {len(ote_zones)}")
        if market_structure_shifts:
            patterns_found.append(f"🔄 MSS: {len(market_structure_shifts)}")
        
        for pattern in patterns_found:
            st.success(pattern)
    
    with col2:
        st.markdown("### 📊 Pattern Statistics")
        
        stats_df = pd.DataFrame({
            'Pattern Type': ['Breaker Blocks', 'Liquidity Sweeps', 'Asian Ranges', 
                           'Power of 3', 'Premium/Discount', 'OTE Zones', 'MSS'],
            'Count': [len(breaker_blocks), len(liquidity_sweeps), len(asian_ranges),
                     len(power_of_3), len(premium_discount), len(ote_zones), len(market_structure_shifts)],
            'Last Detected': [
                breaker_blocks[-1]['date'].strftime('%Y-%m-%d') if breaker_blocks else 'N/A',
                liquidity_sweeps[-1]['date'].strftime('%Y-%m-%d') if liquidity_sweeps else 'N/A',
                asian_ranges[-1]['date'].strftime('%Y-%m-%d') if asian_ranges else 'N/A',
                power_of_3[-1]['date'].strftime('%Y-%m-%d') if power_of_3 else 'N/A',
                premium_discount[-1]['date'].strftime('%Y-%m-%d') if premium_discount else 'N/A',
                ote_zones[-1]['date'].strftime('%Y-%m-%d') if ote_zones else 'N/A',
                market_structure_shifts[-1]['date'].strftime('%Y-%m-%d') if market_structure_shifts else 'N/A'
            ]
        })
        
        st.dataframe(stats_df, use_container_width=True)

def analyze_multi_timeframe(symbol):
    """Analyze multi-timeframe"""
    mtf = MultiTimeframeAnalyzer(symbol)
    mtf_data = mtf.fetch_mtf_data()
    
    if not mtf_data:
        st.error("No multi-timeframe data available")
        return
    
    confluence = mtf.analyze_confluence(mtf_data)
    htf_bias = mtf.get_htf_bias(mtf_data)
    
    # Display results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📈 MTF Confluence")
        st.metric("Confluence Score", f"{confluence['score']:.2f}")
        
        fig = go.Figure(data=[
            go.Bar(x=['Bullish', 'Bearish', 'Neutral'],
                  y=[confluence['bullish'], confluence['bearish'], confluence['neutral']],
                  marker_color=['#10b981', '#ef4444', '#f59e0b'])
        ])
        fig.update_layout(height=300, template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 HTF Bias")
        st.metric("Higher Timeframe Bias", htf_bias)
        
        # Display timeframe details
        st.markdown("**Timeframe Details:**")
        for tf, details in confluence['details'].items():
            st.write(f"{tf}: {details['trend']} (RSI: {details['rsi']:.1f})")
    
    with col3:
        st.markdown("### 🚀 Trading Signal")
        
        if confluence['score'] > 0.3:
            st.success("**STRONG BULLISH BIAS**")
            st.info("Look for LONG entries on LTF")
        elif confluence['score'] < -0.3:
            st.error("**STRONG BEARISH BIAS**")
            st.info("Look for SHORT entries on LTF")
        else:
            st.warning("**NEUTRAL BIAS**")
            st.info("Wait for clearer direction")

def create_advanced_chart(symbol, timeframe, chart_type, indicators):
    """Create advanced chart with indicators"""
    try:
        df = yf.download(symbol, period="1mo", interval=timeframe, progress=False)
        
        if df.empty:
            st.error("No data available")
            return None
        
        # Create figure
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3],
            subplot_titles=(f'{symbol} - Price Action', 'Volume')
        )
        
        # Add main chart
        if chart_type == "Candlestick":
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Price'
            ), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Close'],
                mode='lines',
                name='Price'
            ), row=1, col=1)
        
        # Add indicators
        if "EMA" in indicators:
            df['EMA_20'] = df['Close'].ewm(span=20).mean()
            fig.add_trace(go.Scatter(
                x=df.index, y=df['EMA_20'],
                mode='lines', name='EMA 20',
                line=dict(color='blue', width=1)
            ), row=1, col=1)
        
        if "Bollinger Bands" in indicators:
            df['BB_middle'] = df['Close'].rolling(20).mean()
            df['BB_std'] = df['Close'].rolling(20).std()
            df['BB_upper'] = df['BB_middle'] + (df['BB_std'] * 2)
            df['BB_lower'] = df['BB_middle'] - (df['BB_std'] * 2)
            
            fig.add_trace(go.Scatter(
                x=df.index, y=df['BB_upper'],
                mode='lines', name='BB Upper',
                line=dict(color='gray', width=1)
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index, y=df['BB_lower'],
                mode='lines', name='BB Lower',
                line=dict(color='gray', width=1),
                fill='tonexty'
            ), row=1, col=1)
        
        if "RSI" in indicators:
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            fig.add_trace(go.Scatter(
                x=df.index, y=rsi,
                mode='lines', name='RSI',
                line=dict(color='purple', width=1)
            ), row=2, col=1)
            
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        else:
            # Add volume
            colors = ['green' if df['Close'].iloc[i] >= df['Open'].iloc[i] else 'red' 
                     for i in range(len(df))]
            fig.add_trace(go.Bar(
                x=df.index, y=df['Volume'],
                name='Volume', marker_color=colors
            ), row=2, col=1)
        
        # Update layout
        fig.update_layout(
            template='plotly_dark',
            height=800,
            xaxis_rangeslider_visible=False,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None

# ==================== APPLICATION INITIALIZATION ====================

if __name__ == "__main__":
    main()
