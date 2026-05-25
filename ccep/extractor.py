import pdfplumber


def extract_pdf(path: str, on_page=None) -> str:
    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                pages.append(f"## Page {page.page_number}\n\n{text.strip()}")
            if on_page:
                on_page(i + 1, total)
    return '\n\n'.join(pages)
