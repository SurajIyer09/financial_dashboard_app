import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("📈 Advanced Financial Ratios")

if "data" not in st.session_state:
    st.warning("Upload data in Dashboard page first.")
else:
    df = st.session_state["data"]

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    revenue = st.selectbox("Revenue", numeric_cols)
    expense = st.selectbox("Expense", numeric_cols)
    assets = st.selectbox("Assets", numeric_cols)
    equity = st.selectbox("Equity", numeric_cols)
    debt = st.selectbox("Debt", numeric_cols)
    current_assets = st.selectbox("Current Assets", numeric_cols)
    current_liabilities = st.selectbox("Current Liabilities", numeric_cols)

    df["Net Income"] = df[revenue] - df[expense]

    total_rev = df[revenue].sum()
    net_income = df["Net Income"].sum()
    total_assets = df[assets].sum()
    total_equity = df[equity].sum()
    total_debt = df[debt].sum()

    roa = (net_income / total_assets) * 100 if total_assets else 0
    roe = (net_income / total_equity) * 100 if total_equity else 0
    debt_ratio = (total_debt / total_assets) * 100 if total_assets else 0
    ebitda_margin = (net_income / total_rev) * 100 if total_rev else 0
    current_ratio = (df[current_assets].sum() / df[current_liabilities].sum())

    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    col1.metric("ROA (%)", f"{roa:.2f}")
    col2.metric("ROE (%)", f"{roe:.2f}")
    col3.metric("Debt Ratio (%)", f"{debt_ratio:.2f}")
    col4.metric("EBITDA Margin (%)", f"{ebitda_margin:.2f}")
    col5.metric("Current Ratio", f"{current_ratio:.2f}")

    st.markdown("""
### Interpretation:

• ROA > 5% → Efficient asset usage  
• ROE > 15% → Strong shareholder returns  
• Current Ratio > 1.5 → Good liquidity  
• Low Debt Ratio → Lower financial risk  
""")
