import streamlit as st
from PyPDF2 import PdfReader

def read_uploaded_file(uploaded_file):
    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode('utf8')
    elif uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    else:
        raise ValueError("Unsupported file type.")  

def extract_text_from_pdf(uploaded_file):
    pdf_text = ""
    try:
        pdf_reader = PdfReader(uploaded_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text() + "\n"
    except Exception as e:
        st.error(f"An error occurred while extracting text: {e}")
    return pdf_text

  