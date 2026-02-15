import streamlit as st
import pandas as pd

st.title("🤖 AI Financial Insights")

if "data" not in st.session_state:
    st.warning("Upload data first.")
else:
    df = st.session_state["data"]

    numeric_cols = df.select_dtypes(include="number").columns

    revenue = st.selectbox("Revenue Column", numeric_cols)
    expense = st.selectbox("Expense Column", numeric_cols)

    total_revenue = df[revenue].sum()
    total_expense = df[expense].sum()
    profit = total_revenue - total_expense
    margin = (profit / total_revenue) * 100 if total_revenue else 0

    st.subheader("Executive Summary")

    if margin > 20:
        st.success("Company is highly profitable with strong margins.")
    elif margin > 10:
        st.info("Company is moderately profitable but has room for improvement.")
    else:
        st.error("Profit margins are low. Cost optimization recommended.")

    if total_expense > total_revenue * 0.8:
        st.warning("Expenses are consuming majority of revenue.")

    st.write(f"""
    Total Revenue: ₹ {total_revenue:,.0f}  
    Total Expense: ₹ {total_expense:,.0f}  
    Net Profit: ₹ {profit:,.0f}  
    Profit Margin: {margin:.2f} %
    """)
