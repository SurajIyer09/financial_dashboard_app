import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.title("📊 Live Stock Analysis")

ticker_input = st.text_input("Enter Indian Stock (Example: TCS, RELIANCE)", "TCS")

ticker = ticker_input.upper()
if not ticker.endswith(".NS"):
    ticker = ticker + ".NS"

stock = yf.Ticker(ticker)
data = stock.history(period="1y")

if not data.empty:

    currency = stock.info.get("currency", "INR")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Close Price"
        )
    )

    fig.update_layout(
        title=f"{ticker_input.upper()} Stock Price (1 Year)",
        xaxis_title="Date",
        yaxis_title=f"Price ({currency})",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write(f"Trading Currency: {currency}")

else:
    st.warning("Invalid ticker.")
