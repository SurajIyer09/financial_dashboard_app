import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.title("🔥 NSE Sector Heatmap")

sector_stocks = {
    "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS"],
    "IT": ["TCS.NS", "INFY.NS", "WIPRO.NS"],
    "Energy": ["RELIANCE.NS", "ONGC.NS"]
}

heatmap_data = []

for sector, stocks in sector_stocks.items():
    for stock in stocks:
        try:
            data = yf.download(stock, period="1mo", progress=False)

            if not data.empty and "Close" in data.columns:
                start_price = float(data["Close"].iloc[0])
                end_price = float(data["Close"].iloc[-1])

                change = ((end_price - start_price) / start_price) * 100

                heatmap_data.append({
                    "Sector": str(sector),
                    "Stock": str(stock.replace(".NS", "")),
                    "Change": float(round(change, 2))
                })

        except Exception:
            pass

if len(heatmap_data) == 0:
    st.warning("No market data available.")
else:
    df = pd.DataFrame(heatmap_data)

    # Ensure proper data types
    df["Sector"] = df["Sector"].astype(str)
    df["Stock"] = df["Stock"].astype(str)
    df["Change"] = pd.to_numeric(df["Change"], errors="coerce")

    # Treemap needs positive values for size
    df["Size"] = df["Change"].abs()

    fig = px.treemap(
        df,
        path=["Sector", "Stock"],
        values="Size",
        color="Change",
        color_continuous_scale="RdYlGn",
        title="1-Month NSE Sector Performance"
    )

    st.plotly_chart(fig, use_container_width=True)
