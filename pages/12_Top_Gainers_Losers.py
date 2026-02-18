import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📊 NSE Top Gainers & Losers")

stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS",
          "HDFCBANK.NS", "SBIN.NS", "ITC.NS"]

results = []

for stock in stocks:
    data = yf.Ticker(stock).history(period="5d")
    if not data.empty:
        change = ((data["Close"].iloc[-1] - data["Close"].iloc[0]) /
                  data["Close"].iloc[0]) * 100
        results.append([stock.replace(".NS",""), round(change,2)])

df = pd.DataFrame(results, columns=["Stock", "5-Day % Change"])

gainers = df.sort_values("5-Day % Change", ascending=False).head(3)
losers = df.sort_values("5-Day % Change").head(3)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚀 Top Gainers")
    st.dataframe(gainers)

with col2:
    st.subheader("📉 Top Losers")
    st.dataframe(losers)
