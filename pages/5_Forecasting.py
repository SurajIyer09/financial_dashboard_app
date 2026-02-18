import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px

st.title("📈 Revenue Forecasting (ML)")

if "data" not in st.session_state:
    st.warning("Upload dataset in Dashboard first.")
else:
    df = st.session_state["data"]

    numeric_cols = df.select_dtypes(include="number").columns
    date_col = st.selectbox("Select Date Column", df.columns)
    revenue_col = st.selectbox("Select Revenue Column", numeric_cols)

    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    df["Month_Index"] = range(len(df))

    X = df[["Month_Index"]]
    y = df[revenue_col]

    model = LinearRegression()
    model.fit(X, y)

    future_months = 6
    future_index = np.arange(len(df), len(df) + future_months).reshape(-1, 1)
    predictions = model.predict(future_index)

    future_dates = pd.date_range(
        start=df[date_col].iloc[-1],
        periods=future_months + 1,
        freq="M"
    )[1:]

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted Revenue": predictions
    })

    fig = px.line(df, x=date_col, y=revenue_col, title="Historical Revenue")
    fig.add_scatter(x=forecast_df["Date"], y=forecast_df["Predicted Revenue"],
                    mode="lines+markers", name="Forecast")

    st.plotly_chart(fig, use_container_width=True)
