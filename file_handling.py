from PyPDF2 import PdfReader

def read_uploaded_file(uploaded_file):
    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode('utf8')
    elif uploaded_file.type == "application/pdf":
        return read_pdf(uploaded_file)
    else:
        raise ValueError("Unsupported file type.")

def read_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    essay = ""
    for page in pdf_reader.pages:
        essay += page.extract_text()
    return essay
