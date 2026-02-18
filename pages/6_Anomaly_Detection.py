import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("🚨 Revenue Anomaly Detection")

if "data" not in st.session_state:
    st.warning("Upload dataset first.")
else:
    df = st.session_state["data"]

    numeric_cols = df.select_dtypes(include="number").columns
    revenue_col = st.selectbox("Revenue Column", numeric_cols)

    mean = df[revenue_col].mean()
    std = df[revenue_col].std()

    df["Anomaly"] = np.where(
        abs(df[revenue_col] - mean) > 2 * std,
        "Anomaly",
        "Normal"
    )

    fig = px.scatter(df, y=revenue_col, color="Anomaly",
                     title="Revenue Anomaly Detection")
    st.plotly_chart(fig, use_container_width=True)

    anomalies = df[df["Anomaly"] == "Anomaly"]
    st.subheader("Detected Anomalies")
    st.dataframe(anomalies)
