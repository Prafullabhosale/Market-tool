import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Personal Market Guide", layout="centered")
st.title("📈 Personal Market Guide")

def get_trend(symbol):
    data = yf.download(symbol, period="3mo", interval="1d")

    # If no data
    if data.empty:
        return "No Data", "N/A"

    data["EMA50"] = data["Close"].ewm(span=50).mean()
    latest = data.iloc[-1]

    try:
        close_price = float(latest["Close"])
        ema50 = float(latest["EMA50"])
    except:
        return "Data Error", "N/A"

    if close_price > ema50:
        trend = "Bullish"
    else:
        trend = "Bearish"

    return trend, round(close_price, 2)

# Fetch trends
nifty_trend, nifty_price = get_trend("^NSEI")
bank_trend, bank_price = get_trend("^NSEBANK")

st.subheader("📊 Index Trends")
st.metric("Nifty", nifty_trend, nifty_price)
st.metric("Bank Nifty", bank_trend, bank_price)

if nifty_trend == "Bullish":
    st.success("Market Bias: Buy on dips")
elif nifty_trend == "Bearish":
    st.warning("Market Bias: Trade cautiously")
else:
    st.info("Market data unavailable")

st.info("⚠️ Educational purpose only")
