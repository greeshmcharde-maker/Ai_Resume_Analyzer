from docx import Document

def extract_docx_text(uploaded_file):
    """
    Extract text from a DOCX file uploaded through Streamlit.
    """
    doc = Document(uploaded_file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text