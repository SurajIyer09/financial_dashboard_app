import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

st.title("📄 Generate Financial PDF Report")

if "data" not in st.session_state:
    st.warning("Upload dataset first.")
else:
    df = st.session_state["data"]

    total_revenue = df.select_dtypes(include="number").sum().iloc[0]

    if st.button("Generate PDF Report"):
        file_path = "financial_report.pdf"
        doc = SimpleDocTemplate(file_path)
        elements = []

        elements.append(Paragraph("Financial Report Summary", 
                                  ParagraphStyle(name="Title", fontSize=18)))
        elements.append(Spacer(1, 0.5 * inch))

        elements.append(Paragraph(f"Total Revenue: {total_revenue}", 
                                  ParagraphStyle(name="Normal", fontSize=12)))

        doc.build(elements)

        with open(file_path, "rb") as f:
            st.download_button("Download Report", f, file_name="Financial_Report.pdf")
