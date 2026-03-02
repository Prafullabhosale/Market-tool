import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Personal Market Guide", layout="centered")

st.title("📈 Personal Market Guide")

def get_trend(symbol):
    data = yf.download(symbol, period="3mo", interval="1d")
    data["EMA50"] = data["Close"].ewm(span=50).mean()
    latest = data.iloc[-1]

    if latest["Close"] > latest["EMA50"]:
        trend = "Bullish"
        action = "Buy on dips"
    else:
        trend = "Bearish"
        action = "Avoid longs"

    return trend, round(latest["Close"], 2)

nifty_trend, nifty_price = get_trend("^NSEI")
bank_trend, bank_price = get_trend("^NSEBANK")

st.subheader("📊 Index Trends")
st.metric("Nifty", nifty_trend, nifty_price)
st.metric("Bank Nifty", bank_trend, bank_price)

if nifty_trend == "Bullish":
    st.success("Market Bias: Buy on dips")
else:
    st.warning("Market Bias: Trade cautiously")

st.info("⚠️ Educational purpose only")
