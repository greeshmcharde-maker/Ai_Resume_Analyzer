import fitz  # PyMuPDF

def extract_pdf_text(uploaded_file):
    """
    Extract text from a PDF file uploaded through Streamlit.
    """
    text = ""

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text