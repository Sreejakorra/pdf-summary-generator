import streamlit as st
import pdfplumber
from transformers import pipeline

st.title("📄 PDF Summary Generator")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    if full_text.strip() == "":
        st.warning("⚠️ No extractable text found in this PDF.")
    else:
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        input_text = full_text[:1000]  # first 1000 chars (adjust if needed)
        summary = summarizer(input_text, max_length=130, min_length=50, do_sample=False)[0]['summary_text']
        st.subheader("Summary:")
        st.write(summary)
