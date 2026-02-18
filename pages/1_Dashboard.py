import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Executive Performance Dashboard")

uploaded_file = st.file_uploader("Upload Financial Data", type=["csv", "xlsx"])

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.session_state["data"] = df

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    date_col = st.selectbox("Date Column", df.columns)
    revenue_col = st.selectbox("Revenue Column", numeric_cols)
    expense_col = st.selectbox("Expense Column", numeric_cols)

    df[date_col] = pd.to_datetime(df[date_col])
    df["Year"] = df[date_col].dt.year
    df["Month"] = df[date_col].dt.month
    df["Profit"] = df[revenue_col] - df[expense_col]

    # Monthly Aggregation
    monthly = df.groupby("Month")[[revenue_col, "Profit"]].sum().reset_index()

    # KPIs
    total_revenue = monthly[revenue_col].sum()
    total_profit = monthly["Profit"].sum()

    prev_revenue = monthly[revenue_col].iloc[-2] if len(monthly) > 1 else 0
    current_revenue = monthly[revenue_col].iloc[-1]

    growth = ((current_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue != 0 else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
    col2.metric("Total Profit", f"₹ {total_profit:,.0f}")
    col3.metric("Last Month Growth", f"{growth:.2f} %")

    # Charts
    fig1 = px.line(monthly, x="Month", y=revenue_col,
                   title="Revenue Trend", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(monthly, x="Month", y="Profit",
                   title="Profit Trend", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("Upload financial dataset to begin.")

