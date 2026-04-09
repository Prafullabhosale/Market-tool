import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Trading Assistant", layout="wide")

st.title("📈 Smart Trading Assistant")

# -------------------------------
# INPUT
# -------------------------------
symbol = st.text_input("Enter Stock Symbol (Example: ^NSEI, RELIANCE.NS)", "^NSEI")

# -------------------------------
# FETCH DATA
# -------------------------------
@st.cache_data
def load_data(symbol):
    data = yf.download(symbol, period="6mo", interval="1d")
    return data

data = load_data(symbol)

if data.empty:
    st.error("No data found. Check symbol.")
    st.stop()

# -------------------------------
# EMA CALCULATIONS
# -------------------------------
price_col = "Close" if "Close" in data.columns else "Adj Close"

data["EMA20"] = data[price_col].ewm(span=20, adjust=False).mean()
data["EMA50"] = data[price_col].ewm(span=50, adjust=False).mean()
data["EMA200"] = data[price_col].ewm(span=200, adjust=False).mean()

latest = data.iloc[-1]
prev = data.iloc[-2]

ema20 = latest["EMA20"].item()
ema50 = latest["EMA50"].item()
ema200 = latest["EMA200"].item()

prev_ema20 = prev["EMA20"].item()
prev_ema50 = prev["EMA50"].item()
# -------------------------------
# TREND DETECTION
# -------------------------------
if ema20 > ema50 > ema200:
    trend = "🔥 Strong Bullish"
elif ema20 < ema50 < ema200:
    trend = "❄️ Strong Bearish"
else:
    trend = "⚖️ Sideways"

# -------------------------------
# SIGNAL DETECTION (CROSSOVER)
# -------------------------------
if prev_ema20 < prev_ema50 and ema20 > ema50:
    signal = "🟢 BUY Signal"
if prev_ema20 > prev_ema50 and ema20 < ema50:
    signal = "🔴 SELL Signal"
else:
    signal = "⏳ No Fresh Signal"

# -------------------------------
# STRENGTH
# -------------------------------
ema_gap = abs(ema20 - ema50)

if ema_gap > 50:
    strength = "💪 Strong"
elif ema_gap > 20:
    strength = "👍 Moderate"
else:
    strength = "⚠️ Weak"

# -------------------------------
# DISPLAY METRICS
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Price", round(latest[price_col], 2))
col2.metric("Trend", trend)
col3.metric("Signal", signal)
col4.metric("Strength", strength)

# -------------------------------
# CHART
# -------------------------------
fig = go.Figure()

fig.add_trace(go.Scatter(x=data.index, y=data[price_col], name="Price"))
fig.add_trace(go.Scatter(x=data.index, y=data["EMA20"], name="EMA20"))
fig.add_trace(go.Scatter(x=data.index, y=data["EMA50"], name="EMA50"))
fig.add_trace(go.Scatter(x=data.index, y=data["EMA200"], name="EMA200"))

fig.update_layout(title=f"{symbol} Price & EMAs", xaxis_title="Date", yaxis_title="Price")

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# DATA TABLE
# -------------------------------
with st.expander("📊 Show Data"):
    st.dataframe(data.tail(20))
