import streamlit as st
import openai
from PyPDF2 import PdfReader

st.set_page_config(page_title="📘 Smart PDF Analyzer", layout="centered")

st.title("📘 Smart PDF Summary Analyzer")
st.markdown("Upload any PDF and get a detailed, human-like summary in a report format. Ideal for office reports, articles, or presentations.")

# OpenAI API Key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_pdf):
    reader = PdfReader(uploaded_pdf)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    return full_text

# Function to generate a detailed summary
def generate_detailed_summary(text):
    prompt = f"""
You are a professional report writer. Read the following document and summarize it into a well-structured, detailed office-style report. Your summary should include:

1. 📘 Title (guess based on content)
2. 🧩 Overview (2-3 paragraphs)
3. 🧠 Key Sections (bullet points or short paragraphs)
4. 📊 Data/Insights (if any)
5. ✅ Conclusion and Recommendations

The tone should be professional, clear, and informative.

Document:
{text}
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1200
    )
    return response['choices'][0]['message']['content']

# Upload PDF
uploaded_pdf = st.file_uploader("📄 Upload your PDF file", type=["pdf"])

if uploaded_pdf:
    with st.spinner("🔍 Analyzing your PDF... Please wait."):
        pdf_text = extract_text_from_pdf(uploaded_pdf)

        if len(pdf_text.strip()) < 100:
            st.warning("The uploaded PDF seems to be empty or not readable. Please try another file.")
        else:
            if len(pdf_text) > 6000:
                pdf_text = pdf_text[:6000]  # Limit for GPT-3.5

            summary = generate_detailed_summary(pdf_text)

            st.success("✅ Summary generated!")
            st.markdown("---")
            st.subheader("📄 Professional Summary")
            st.markdown(summary)
