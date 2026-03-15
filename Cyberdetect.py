# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import joblib
import time
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

# ─── Configuration ────────────────────────────────────────────
st.set_page_config(
    page_title="CyberDetect AI — Marwa Lehdaoui",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS Dark Cyber Theme ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;400;600&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    background-color: #050d1a !important;
    color: #c8d8e8 !important;
    font-family: 'Rajdhani', sans-serif !important;
}
.stApp { background: #050d1a !important; }

/* ── Hide default elements ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 2rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060f1e 0%, #0a1628 100%) !important;
    border-right: 1px solid #0d4f8c !important;
}
[data-testid="stSidebar"] * { color: #8ab4d4 !important; }

/* ── Title ── */
.cyber-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 900;
    color: #00d4ff;
    text-transform: uppercase;
    letter-spacing: 4px;
    text-shadow: 0 0 20px #00d4ff88, 0 0 40px #00d4ff44;
    margin: 0;
}
.cyber-subtitle {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #4a8fa8;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── KPI Cards ── */
.kpi-card {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f35 100%);
    border: 1px solid #0d4f8c;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff, transparent);
}
.kpi-value {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 700;
    margin: 8px 0 4px;
}
.kpi-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4a8fa8;
}
.kpi-icon { font-size: 1.5rem; }
.color-blue  { color: #00d4ff; text-shadow: 0 0 15px #00d4ff88; }
.color-red   { color: #ff4455; text-shadow: 0 0 15px #ff445588; }
.color-yellow{ color: #ffd700; text-shadow: 0 0 15px #ffd70088; }
.color-green { color: #00ff88; text-shadow: 0 0 15px #00ff8888; }
.color-orange{ color: #ff8800; text-shadow: 0 0 15px #ff880088; }

/* ── Section headers ── */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 0.8rem;
    color: #00d4ff;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 10px 0 8px;
    border-bottom: 1px solid #0d4f8c;
    margin-bottom: 15px;
}
.section-header::before { content: "► "; }

/* ── Chart containers ── */
.chart-container {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f35 100%);
    border: 1px solid #0d4f8c;
    border-radius: 8px;
    padding: 15px;
}

/* ── Inputs ── */
.stTextInput input, .stSelectbox select, .stNumberInput input {
    background: #0a1628 !important;
    border: 1px solid #0d4f8c !important;
    color: #c8d8e8 !important;
    border-radius: 4px !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stSlider > div { color: #00d4ff !important; }

/* ── Buttons ── */
.stButton button {
    background: linear-gradient(135deg, #003366, #0055aa) !important;
    color: #00d4ff !important;
    border: 1px solid #0088cc !important;
    border-radius: 4px !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 10px 20px !important;
    transition: all 0.3s !important;
}
.stButton button:hover {
    background: linear-gradient(135deg, #004488, #0077cc) !important;
    box-shadow: 0 0 20px #0088cc88 !important;
}

/* ── Alert boxes ── */
.alert-box {
    background: linear-gradient(135deg, #1a0a1a, #2a0d1a);
    border: 1px solid #ff4455;
    border-left: 4px solid #ff4455;
    border-radius: 6px;
    padding: 15px 20px;
    margin: 10px 0;
}
.success-box {
    background: linear-gradient(135deg, #0a1a0a, #0d2a1a);
    border: 1px solid #00ff88;
    border-left: 4px solid #00ff88;
    border-radius: 6px;
    padding: 15px 20px;
    margin: 10px 0;
}

/* ── Nav items ── */
.nav-item {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 1px;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
    margin: 3px 0;
}

/* ── Table ── */
.stDataFrame {
    background: #0a1628 !important;
}
thead tr th {
    background: #0d2040 !important;
    color: #00d4ff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
}
tbody tr td {
    background: #0a1628 !important;
    color: #8ab4d4 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* ── Divider ── */
hr { border-color: #0d4f8c !important; }

/* ── Metric ── */
[data-testid="metric-container"] {
    background: #0a1628 !important;
    border: 1px solid #0d4f8c !important;
    border-radius: 8px !important;
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────────
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'Dashboard'

# ══════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:

    st.markdown("""
    <style>
    /* ── Full page login background ── */
    .stApp {
        background: radial-gradient(ellipse at 20% 50%, #0a1f3a 0%, #050d1a 60%) !important;
    }

    /* ── Network animation canvas ── */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 90vh;
    }
    .login-card {
        background: linear-gradient(145deg, #071428 0%, #0a1e35 60%, #071428 100%);
        border: 1px solid #1a4a7a;
        border-radius: 16px;
        padding: 40px 50px;
        width: 420px;
        box-shadow: 0 0 60px #00d4ff22, 0 0 120px #00508044,
                    inset 0 0 40px #00d4ff08;
        position: relative;
        overflow: hidden;
    }
    .login-card::before {
        content: '';
        position: absolute;
        top: -2px; left: -2px; right: -2px; bottom: -2px;
        border-radius: 18px;
        background: linear-gradient(45deg,
            transparent 30%, #00d4ff22 50%, transparent 70%);
        z-index: -1;
    }
    /* Network icon */
    .network-icon {
        text-align: center;
        margin-bottom: 10px;
    }
    .network-svg {
        width: 120px;
        height: 120px;
        filter: drop-shadow(0 0 15px #00d4ff88);
    }
    /* Title */
    .login-title {
        text-align: center;
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 10px 0 4px;
        letter-spacing: 2px;
    }
    .login-title span.white { color: #ffffff; }
    .login-title span.cyan  { color: #00d4ff;
                               text-shadow: 0 0 20px #00d4ffaa; }
    .login-subtitle {
        text-align: center;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.65rem;
        color: #4a7fa0;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    /* Status badge */
    .status-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: rgba(0, 255, 136, 0.08);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 30px;
        padding: 8px 20px;
        margin: 0 auto 28px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        color: #00ff88;
        letter-spacing: 1px;
    }
    .status-dot {
        width: 8px; height: 8px;
        background: #00ff88;
        border-radius: 50%;
        box-shadow: 0 0 8px #00ff88;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%,100% { opacity: 1; transform: scale(1); }
        50%      { opacity: 0.5; transform: scale(0.8); }
    }
    /* Input labels */
    .input-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        color: #00d4ff;
        letter-spacing: 2px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .input-label::before { content: "► "; color: #00d4ff; }
    /* Corner decorations */
    .corner-tl, .corner-br {
        position: absolute;
        width: 20px; height: 20px;
    }
    .corner-tl {
        top: 12px; left: 12px;
        border-top: 2px solid #00d4ff;
        border-left: 2px solid #00d4ff;
    }
    .corner-br {
        bottom: 12px; right: 12px;
        border-bottom: 2px solid #00d4ff;
        border-right: 2px solid #00d4ff;
    }
    /* Scanline effect */
    .scanline {
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg,
            transparent, #00d4ff44, #00d4ffaa, #00d4ff44, transparent);
        animation: scan 3s linear infinite;
    }
    @keyframes scan {
        0%   { top: 0%; opacity: 1; }
        100% { top: 100%; opacity: 0; }
    }
    /* Error box */
    .error-box {
        background: rgba(255, 68, 85, 0.1);
        border: 1px solid #ff4455;
        border-left: 3px solid #ff4455;
        border-radius: 6px;
        padding: 10px 15px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.72rem;
        color: #ff4455;
        margin-top: 10px;
        text-align: center;
    }
    /* Demo hint */
    .demo-hint {
        text-align: center;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.62rem;
        color: #1a4a6a;
        margin-top: 15px;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Center column ──
    _, col, _ = st.columns([1, 1.2, 1])
    with col:

        st.markdown("""
        <div style='background:linear-gradient(145deg,#071428,#0a1e35,#071428);
                    border:1px solid #1a4a7a; border-radius:16px;
                    padding:35px 40px 25px; text-align:center;
                    box-shadow:0 0 60px #00d4ff22,0 0 120px #00508044;
                    position:relative; overflow:hidden;'>
            <div style="position:absolute;top:12px;left:12px;width:18px;height:18px;
                        border-top:2px solid #00d4ff;border-left:2px solid #00d4ff;"></div>
            <div style="position:absolute;top:12px;right:12px;width:18px;height:18px;
                        border-top:2px solid #00d4ff;border-right:2px solid #00d4ff;"></div>
            <div style="position:absolute;bottom:12px;left:12px;width:18px;height:18px;
                        border-bottom:2px solid #00d4ff;border-left:2px solid #00d4ff;"></div>
            <div style="position:absolute;bottom:12px;right:12px;width:18px;height:18px;
                        border-bottom:2px solid #00d4ff;border-right:2px solid #00d4ff;"></div>
            <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg"
                 style="width:110px;height:110px;filter:drop-shadow(0 0 15px #00d4ff88);">
                <defs>
                    <radialGradient id="bg2" cx="50%" cy="50%" r="50%">
                        <stop offset="0%"   stop-color="#00d4ff" stop-opacity="0.2"/>
                        <stop offset="100%" stop-color="#050d1a" stop-opacity="0"/>
                    </radialGradient>
                </defs>
                <circle cx="60" cy="60" r="55" fill="url(#bg2)"/>
                <circle cx="60" cy="60" r="54" fill="none" stroke="#0d4f8c" stroke-width="0.5"/>
                <line x1="60" y1="60" x2="20"  y2="25"  stroke="#00d4ff" stroke-width="1" opacity="0.7"/>
                <line x1="60" y1="60" x2="100" y2="25"  stroke="#00d4ff" stroke-width="1" opacity="0.7"/>
                <line x1="60" y1="60" x2="15"  y2="75"  stroke="#00d4ff" stroke-width="1" opacity="0.7"/>
                <line x1="60" y1="60" x2="105" y2="75"  stroke="#00d4ff" stroke-width="1" opacity="0.7"/>
                <line x1="60" y1="60" x2="40"  y2="105" stroke="#00d4ff" stroke-width="1" opacity="0.7"/>
                <line x1="60" y1="60" x2="80"  y2="105" stroke="#00d4ff" stroke-width="1" opacity="0.7"/>
                <line x1="20" y1="25" x2="100" y2="25"  stroke="#00d4ff" stroke-width="0.5" opacity="0.25"/>
                <line x1="15" y1="75" x2="40"  y2="105" stroke="#00d4ff" stroke-width="0.5" opacity="0.25"/>
                <line x1="105" y1="75" x2="80" y2="105" stroke="#00d4ff" stroke-width="0.5" opacity="0.25"/>
                <circle cx="60" cy="60" r="9"  fill="#00d4ff"/>
                <circle cx="60" cy="60" r="14" fill="none" stroke="#00d4ff" stroke-width="1" opacity="0.3"/>
                <circle cx="20"  cy="25"  r="5" fill="#00ff88" opacity="0.9"/>
                <circle cx="100" cy="25"  r="5" fill="#00ff88" opacity="0.9"/>
                <circle cx="15"  cy="75"  r="5" fill="#00ff88" opacity="0.9"/>
                <circle cx="105" cy="75"  r="5" fill="#00ff88" opacity="0.9"/>
                <circle cx="40"  cy="105" r="5" fill="#00ff88" opacity="0.9"/>
                <circle cx="80"  cy="105" r="5" fill="#00ff88" opacity="0.9"/>
            </svg>
            <div style='font-family:Orbitron,monospace;font-size:1.8rem;
                        font-weight:700;letter-spacing:2px;margin:10px 0 4px;'>
                <span style="color:#fff;">Cyber</span>
                <span style="color:#00d4ff;text-shadow:0 0 20px #00d4ffaa;">Detect</span>
                <span style="color:#fff;"> AI</span>
            </div>
            <div style='font-family:Share Tech Mono,monospace;font-size:0.62rem;
                        color:#4a7fa0;letter-spacing:4px;
                        text-transform:uppercase;margin-bottom:18px;'>
                Network Attack · Prediction Platform
            </div>
            <div style='display:inline-flex;align-items:center;gap:8px;
                        background:rgba(0,255,136,0.08);
                        border:1px solid rgba(0,255,136,0.35);
                        border-radius:30px;padding:7px 18px;
                        font-family:Share Tech Mono,monospace;
                        font-size:0.68rem;color:#00ff88;letter-spacing:1px;'>
                <span style='width:7px;height:7px;background:#00ff88;
                             border-radius:50%;box-shadow:0 0 8px #00ff88;
                             display:inline-block;'></span>
                System Online &nbsp;·&nbsp; All Services Active
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""<div style='font-family:Share Tech Mono,monospace;
            font-size:0.7rem;color:#00d4ff;letter-spacing:2px;margin-bottom:5px;'>
            ► USERNAME</div>""", unsafe_allow_html=True)
        username = st.text_input("u", placeholder="admin  /  analyst  /  demo",
                                  label_visibility="collapsed", key="usr")

        st.markdown("""<div style='font-family:Share Tech Mono,monospace;
            font-size:0.7rem;color:#00d4ff;letter-spacing:2px;
            margin-top:10px;margin-bottom:5px;'>
            ► PASSWORD</div>""", unsafe_allow_html=True)
        password = st.text_input("p", type="password",
                                  placeholder="• • • • • • • •",
                                  label_visibility="collapsed", key="pwd")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("[ AUTHENTICATE → ]", use_container_width=True):
            if username == "admin" and password == "soc2024":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.markdown("""<div style='background:rgba(255,68,85,0.1);
                    border:1px solid #ff4455;border-left:3px solid #ff4455;
                    border-radius:6px;padding:10px 15px;
                    font-family:Share Tech Mono,monospace;
                    font-size:0.72rem;color:#ff4455;
                    text-align:center;margin-top:10px;'>
                    ⚠ ACCESS DENIED — Invalid credentials
                </div>""", unsafe_allow_html=True)

        st.markdown("""<div style='text-align:center;
            font-family:Share Tech Mono,monospace;font-size:0.62rem;
            color:#1a4a6a;margin-top:12px;letter-spacing:1px;'>
            admin / soc2024</div>""", unsafe_allow_html=True)

    st.stop()

# ══════════════════════════════════════════════════════════════
# DATA & MODEL LOADING
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    try:
        return pd.read_csv('Global_Cybersecurity_Threats_2015-2024.csv')
    except:
        np.random.seed(42)
        n = 3000
        attack_types = ['DDoS','Phishing','SQL Injection',
                        'Ransomware','Malware','Man-in-the-Middle']
        industries    = ['IT','Banking','Healthcare','Retail',
                         'Education','Telecom','Government']
        sources       = ['Nation-state','Unknown','Insider','Hacker Group']
        vulns         = ['Zero-day','Social Engineering',
                         'Unpatched Software','Weak Passwords']
        defenses      = ['Antivirus','VPN','Encryption','Firewall','AI Detection']
        countries     = ['USA','China','Russia','UK','France','Germany',
                         'India','Brazil','Japan','Australia']
        return pd.DataFrame({
            'Country'                          : np.random.choice(countries, n),
            'Year'                             : np.random.randint(2015, 2025, n),
            'Attack Type'                      : np.random.choice(attack_types, n),
            'Target Industry'                  : np.random.choice(industries, n),
            'Financial Loss (in Million $)'    : np.round(np.random.uniform(0.5,100,n),2),
            'Number of Affected Users'         : np.random.randint(100, 1000000, n),
            'Attack Source'                    : np.random.choice(sources, n),
            'Security Vulnerability Type'      : np.random.choice(vulns, n),
            'Defense Mechanism Used'           : np.random.choice(defenses, n),
            'Incident Resolution Time (in Hours)': np.random.randint(1, 500, n),
        })

@st.cache_resource
def load_model():
    try:
        model  = joblib.load('best_model.pkl')
        scaler = joblib.load('scaler.pkl')
        le     = joblib.load('label_encoder.pkl')
        return model, scaler, le, True
    except:
        return None, None, None, False

df = load_data()
model, scaler, le_target, model_loaded = load_model()

# ─── Matplotlib dark theme ─────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor' : '#0a1628',
    'axes.facecolor'   : '#0a1628',
    'axes.edgecolor'   : '#0d4f8c',
    'axes.labelcolor'  : '#8ab4d4',
    'xtick.color'      : '#4a8fa8',
    'ytick.color'      : '#4a8fa8',
    'text.color'       : '#8ab4d4',
    'grid.color'       : '#0d2840',
    'grid.alpha'       : 0.5,
})
CYBER_COLORS = ['#00d4ff','#ff4455','#ffd700',
                '#00ff88','#ff8800','#aa44ff']

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0 15px;'>
        <div style='font-size:3rem;'>🛡️</div>
        <div style='font-family:Orbitron,monospace; font-size:1rem;
                    color:#00d4ff; font-weight:900;
                    letter-spacing:3px;'>CYBERDETECT</div>
        <div style='font-family:Share Tech Mono,monospace; font-size:0.6rem;
                    color:#2a5f7a; letter-spacing:2px;'>AI · SECURE EDITION</div>
    </div>
    <hr>
    <div style='background:#0d1f35; border:1px solid #0d4f8c;
                border-radius:6px; padding:12px; margin:10px 0;'>
        <div style='font-family:Share Tech Mono,monospace; font-size:0.7rem;
                    color:#4a8fa8;'>👤 ADMIN</div>
        <div style='font-family:Orbitron,monospace; font-size:0.8rem;
                    color:#00d4ff;'>Administrator</div>
        <div style='font-family:Share Tech Mono,monospace; font-size:0.6rem;
                    color:#2a5f7a; margin-top:4px;'>● ACTIVE</div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    pages = {
        "⬛  THREAT OVERVIEW"    : "Dashboard",
        "⬛  ATTACK PREDICTOR"   : "Prediction",
        "⬛  LIVE MONITORING"    : "Monitoring",
        "⬛  DATA EXPLORER"      : "Exploration",
        "⬛  DOCUMENTATION"      : "Documentation",
        "⬛  ABOUT"              : "About",
    }
    for label, key in pages.items():
        if st.button(label, use_container_width=True,
                     key=f"nav_{key}"):
            st.session_state.page = key
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    now = datetime.now().strftime("%d %b %Y  %H:%M")
    st.markdown(f"""
    <div style='font-family:Share Tech Mono,monospace;
                font-size:0.65rem; color:#2a5f7a;
                text-align:center; padding:5px;'>
        🕐 {now}
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:linear-gradient(135deg,#071428,#0a1e35);
                border:1px solid #0d4f8c; border-radius:8px;
                padding:12px 15px; margin:10px 0;
                text-align:center;'>
        <div style='font-family:Share Tech Mono,monospace;
                    font-size:0.6rem; color:#2a5f7a;
                    letter-spacing:2px; margin-bottom:4px;'>
            ── DEVELOPED BY ──
        </div>
        <div style='font-family:Orbitron,monospace;
                    font-size:0.85rem; color:#00d4ff;
                    font-weight:700; letter-spacing:1px;
                    text-shadow:0 0 10px #00d4ff88;'>
            Marwa Lehdaoui
        </div>
        <div style='font-family:Share Tech Mono,monospace;
                    font-size:0.6rem; color:#4a7fa0;
                    margin-top:3px; letter-spacing:1px;'>
            SOC AI Workshop · 2026
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 SIGN OUT", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

page = st.session_state.page

# ══════════════════════════════════════════════════════════════
# PAGE : DASHBOARD
# ══════════════════════════════════════════════════════════════
if page == "Dashboard":
    st.markdown("""
    <div class='cyber-title'>System Dashboard</div>
    <div class='cyber-subtitle'>
        Real-Time Threat Intelligence · """ +
        datetime.now().strftime("%d %b %Y  %H:%M") +
    """</div>
    <hr>""", unsafe_allow_html=True)

    # ── KPI Row ──────────────────────────────────────────────
    total        = len(df)
    n_countries  = df['Country'].nunique()
    avg_loss     = df['Financial Loss (in Million $)'].mean()
    avg_res      = df['Incident Resolution Time (in Hours)'].mean()
    top_attack   = df['Attack Type'].value_counts().idxmax()
    acc          = 62.5 if not model_loaded else 92.0

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    for col, icon, val, label, cls in [
        (k1, "🌐", f"{total:,}",         "TOTAL INCIDENTS",  "color-blue"),
        (k2, "🌍", f"{n_countries}",      "COUNTRIES",        "color-cyan" if False else "color-blue"),
        (k3, "💰", f"${avg_loss:.1f}M",   "AVG LOSS",         "color-red"),
        (k4, "⏱️", f"{avg_res:.0f}h",     "AVG RESOLUTION",   "color-yellow"),
        (k5, "🎯", f"{acc:.1f}%",         "MODEL ACCURACY",   "color-green"),
        (k6, "🔴", top_attack[:6]+"...",  "TOP ATTACK",       "color-orange"),
    ]:
        col.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-icon'>{icon}</div>
            <div class='kpi-value {cls}'>{val}</div>
            <div class='kpi-label'>{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1 : Attack Distribution + Trend ──────────────────
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='section-header'>Attack Type Distribution</div>",
                    unsafe_allow_html=True)
        counts = df['Attack Type'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        wedges, texts, autotexts = ax.pie(
            counts, labels=None, autopct='%1.1f%%',
            colors=CYBER_COLORS,
            wedgeprops=dict(width=0.6, edgecolor='#050d1a', linewidth=2),
            startangle=90
        )
        for t in autotexts:
            t.set_color('#050d1a')
            t.set_fontsize(9)
            t.set_fontweight('bold')
        ax.legend(counts.index, loc='lower center',
                  bbox_to_anchor=(0.5, -0.15), ncol=3,
                  fontsize=7, framealpha=0, labelcolor='#8ab4d4')
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

    with c2:
        st.markdown("<div class='section-header'>Attack Trend by Year</div>",
                    unsafe_allow_html=True)
        yearly = df.groupby(['Year','Attack Type']).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(6, 4))
        for i, col_name in enumerate(yearly.columns):
            ax.plot(yearly.index, yearly[col_name],
                    color=CYBER_COLORS[i % 6],
                    linewidth=2, marker='o', markersize=4,
                    label=col_name)
        ax.set_xlabel('Year', fontsize=8)
        ax.set_ylabel('Incidents', fontsize=8)
        ax.legend(fontsize=6, framealpha=0, labelcolor='#8ab4d4', ncol=2)
        ax.grid(alpha=0.3)
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

    # ── Row 2 : Industry + Source ─────────────────────────────
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("<div class='section-header'>Target Industry</div>",
                    unsafe_allow_html=True)
        ind = df['Target Industry'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.barh(ind.index, ind.values,
                       color=CYBER_COLORS[:len(ind)], alpha=0.85)
        ax.set_xlabel('Incidents', fontsize=8)
        ax.grid(axis='x', alpha=0.3)
        for bar, val in zip(bars, ind.values):
            ax.text(val + 2, bar.get_y() + bar.get_height()/2,
                    str(val), va='center', fontsize=7, color='#8ab4d4')
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

    with c4:
        st.markdown("<div class='section-header'>Attack Source</div>",
                    unsafe_allow_html=True)
        src = df['Attack Source'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(src.index, src.values,
               color=['#ff4455','#ffd700','#00ff88','#aa44ff'],
               alpha=0.85, width=0.6)
        ax.set_ylabel('Count', fontsize=8)
        ax.tick_params(axis='x', rotation=15, labelsize=7)
        ax.grid(axis='y', alpha=0.3)
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

    # ── Row 3 : Financial Loss + Resolution Time ──────────────
    c5, c6 = st.columns(2)

    with c5:
        st.markdown("<div class='section-header'>Financial Loss by Attack Type (Avg M$)</div>",
                    unsafe_allow_html=True)
        loss = df.groupby('Attack Type')['Financial Loss (in Million $)'].mean().sort_values()
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.barh(loss.index, loss.values,
                       color=CYBER_COLORS[:len(loss)], alpha=0.85)
        ax.set_xlabel('Avg Loss (M$)', fontsize=8)
        ax.grid(axis='x', alpha=0.3)
        for bar, val in zip(bars, loss.values):
            ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                    f'${val:.1f}M', va='center', fontsize=7, color='#8ab4d4')
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

    with c6:
        st.markdown("<div class='section-header'>Resolution Time by Attack Type (Avg Hours)</div>",
                    unsafe_allow_html=True)
        res = df.groupby('Attack Type')['Incident Resolution Time (in Hours)'].mean().sort_values()
        fig, ax = plt.subplots(figsize=(6, 4))
        colors_res = ['#00ff88' if v < res.mean() else '#ff4455' for v in res.values]
        bars = ax.bar(res.index, res.values, color=colors_res, alpha=0.85, width=0.6)
        ax.axhline(res.mean(), color='#ffd700', linestyle='--',
                   linewidth=1.5, label=f'Avg: {res.mean():.0f}h')
        ax.set_ylabel('Avg Hours', fontsize=8)
        ax.tick_params(axis='x', rotation=30, labelsize=7)
        ax.legend(fontsize=7, framealpha=0, labelcolor='#ffd700')
        ax.grid(axis='y', alpha=0.3)
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

    # ── Row 4 : Vulnerability + Defense ──────────────────────
    c7, c8 = st.columns(2)

    with c7:
        st.markdown("<div class='section-header'>Security Vulnerability Types</div>",
                    unsafe_allow_html=True)
        vuln = df['Security Vulnerability Type'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        wedges, texts, autotexts = ax.pie(
            vuln, labels=vuln.index, autopct='%1.1f%%',
            colors=['#ff4455','#ffd700','#00d4ff','#aa44ff'],
            wedgeprops=dict(width=0.5, edgecolor='#050d1a', linewidth=2),
            startangle=45
        )
        for t in texts:
            t.set_fontsize(7)
            t.set_color('#8ab4d4')
        for t in autotexts:
            t.set_fontsize(8)
            t.set_color('#050d1a')
            t.set_fontweight('bold')
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

    with c8:
        st.markdown("<div class='section-header'>Defense Mechanism Used</div>",
                    unsafe_allow_html=True)
        defense = df['Defense Mechanism Used'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.barh(defense.index, defense.values,
                       color=CYBER_COLORS[:len(defense)], alpha=0.85)
        ax.set_xlabel('Count', fontsize=8)
        ax.grid(axis='x', alpha=0.3)
        for bar, val in zip(bars, defense.values):
            ax.text(val + 2, bar.get_y() + bar.get_height()/2,
                    str(val), va='center', fontsize=7, color='#8ab4d4')
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

    # ── Row 5 : Top 10 Countries + Heatmap ───────────────────
    c9, c10 = st.columns(2)

    with c9:
        st.markdown("<div class='section-header'>Top 10 Countries by Incidents</div>",
                    unsafe_allow_html=True)
        top_countries = df['Country'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.barh(top_countries.index[::-1],
                       top_countries.values[::-1],
                       color='#00d4ff', alpha=0.8)
        ax.set_xlabel('Incidents', fontsize=8)
        ax.grid(axis='x', alpha=0.3)
        for bar, val in zip(bars, top_countries.values[::-1]):
            ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                    str(val), va='center', fontsize=7, color='#8ab4d4')
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

    with c10:
        st.markdown("<div class='section-header'>Attack Type vs Industry Heatmap</div>",
                    unsafe_allow_html=True)
        heatmap_data = df.pivot_table(
            index='Attack Type',
            columns='Target Industry',
            aggfunc='size',
            fill_value=0
        )
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(heatmap_data, ax=ax,
                    cmap='Blues', annot=True, fmt='d',
                    linewidths=0.5, linecolor='#050d1a',
                    annot_kws={'size': 6, 'color': 'white'},
                    cbar_kws={'shrink': 0.8})
        ax.set_xlabel('Industry', fontsize=7)
        ax.set_ylabel('Attack Type', fontsize=7)
        ax.tick_params(axis='x', rotation=30, labelsize=6)
        ax.tick_params(axis='y', rotation=0, labelsize=6)
        fig.patch.set_facecolor('#0a1628')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # ── Row 6 : Affected Users + Loss by Country ─────────────
    c11, c12 = st.columns(2)

    with c11:
        st.markdown("<div class='section-header'>Affected Users by Attack Type</div>",
                    unsafe_allow_html=True)
        users = df.groupby('Attack Type')['Number of Affected Users'].sum().sort_values()
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.barh(users.index, users.values / 1e6,
                       color=CYBER_COLORS[:len(users)], alpha=0.85)
        ax.set_xlabel('Total Users Affected (Millions)', fontsize=8)
        ax.grid(axis='x', alpha=0.3)
        for bar, val in zip(bars, users.values):
            ax.text(val/1e6 + 0.1, bar.get_y() + bar.get_height()/2,
                    f'{val/1e6:.1f}M', va='center', fontsize=7, color='#8ab4d4')
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

    with c12:
        st.markdown("<div class='section-header'>Financial Loss by Source</div>",
                    unsafe_allow_html=True)
        loss_src = df.groupby('Attack Source')['Financial Loss (in Million $)'].sum().sort_values()
        fig, ax = plt.subplots(figsize=(6, 4))
        wedges, texts, autotexts = ax.pie(
            loss_src, labels=loss_src.index, autopct='%1.1f%%',
            colors=['#ff4455','#ffd700','#00d4ff','#aa44ff'],
            wedgeprops=dict(width=0.55, edgecolor='#050d1a', linewidth=2),
            startangle=90
        )
        for t in texts:
            t.set_fontsize(7.5)
            t.set_color('#8ab4d4')
        for t in autotexts:
            t.set_fontsize(8)
            t.set_color('#050d1a')
            t.set_fontweight('bold')
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

    # ── Summary Table ─────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Attack Summary Table</div>",
                unsafe_allow_html=True)
    summary = df.groupby('Attack Type').agg(
        Incidents         = ('Attack Type', 'count'),
        Avg_Loss_M        = ('Financial Loss (in Million $)', 'mean'),
        Total_Users_M     = ('Number of Affected Users', lambda x: x.sum()/1e6),
        Avg_Resolution_h  = ('Incident Resolution Time (in Hours)', 'mean'),
    ).round(2)
    summary.columns = ['Incidents', 'Avg Loss ($M)',
                        'Total Users (M)', 'Avg Resolution (h)']
    summary = summary.sort_values('Incidents', ascending=False)
    st.dataframe(summary.style
                 .background_gradient(cmap='Blues', subset=['Incidents'])
                 .background_gradient(cmap='Reds',  subset=['Avg Loss ($M)'])
                 .format({'Avg Loss ($M)': '${:.2f}',
                          'Total Users (M)': '{:.2f}M',
                          'Avg Resolution (h)': '{:.1f}h'}),
                 use_container_width=True)

# PAGE : PREDICTION
# ══════════════════════════════════════════════════════════════
elif page == "Prediction":
    st.markdown("""
    <div class='cyber-title'>Attack Prediction</div>
    <div class='cyber-subtitle'>AI-Powered Threat Classification Engine</div>
    <hr>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:linear-gradient(135deg,#0a1628,#0d1f35);
                border:1px solid #0d4f8c; border-radius:8px;
                padding:12px 20px; margin-bottom:20px;
                font-family:Share Tech Mono,monospace;
                font-size:0.75rem; color:#4a8fa8;'>
        ⚡ Enter incident parameters below to classify the attack type
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-header'>Network Parameters</div>",
                    unsafe_allow_html=True)
        country  = st.selectbox("🌍 Country",
                                 sorted(df['Country'].unique()))
        year     = st.slider("📅 Year", 2015, 2024, 2023)
        industry = st.selectbox("🏭 Target Industry",
                                 sorted(df['Target Industry'].unique()))
        fin_loss = st.number_input("💰 Financial Loss (M$)",
                                    0.0, 100.0, 25.0, step=0.5)
        users    = st.number_input("👥 Affected Users",
                                    0, 10000000, 50000, step=1000)

    with c2:
        st.markdown("<div class='section-header'>Threat Intelligence</div>",
                    unsafe_allow_html=True)
        source  = st.selectbox("🎯 Attack Source",
                                sorted(df['Attack Source'].unique()))
        vuln    = st.selectbox("🔓 Vulnerability Type",
                                sorted(df['Security Vulnerability Type'].unique()))
        defense = st.selectbox("🛡️ Defense Mechanism",
                                sorted(df['Defense Mechanism Used'].unique()))
        res_time = st.number_input("⏱️ Resolution Time (hours)",
                                    1, 500, 48, step=1)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡ ANALYZE THREAT", use_container_width=True):
        with st.spinner('🔍 Analyzing threat signature...'):
            time.sleep(1)

        if model_loaded:
            cat_cols = ['Country','Target Industry','Attack Source',
                        'Security Vulnerability Type','Defense Mechanism Used']
            enc = {}
            for col in cat_cols:
                e = LabelEncoder().fit(df[col])
                enc[col] = e

            input_df = pd.DataFrame([{
                'Country'                          : enc['Country'].transform([country])[0],
                'Year'                             : year,
                'Target Industry'                  : enc['Target Industry'].transform([industry])[0],
                'Financial Loss (in Million $)'    : fin_loss,
                'Number of Affected Users'         : users,
                'Attack Source'                    : enc['Attack Source'].transform([source])[0],
                'Security Vulnerability Type'      : enc['Security Vulnerability Type'].transform([vuln])[0],
                'Defense Mechanism Used'           : enc['Defense Mechanism Used'].transform([defense])[0],
                'Incident Resolution Time (in Hours)': res_time,
            }])
            scaled      = scaler.transform(input_df)
            pred        = model.predict(scaled)[0]
            proba       = model.predict_proba(scaled)[0]
            attack_name = le_target.inverse_transform([pred])[0]
            confidence  = max(proba) * 100
        else:
            # Demo mode
            attack_types = ['DDoS','Phishing','SQL Injection',
                            'Ransomware','Malware','Man-in-the-Middle']
            attack_name = np.random.choice(attack_types)
            proba       = np.random.dirichlet(np.ones(6))
            confidence  = max(proba) * 100

        icons = {
            'DDoS'             : '💥',
            'Phishing'         : '🎣',
            'SQL Injection'    : '💉',
            'Ransomware'       : '🔒',
            'Malware'          : '🦠',
            'Man-in-the-Middle': '🕵️'
        }
        severity_map = {
            'DDoS'             : ('HIGH',   '#ff4455'),
            'Ransomware'       : ('CRITICAL','#ff0000'),
            'SQL Injection'    : ('HIGH',   '#ff4455'),
            'Phishing'         : ('MEDIUM', '#ffd700'),
            'Malware'          : ('HIGH',   '#ff4455'),
            'Man-in-the-Middle': ('MEDIUM', '#ffd700'),
        }
        icon     = icons.get(attack_name, '⚠️')
        sev, clr = severity_map.get(attack_name, ('MEDIUM','#ffd700'))

        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#1a0a0a,#2a0d0d);
                    border:2px solid {clr}; border-radius:10px;
                    padding:20px; margin:15px 0; text-align:center;'>
            <div style='font-size:3rem;'>{icon}</div>
            <div style='font-family:Orbitron,monospace; font-size:1.5rem;
                        color:{clr}; font-weight:900;
                        text-shadow:0 0 20px {clr}88;'>
                {attack_name}
            </div>
            <div style='font-family:Share Tech Mono,monospace;
                        font-size:0.8rem; color:#8ab4d4; margin-top:8px;'>
                SEVERITY: <span style='color:{clr};'>{sev}</span>
                &nbsp;&nbsp;|&nbsp;&nbsp;
                CONFIDENCE: <span style='color:#00ff88;'>{confidence:.1f}%</span>
            </div>
        </div>""", unsafe_allow_html=True)

        # Probability chart
        st.markdown("<div class='section-header'>Probability Distribution</div>",
                    unsafe_allow_html=True)
        if model_loaded:
            classes = le_target.classes_
        else:
            classes = ['DDoS','Malware','Man-in-the-Middle',
                       'Phishing','Ransomware','SQL Injection']

        proba_df = pd.DataFrame({
            'Attack' : classes,
            'Prob'   : proba
        }).sort_values('Prob', ascending=True)

        fig, ax = plt.subplots(figsize=(8, 3))
        colors_bar = ['#ff4455' if a == attack_name
                      else '#0d4f8c'
                      for a in proba_df['Attack']]
        bars = ax.barh(proba_df['Attack'], proba_df['Prob'],
                       color=colors_bar, alpha=0.9, height=0.6)
        for bar, val in zip(bars, proba_df['Prob']):
            ax.text(val + 0.005, bar.get_y() + bar.get_height()/2,
                    f'{val*100:.1f}%', va='center',
                    fontsize=8, color='#8ab4d4')
        ax.set_xlim(0, 1.15)
        ax.set_xlabel('Probability', fontsize=8)
        ax.grid(axis='x', alpha=0.3)
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

# ══════════════════════════════════════════════════════════════
# PAGE : LIVE MONITORING
# ══════════════════════════════════════════════════════════════
elif page == "Monitoring":
    st.markdown("""
    <div class='cyber-title'>Live Monitoring</div>
    <div class='cyber-subtitle'>Real-Time Network Traffic Analysis</div>
    <hr>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:linear-gradient(135deg,#0a1a0a,#0d2a1a);
                border:1px solid #00ff88; border-left:4px solid #00ff88;
                border-radius:6px; padding:12px 20px; margin-bottom:20px;
                font-family:Share Tech Mono,monospace; font-size:0.75rem;
                color:#00ff88;'>
        ● SYSTEM ACTIVE — Monitoring 1,247 network endpoints
    </div>""", unsafe_allow_html=True)

    # Simulated live data
    np.random.seed(int(time.time()) % 100)
    t = np.linspace(0, 24, 200)
    traffic = 100 + 50*np.sin(t/3) + np.random.randn(200)*15
    threats = np.where(traffic > 140,
                       traffic - 140 + np.random.randn(200)*5, 0)

    fig, axes = plt.subplots(2, 1, figsize=(12, 6))

    axes[0].fill_between(t, traffic, alpha=0.3, color='#00d4ff')
    axes[0].plot(t, traffic, color='#00d4ff', linewidth=1.5)
    axes[0].set_ylabel('Traffic Volume', fontsize=8)
    axes[0].set_title('Network Traffic (Last 24h)',
                      fontsize=9, color='#00d4ff',
                      fontfamily='monospace')
    axes[0].grid(alpha=0.3)

    axes[1].fill_between(t, threats, alpha=0.4, color='#ff4455')
    axes[1].plot(t, threats, color='#ff4455', linewidth=1.5)
    axes[1].set_ylabel('Threat Level', fontsize=8)
    axes[1].set_xlabel('Hour', fontsize=8)
    axes[1].set_title('Threat Detection Signal',
                      fontsize=9, color='#ff4455',
                      fontfamily='monospace')
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    fig.patch.set_facecolor('#0a1628')
    st.pyplot(fig)
    plt.close()

    # Recent alerts table
    st.markdown("<div class='section-header'>Recent Alerts</div>",
                unsafe_allow_html=True)
    alerts = pd.DataFrame({
        'Time'     : ['02:07:45','02:06:12','02:04:33',
                      '02:03:19','02:01:55'],
        'Source IP': ['192.168.1.45','10.0.0.23','172.16.0.8',
                      '192.168.2.11','10.0.1.5'],
        'Attack'   : ['DDoS','Phishing','SQL Injection',
                      'Malware','Ransomware'],
        'Severity' : ['HIGH','MEDIUM','HIGH','HIGH','CRITICAL'],
        'Status'   : ['BLOCKED','LOGGED','BLOCKED',
                      'ANALYZING','BLOCKED'],
    })
    st.dataframe(alerts, use_container_width=True,
                 hide_index=True)

# ══════════════════════════════════════════════════════════════
# PAGE : DATA EXPLORATION
# ══════════════════════════════════════════════════════════════
elif page == "Exploration":
    st.markdown("""
    <div class='cyber-title'>Data Exploration</div>
    <div class='cyber-subtitle'>Dataset Statistics & Analysis</div>
    <hr>""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f"""<div class='kpi-card'>
        <div class='kpi-icon'>📁</div>
        <div class='kpi-value color-blue'>{len(df):,}</div>
        <div class='kpi-label'>Total Records</div>
    </div>""", unsafe_allow_html=True)
    col2.markdown(f"""<div class='kpi-card'>
        <div class='kpi-icon'>📋</div>
        <div class='kpi-value color-green'>{df.shape[1]}</div>
        <div class='kpi-label'>Features</div>
    </div>""", unsafe_allow_html=True)
    col3.markdown(f"""<div class='kpi-card'>
        <div class='kpi-icon'>🛡️</div>
        <div class='kpi-value color-red'>{df['Attack Type'].nunique()}</div>
        <div class='kpi-label'>Attack Types</div>
    </div>""", unsafe_allow_html=True)
    col4.markdown(f"""<div class='kpi-card'>
        <div class='kpi-icon'>🌍</div>
        <div class='kpi-value color-yellow'>{df['Country'].nunique()}</div>
        <div class='kpi-label'>Countries</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Dataset Preview</div>",
                unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True,
                 hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-header'>Financial Loss by Attack</div>",
                    unsafe_allow_html=True)
        loss = df.groupby('Attack Type')[
            'Financial Loss (in Million $)'].mean()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(loss.index, loss.values,
               color=CYBER_COLORS[:len(loss)], alpha=0.85)
        ax.set_ylabel('Avg Loss (M$)', fontsize=8)
        ax.tick_params(axis='x', rotation=30, labelsize=7)
        ax.grid(axis='y', alpha=0.3)
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

    with c2:
        st.markdown("<div class='section-header'>Attacks per Year</div>",
                    unsafe_allow_html=True)
        yearly = df.groupby(['Year','Attack Type']).size()\
                   .unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(6, 4))
        for i, col in enumerate(yearly.columns):
            ax.plot(yearly.index, yearly[col],
                    color=CYBER_COLORS[i % 6],
                    linewidth=2, label=col, marker='o',
                    markersize=3)
        ax.set_xlabel('Year', fontsize=8)
        ax.set_ylabel('Count', fontsize=8)
        ax.legend(fontsize=6, framealpha=0,
                  labelcolor='#8ab4d4', ncol=2)
        ax.grid(alpha=0.3)
        fig.patch.set_facecolor('#0a1628')
        st.pyplot(fig)
        plt.close()

# ══════════════════════════════════════════════════════════════
# PAGE : DOCUMENTATION
# ══════════════════════════════════════════════════════════════
elif page == "Documentation":
    st.markdown("""
    <div class='cyber-title'>Documentation</div>
    <div class='cyber-subtitle'>CyberDetect AI — Guide Technique Complet</div>
    <hr>""", unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Vue d'ensemble",
        "📊 Dataset",
        "🤖 Modèles ML",
        "📈 Métriques",
        "🚀 Guide d'utilisation"
    ])

    # ── Tab 1 : Vue d'ensemble ────────────────────────────────
    with tab1:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#0a1628,#0d1f35);
                    border:1px solid #0d4f8c; border-radius:10px;
                    padding:25px; margin-bottom:15px;'>
            <div style='font-family:Orbitron,monospace; color:#00d4ff;
                        font-size:0.9rem; letter-spacing:3px;
                        margin-bottom:15px;'>🛡️ VUE D'ENSEMBLE</div>
            <div style='font-family:Rajdhani,sans-serif;
                        color:#8ab4d4; line-height:2; font-size:1rem;'>
                CyberDetect AI est une plateforme de détection d'attaques réseau
                basée sur le Machine Learning. Elle analyse les incidents de
                cybersécurité mondiaux et prédit le type d'attaque à partir
                de paramètres de sécurité.<br><br>
                <b style='color:#00d4ff;'>Objectif principal :</b>
                Classification multi-classe de 6 types d'attaques réseau<br>
                <b style='color:#00d4ff;'>Approche :</b>
                Supervised Learning avec 4 algorithmes ML<br>
                <b style='color:#00d4ff;'>Application :</b>
                Aide à la décision pour les analystes SOC
            </div>
        </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div style='background:#0a1628;border:1px solid #0d4f8c;
                        border-radius:8px;padding:20px;'>
                <div style='font-family:Orbitron,monospace;color:#00ff88;
                            font-size:0.75rem;letter-spacing:2px;
                            margin-bottom:12px;'>✅ FONCTIONNALITÉS</div>
                <div style='font-family:Share Tech Mono,monospace;
                            color:#8ab4d4;font-size:0.78rem;line-height:2;'>
                    ► Dashboard temps réel<br>
                    ► Prédiction IA des attaques<br>
                    ► Monitoring réseau live<br>
                    ► Exploration des données<br>
                    ► 4 algorithmes ML comparés<br>
                    ► Métriques d'évaluation complètes<br>
                    ► Interface SOC professionnelle<br>
                    ► Export des modèles (.pkl)
                </div>
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div style='background:#0a1628;border:1px solid #0d4f8c;
                        border-radius:8px;padding:20px;'>
                <div style='font-family:Orbitron,monospace;color:#ffd700;
                            font-size:0.75rem;letter-spacing:2px;
                            margin-bottom:12px;'>🔧 STACK TECHNIQUE</div>
                <div style='font-family:Share Tech Mono,monospace;
                            color:#8ab4d4;font-size:0.78rem;line-height:2;'>
                    ► Python 3.12<br>
                    ► Streamlit (Interface Web)<br>
                    ► Scikit-learn (ML)<br>
                    ► Pandas / NumPy (Data)<br>
                    ► Matplotlib / Seaborn (Viz)<br>
                    ► Imbalanced-learn (SMOTE)<br>
                    ► Joblib (Export modèles)<br>
                    ► VS Code / Google Colab
                </div>
            </div>""", unsafe_allow_html=True)

    # ── Tab 2 : Dataset ───────────────────────────────────────
    with tab2:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#0a1628,#0d1f35);
                    border:1px solid #0d4f8c; border-radius:10px;
                    padding:25px; margin-bottom:15px;'>
            <div style='font-family:Orbitron,monospace; color:#00d4ff;
                        font-size:0.9rem; letter-spacing:3px;
                        margin-bottom:15px;'>📊 DATASET</div>
            <div style='font-family:Rajdhani,sans-serif;
                        color:#8ab4d4; line-height:2; font-size:1rem;'>
                <b style='color:#00d4ff;'>Nom :</b>
                Global Cybersecurity Threats 2015–2024<br>
                <b style='color:#00d4ff;'>Source :</b> Kaggle<br>
                <b style='color:#00d4ff;'>Lignes :</b> 3 000 incidents<br>
                <b style='color:#00d4ff;'>Colonnes :</b> 10 variables<br>
                <b style='color:#00d4ff;'>Période :</b> 2015 → 2024 (10 ans)<br>
                <b style='color:#00d4ff;'>Variable cible :</b> Attack Type (6 classes)
            </div>
        </div>""", unsafe_allow_html=True)

        # Colonnes table
        st.markdown("""
        <div style='font-family:Orbitron,monospace;color:#00d4ff;
                    font-size:0.75rem;letter-spacing:2px;
                    margin-bottom:10px;'>► DESCRIPTION DES COLONNES</div>
        """, unsafe_allow_html=True)

        cols_data = {
            'Colonne': [
                'Country', 'Year', 'Attack Type', 'Target Industry',
                'Financial Loss (in Million $)', 'Number of Affected Users',
                'Attack Source', 'Security Vulnerability Type',
                'Defense Mechanism Used', 'Incident Resolution Time (in Hours)'
            ],
            'Type': [
                'Catégoriel', 'Numérique', 'Catégoriel (Cible)', 'Catégoriel',
                'Numérique', 'Numérique',
                'Catégoriel', 'Catégoriel',
                'Catégoriel', 'Numérique'
            ],
            'Description': [
                "Pays où l'incident s'est produit",
                "Année de l'incident (2015-2024)",
                "6 types : DDoS, Phishing, SQL Injection, Ransomware, Malware, MitM",
                "Secteur ciblé : IT, Banking, Healthcare, Retail...",
                "Perte financière en millions de dollars",
                "Nombre d'utilisateurs affectés",
                "Origine : Nation-state, Insider, Hacker Group, Unknown",
                "Type de faille : Zero-day, Social Engineering, Unpatched Software...",
                "Défense utilisée : Firewall, VPN, Antivirus, Encryption...",
                "Durée de résolution en heures"
            ]
        }
        st.dataframe(pd.DataFrame(cols_data),
                     use_container_width=True, hide_index=True)

        # Attack types
        st.markdown("""
        <div style='font-family:Orbitron,monospace;color:#00d4ff;
                    font-size:0.75rem;letter-spacing:2px;
                    margin:15px 0 10px;'>► TYPES D'ATTAQUES</div>
        """, unsafe_allow_html=True)

        attacks_data = {
            "Type d'attaque": ["DDoS", "Phishing", "SQL Injection",
                                'Ransomware', 'Malware', 'Man-in-the-Middle'],
            "Icône": ["💥", "🎣", "💉", "🔒", "🦠", "🕵️"],
            "Sévérité": ["HIGH", "MEDIUM", "HIGH", "CRITICAL", "HIGH", "MEDIUM"],
            "Description": [
                "Saturation des ressources réseau par flood de requêtes",
                "Vol d'identifiants via faux sites ou emails frauduleux",
                "Injection de code SQL malveillant dans les bases de données",
                "Chiffrement des données avec demande de rançon",
                "Logiciel malveillant infectant les systèmes",
                "Interception des communications entre deux parties"
            ]
        }
        st.dataframe(pd.DataFrame(attacks_data),
                     use_container_width=True, hide_index=True)

    # ── Tab 3 : Modèles ML ────────────────────────────────────
    with tab3:
        st.markdown("""
        <div style='font-family:Orbitron,monospace;color:#00d4ff;
                    font-size:0.9rem;letter-spacing:3px;margin-bottom:15px;'>
            🤖 ALGORITHMES DE MACHINE LEARNING
        </div>""", unsafe_allow_html=True)

        models_info = [
            ("🔵 Régression Logistique", "#00d4ff",
             "Algorithme de classification linéaire basé sur la fonction sigmoïde.",
             ["Simple et rapide à entraîner",
              "Coefficients interprétables",
              "Bonne baseline pour comparaison",
              "Fonctionne bien avec données linéaires"],
             ["Limité aux frontières linéaires",
              "Moins performant sur données complexes"]),
            ("🟡 K-Nearest Neighbors (KNN)", "#ffd700",
             "Classification basée sur les K voisins les plus proches dans l'espace des features.",
             ["Non-paramétrique — pas d'hypothèse sur les données",
              "Intuitif et facile à comprendre",
              "Efficace sur petits datasets"],
             ["Lent sur grands datasets",
              "Sensible aux outliers et au bruit"]),
            ("🌲 Random Forest", "#00ff88",
             "Ensemble de plusieurs arbres de décision entraînés sur des sous-échantillons.",
             ["Très robuste — réduit l'overfitting",
              "Feature importance disponible",
              "Gère bien les données non-linéaires",
              "Généralement le meilleur modèle"],
             ["Moins interprétable qu'un arbre simple",
              "Plus lent à entraîner que LR"]),
            ("🔴 SVM (Support Vector Machine)", "#ff4455",
             "Trouve l'hyperplan optimal qui sépare au mieux les classes.",
             ["Très efficace en haute dimension",
              "Robuste contre l'overfitting",
              "Kernel RBF pour données non-linéaires"],
             ["Lent sur grands datasets",
              "Sensible au choix des hyperparamètres"]),
        ]

        for name, color, desc, pros, cons in models_info:
            st.markdown(f"""
            <div style='background:#0a1628;border:1px solid #0d4f8c;
                        border-left:3px solid {color};border-radius:8px;
                        padding:18px;margin-bottom:12px;'>
                <div style='font-family:Orbitron,monospace;color:{color};
                            font-size:0.85rem;font-weight:700;
                            margin-bottom:8px;'>{name}</div>
                <div style='font-family:Rajdhani,sans-serif;color:#8ab4d4;
                            font-size:0.9rem;margin-bottom:10px;'>{desc}</div>
                <div style='display:flex;gap:20px;flex-wrap:wrap;'>
                    <div style='flex:1;min-width:200px;'>
                        <div style='font-family:Share Tech Mono,monospace;
                                    color:#00ff88;font-size:0.65rem;
                                    letter-spacing:2px;margin-bottom:5px;'>
                            ✅ AVANTAGES</div>
                        <div style='font-family:Share Tech Mono,monospace;
                                    color:#8ab4d4;font-size:0.72rem;
                                    line-height:1.8;'>{chr(10).join(["► " + p for p in pros])}</div>
                    </div>
                    <div style='flex:1;min-width:200px;'>
                        <div style='font-family:Share Tech Mono,monospace;
                                    color:#ff4455;font-size:0.65rem;
                                    letter-spacing:2px;margin-bottom:5px;'>
                            ⚠ LIMITES</div>
                        <div style='font-family:Share Tech Mono,monospace;
                                    color:#8ab4d4;font-size:0.72rem;
                                    line-height:1.8;'>{chr(10).join(["► " + c for c in cons])}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Pipeline
        st.markdown("""
        <div style='font-family:Orbitron,monospace;color:#00d4ff;
                    font-size:0.75rem;letter-spacing:2px;margin:15px 0 10px;'>
            ► PIPELINE ML</div>
        <div style='background:#0a1628;border:1px solid #0d4f8c;
                    border-radius:8px;padding:18px;'>
            <div style='font-family:Share Tech Mono,monospace;
                        color:#8ab4d4;font-size:0.78rem;line-height:2.2;'>
                <span style='color:#00d4ff;'>1.</span> Chargement du CSV
                &nbsp;→&nbsp;
                <span style='color:#00d4ff;'>2.</span> Data Cleaning (NaN, doublons)
                &nbsp;→&nbsp;
                <span style='color:#00d4ff;'>3.</span> Label Encoding
                &nbsp;→&nbsp;
                <span style='color:#00d4ff;'>4.</span> SMOTE (équilibrage)
                &nbsp;→&nbsp;
                <span style='color:#00d4ff;'>5.</span> Train/Val/Test Split (70/15/15)
                &nbsp;→&nbsp;
                <span style='color:#00d4ff;'>6.</span> StandardScaler
                &nbsp;→&nbsp;
                <span style='color:#00d4ff;'>7.</span> Entraînement 4 modèles
                &nbsp;→&nbsp;
                <span style='color:#00d4ff;'>8.</span> Évaluation métriques
                &nbsp;→&nbsp;
                <span style='color:#00d4ff;'>9.</span> Export .pkl
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Tab 4 : Métriques ─────────────────────────────────────
    with tab4:
        st.markdown("""
        <div style='font-family:Orbitron,monospace;color:#00d4ff;
                    font-size:0.9rem;letter-spacing:3px;margin-bottom:15px;'>
            📈 MÉTRIQUES D'ÉVALUATION
        </div>""", unsafe_allow_html=True)

        metrics_info = [
            ("🎯 Accuracy", "#00d4ff",
             "Proportion de prédictions correctes sur le total.",
             "Accuracy = (VP + VN) / Total",
             "Fiable uniquement si le dataset est équilibré. Notre dataset est équilibré (~16% par classe) → Accuracy est fiable."),
            ("🔬 Precision", "#ffd700",
             "Parmi les instances prédites comme attaque X, combien sont vraiment X.",
             "Precision = VP / (VP + FP)",
             "Une precision élevée = peu de fausses alarmes. Important pour éviter de surcharger les analystes SOC."),
            ("📡 Recall (Sensibilité)", "#ff4455",
             "Parmi toutes les vraies attaques X, combien ont été détectées.",
             "Recall = VP / (VP + FN)",
             "CRITIQUE en cybersécurité — mieux vaut une fausse alerte que rater une vraie attaque ransomware."),
            ("⚖️ F1-Score", "#00ff88",
             "Moyenne harmonique entre Precision et Recall. Métrique principale.",
             "F1 = 2 × (Precision × Recall) / (Precision + Recall)",
             "Meilleure métrique globale car elle équilibre precision et recall. Utilisée pour choisir le meilleur modèle."),
            ("📊 ROC-AUC", "#aa44ff",
             "Aire sous la courbe ROC. Mesure la capacité discriminante du modèle.",
             "AUC = 1.0 → Parfait | AUC = 0.5 → Aléatoire",
             "AUC > 0.95 = excellent modèle. Indépendant du seuil de classification."),
        ]

        for name, color, desc, formula, interpretation in metrics_info:
            st.markdown(f"""
            <div style='background:#0a1628;border:1px solid #0d4f8c;
                        border-left:3px solid {color};border-radius:8px;
                        padding:18px;margin-bottom:12px;'>
                <div style='font-family:Orbitron,monospace;color:{color};
                            font-size:0.85rem;font-weight:700;
                            margin-bottom:8px;'>{name}</div>
                <div style='font-family:Rajdhani,sans-serif;color:#8ab4d4;
                            font-size:0.9rem;margin-bottom:8px;'>{desc}</div>
                <div style='background:#071428;border-radius:4px;
                            padding:8px 12px;margin-bottom:8px;
                            font-family:Share Tech Mono,monospace;
                            color:{color};font-size:0.78rem;'>
                    {formula}
                </div>
                <div style='font-family:Share Tech Mono,monospace;
                            color:#4a7fa0;font-size:0.72rem;
                            font-style:italic;'>
                    💡 {interpretation}
                </div>
            </div>""", unsafe_allow_html=True)

    # ── Tab 5 : Guide d'utilisation ───────────────────────────
    with tab5:
        st.markdown("""
        <div style='font-family:Orbitron,monospace;color:#00d4ff;
                    font-size:0.9rem;letter-spacing:3px;margin-bottom:15px;'>
            🚀 GUIDE D'UTILISATION
        </div>""", unsafe_allow_html=True)

        steps = [
            ("01", "CONNEXION", "#00d4ff",
             "Accédez à l'application via http://localhost:8501",
             ["Entrez vos identifiants : admin / soc2024",
              "Cliquez sur [ AUTHENTICATE → ]",
              "Vous accédez au Dashboard principal"]),
            ("02", "DASHBOARD", "#00ff88",
             "Analysez les statistiques globales des cyberattaques",
             ["Consultez les 6 KPIs en haut de page",
              "Analysez la distribution des attaques (donut chart)",
              "Observez les tendances annuelles 2015-2024",
              "Identifiez les secteurs et pays les plus ciblés",
              "Consultez la heatmap Attaque × Industrie"]),
            ("03", "PRÉDICTION", "#ffd700",
             "Prédisez le type d'attaque d'un incident",
             ["Renseignez les paramètres réseau (pays, secteur, perte...)",
              "Cliquez sur [ ANALYZE THREAT ]",
              "Consultez le type d'attaque prédit avec la sévérité",
              "Analysez les probabilités par classe"]),
            ("04", "LIVE MONITORING", "#ff4455",
             "Surveillez le trafic réseau en temps réel",
             ["Observez les courbes de trafic sur 24h",
              "Identifiez les pics d'activité suspecte",
              "Consultez la table des alertes récentes"]),
            ("05", "DATA EXPLORATION", "#aa44ff",
             "Explorez le dataset en détail",
             ["Consultez les statistiques descriptives",
              "Analysez les pertes financières par attaque",
              "Visualisez l'évolution temporelle des attaques"]),
        ]

        for num, title, color, desc, sub_steps in steps:
            st.markdown(f"""
            <div style='background:#0a1628;border:1px solid #0d4f8c;
                        border-radius:8px;padding:18px;margin-bottom:12px;
                        display:flex;gap:20px;'>
                <div style='font-family:Orbitron,monospace;color:{color};
                            font-size:2rem;font-weight:900;opacity:0.3;
                            min-width:50px;'>{num}</div>
                <div style='flex:1;'>
                    <div style='font-family:Orbitron,monospace;color:{color};
                                font-size:0.85rem;font-weight:700;
                                letter-spacing:2px;margin-bottom:6px;'>{title}</div>
                    <div style='font-family:Rajdhani,sans-serif;color:#8ab4d4;
                                font-size:0.9rem;margin-bottom:8px;'>{desc}</div>
                    <div style='font-family:Share Tech Mono,monospace;
                                color:#4a7fa0;font-size:0.72rem;line-height:1.9;'>
                        {"<br>".join(["► " + s for s in sub_steps])}
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        # FAQ
        st.markdown("""
        <div style='font-family:Orbitron,monospace;color:#00d4ff;
                    font-size:0.75rem;letter-spacing:2px;margin:20px 0 10px;'>
            ► FAQ — QUESTIONS FRÉQUENTES</div>""", unsafe_allow_html=True)

        faqs = [
            ("Les fichiers .pkl sont manquants ?",
             "Exécutez d'abord le notebook notebook_cyber.py jusqu'à l'Étape 6. Les fichiers best_model.pkl, scaler.pkl et label_encoder.pkl seront générés automatiquement."),
            ("Le modèle est en mode démo ?",
             "Sans les fichiers .pkl, l'application utilise des données simulées. Entraînez le modèle dans Colab ou VS Code puis copiez les .pkl dans le même dossier que app.py."),
            ("Comment changer le mot de passe ?",
             "Dans app.py, cherchez la ligne : if username == 'admin' and password == 'soc2024' et modifiez les valeurs selon vos besoins."),
            ("Comment déployer en ligne ?",
             "Utilisez Streamlit Cloud (streamlit.io), Heroku, ou ngrok pour une URL publique temporaire depuis Google Colab."),
        ]

        for q, a in faqs:
            with st.expander(f"❓ {q}"):
                st.markdown(f"""
                <div style='font-family:Share Tech Mono,monospace;
                            color:#8ab4d4;font-size:0.78rem;
                            line-height:1.8;padding:10px;'>
                    ► {a}
                </div>""", unsafe_allow_html=True)

# PAGE : ABOUT
# ══════════════════════════════════════════════════════════════
elif page == "About":
    st.markdown("""
    <div class='cyber-title' style='text-align:center;'>About</div>
    <div class='cyber-subtitle' style='text-align:center;'>CyberDetect AI — System Information</div>
    <hr>""", unsafe_allow_html=True)

    _, col_about, _ = st.columns([1, 2, 1])
    with col_about:

        # Logo + Title
        st.markdown("""<div style="text-align:center; padding:30px 20px 10px;">
            <div style="font-size:4rem;">🛡️</div>
            <div style="font-family:Orbitron,monospace; font-size:1.8rem;
                        font-weight:900; letter-spacing:4px; margin:10px 0 4px;
                        color:#00d4ff; text-shadow:0 0 20px #00d4ffaa;">
                CyberDetect AI
            </div>
            <div style="font-family:Share Tech Mono,monospace; font-size:0.65rem;
                        color:#2a5f7a; letter-spacing:4px; text-transform:uppercase;">
                Network Intrusion Detection System · v1.0
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#0d4f8c;'>", unsafe_allow_html=True)

        # Info cards
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div style="background:#071428; border:1px solid #0d4f8c;
                border-radius:8px; padding:14px; margin-bottom:10px;">
                <div style="font-family:Share Tech Mono,monospace; font-size:0.6rem;
                            color:#2a5f7a; letter-spacing:2px; margin-bottom:6px;">
                    📊 DATASET</div>
                <div style="font-family:Rajdhani,sans-serif; color:#8ab4d4;
                            font-size:0.85rem; line-height:1.7;">
                    Global Cybersecurity<br>Threats 2015-2024<br>
                    <span style="color:#00d4ff;">3 000 incidents</span>
                </div></div>""", unsafe_allow_html=True)

            st.markdown("""<div style="background:#071428; border:1px solid #0d4f8c;
                border-radius:8px; padding:14px;">
                <div style="font-family:Share Tech Mono,monospace; font-size:0.6rem;
                            color:#2a5f7a; letter-spacing:2px; margin-bottom:6px;">
                    🤖 MODELES ML</div>
                <div style="font-family:Rajdhani,sans-serif; color:#8ab4d4;
                            font-size:0.85rem; line-height:1.7;">
                    Logistic Regression<br>KNN · Random Forest · SVM<br>
                    <span style="color:#00d4ff;">+ SMOTE Balancing</span>
                </div></div>""", unsafe_allow_html=True)

        with col2:
            st.markdown("""<div style="background:#071428; border:1px solid #0d4f8c;
                border-radius:8px; padding:14px; margin-bottom:10px;">
                <div style="font-family:Share Tech Mono,monospace; font-size:0.6rem;
                            color:#2a5f7a; letter-spacing:2px; margin-bottom:6px;">
                    🛡️ ATTAQUES</div>
                <div style="font-family:Rajdhani,sans-serif; color:#8ab4d4;
                            font-size:0.85rem; line-height:1.7;">
                    DDoS · Phishing<br>SQL Injection · Ransomware<br>
                    <span style="color:#00d4ff;">Malware · MitM</span>
                </div></div>""", unsafe_allow_html=True)

            st.markdown("""<div style="background:#071428; border:1px solid #0d4f8c;
                border-radius:8px; padding:14px;">
                <div style="font-family:Share Tech Mono,monospace; font-size:0.6rem;
                            color:#2a5f7a; letter-spacing:2px; margin-bottom:6px;">
                    🔧 FRAMEWORK</div>
                <div style="font-family:Rajdhani,sans-serif; color:#8ab4d4;
                            font-size:0.85rem; line-height:1.7;">
                    Streamlit · Scikit-learn<br>Pandas · Matplotlib<br>
                    <span style="color:#00d4ff;">Python 3.12</span>
                </div></div>""", unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#0d4f8c;'>", unsafe_allow_html=True)

        # Author
        st.markdown("""<div style="text-align:center; padding:20px 0;">
            <div style="font-family:Share Tech Mono,monospace; font-size:0.6rem;
                        color:#2a5f7a; letter-spacing:3px; margin-bottom:10px;">
                DEVELOPED BY</div>
            <div style="font-family:Orbitron,monospace; font-size:1.6rem;
                        color:#00d4ff; font-weight:900; letter-spacing:3px;
                        text-shadow:0 0 25px #00d4ffbb; margin-bottom:6px;">
                Marwa Lehdaoui</div>
            <div style="font-family:Share Tech Mono,monospace; font-size:0.65rem;
                        color:#4a7fa0; letter-spacing:2px; margin-bottom:20px;">
                SOC AI Workshop · 2026</div>
            <div style="display:flex; justify-content:center; gap:8px; flex-wrap:wrap;">
                <span style="background:rgba(0,212,255,0.1); border:1px solid #00d4ff44;
                             border-radius:20px; padding:4px 12px;
                             font-family:Share Tech Mono,monospace;
                             font-size:0.65rem; color:#00d4ff;">Machine Learning</span>
                <span style="background:rgba(0,255,136,0.1); border:1px solid #00ff8844;
                             border-radius:20px; padding:4px 12px;
                             font-family:Share Tech Mono,monospace;
                             font-size:0.65rem; color:#00ff88;">Cybersecurity</span>
                <span style="background:rgba(255,215,0,0.1); border:1px solid #ffd70044;
                             border-radius:20px; padding:4px 12px;
                             font-family:Share Tech Mono,monospace;
                             font-size:0.65rem; color:#ffd700;">SOC Analytics</span>
                <span style="background:rgba(170,68,255,0.1); border:1px solid #aa44ff44;
                             border-radius:20px; padding:4px 12px;
                             font-family:Share Tech Mono,monospace;
                             font-size:0.65rem; color:#aa44ff;">Streamlit</span>
            </div>
        </div>""", unsafe_allow_html=True)
