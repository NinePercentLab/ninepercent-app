
import streamlit as st
import openai
import tempfile
from PyPDF2 import PdfReader

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="NinePercent", layout="centered")
st.title("📄 NinePercent – 9% LIHTC Compliance Reviewer")

st.markdown("Upload your NY HCR application materials to automatically check for compliance with the 2025 RFP, QAP, Design, and Sustainability standards.")

uploaded_files = st.file_uploader("📂 Upload one or more documents", type=["pdf", "docx", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded. Click 'Run Compliance Review' to proceed.")

    if st.button("🚀 Run Compliance Review"):
        for file in uploaded_files:
            file_name = file.name
            if file_name.endswith(".pdf"):
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(file.read())
                    tmp_file_path = tmp_file.name

                reader = PdfReader(tmp_file_path)
                full_text = ""
                for page in reader.pages:
                    full_text += page.extract_text() or ""

                st.subheader(f"📘 Review: {file_name}")
                with st.spinner("Analyzing..."):
                    response = openai.ChatCompletion.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a compliance reviewer for affordable housing LIHTC applications in New York. Check this document against the 2025 NY HCR 9% RFP and Design Guidelines."},
                            {"role": "user", "content": full_text[:12000]}
                        ],
                        temperature=0.3,
                    )
                    result = response["choices"][0]["message"]["content"]
                    st.markdown(result)

        st.success("✅ Review complete. You may download or save your results.")
