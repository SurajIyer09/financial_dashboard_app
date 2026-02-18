import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🇮🇳 Indian Market Terminal")

ticker_input = st.text_input("Enter NSE Stock", "TCS")
ticker = ticker_input.upper() + ".NS"

stock = yf.Ticker(ticker)
data = stock.history(period="1y")

if not data.empty:

    # Moving averages
    data["MA50"] = data["Close"].rolling(50).mean()
    data["MA200"] = data["Close"].rolling(200).mean()

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="Price"
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["MA50"],
        name="MA 50"
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["MA200"],
        name="MA 200"
    ))

    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Invalid Ticker")
