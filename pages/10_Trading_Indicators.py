import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.title("📈 Trading Indicators Engine")

ticker = st.text_input("Enter NSE Stock", "TCS") + ".NS"
data = yf.Ticker(ticker).history(period="6mo")

if not data.empty:

    # RSI
    delta = data["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    data["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = data["Close"].ewm(span=12).mean()
    ema26 = data["Close"].ewm(span=26).mean()
    data["MACD"] = ema12 - ema26

    st.subheader("RSI Indicator")

    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=data.index, y=data["RSI"]))
    fig_rsi.update_layout(template="plotly_dark")
    st.plotly_chart(fig_rsi)

    st.subheader("MACD Indicator")

    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=data.index, y=data["MACD"]))
    fig_macd.update_layout(template="plotly_dark")
    st.plotly_chart(fig_macd)

else:
    st.warning("Invalid ticker")
