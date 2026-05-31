import fitz
from docx import Document


def extract_text_from_pdf(
    pdf_path
):

    text = ""

    pdf_document = fitz.open(
        pdf_path
    )

    for page in pdf_document:

        text += page.get_text()

    return text


def extract_text_from_docx(
    docx_path
):

    doc = Document(
        docx_path
    )

    text = ""

    for para in doc.paragraphs:

        text += para.text + "\n"

    return text


def extract_text_from_txt(
    txt_path
):

    with open(
        txt_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def extract_resume_text(
    file_path
):

    if file_path.endswith(".pdf"):

        return extract_text_from_pdf(
            file_path
        )

    elif file_path.endswith(".docx"):

        return extract_text_from_docx(
            file_path
        )

    elif file_path.endswith(".txt"):

        return extract_text_from_txt(
            file_path
        )

    else:

        return "Unsupported file format"