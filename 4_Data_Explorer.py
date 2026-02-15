import streamlit as st
import pandas as pd

st.title("🔍 Data Explorer")

if "data" not in st.session_state:
    st.warning("Please upload data in Dashboard page first.")
else:
    df = st.session_state["data"]

    st.subheader("Dataset Overview")

    st.write("Shape:", df.shape)
    st.write("Columns:", df.columns.tolist())

    st.subheader("Statistical Summary")
    st.dataframe(df.describe())

    st.subheader("Full Dataset")
    st.dataframe(df)
