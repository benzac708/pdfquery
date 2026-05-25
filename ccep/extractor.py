import pdfplumber


def extract_pdf(path: str) -> str:
    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(f"## Page {page.page_number}\n\n{text.strip()}")
    return '\n\n'.join(pages)
