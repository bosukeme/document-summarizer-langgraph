from pypdf import PdfReader
import docx


def load_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def load_word(file) -> str:
    doc = docx.Document(file)

    return "\n".join([para.text for para in doc.paragraphs])


if __name__ == "__main__":
    # Test PDF
    path = "AI doc.pdf"
    pdf_text = load_pdf(path)
    print("PDF Content:\n", pdf_text)

    # # Test Word
    path = "AI doc.docx"
    word_text = load_word(path)
    print("Word Content:\n", word_text)
