import sys
import shutil
from pathlib import Path
from tqdm import tqdm
from ccep.extractor import extract_pdf
from ccep.chunker import chunk_markdown
from ccep.vectordb import VectorDB
from ccep.rag import RAG
from ccep.models import Document, generate_id
from ccep.config import UPLOAD_DIR


def cmd_ingest(pdf_path: str):
    path = Path(pdf_path)
    if not path.exists():
        print(f"❌ File not found: {pdf_path}")
        return 1

    print(f"📄 {path.name}:", end="", flush=True)
    total_pages = [0]
    def on_page(n, total):
        if total_pages[0] != total:
            total_pages[0] = total
            print(f" {total} pages", end="", flush=True)
    markdown = extract_pdf(str(path), on_page=on_page)
    word_count = len(markdown.split())
    print(f", {word_count} words")

    with tqdm(total=3, desc="✂️  Chunking → embedding → storing", unit="step", leave=False) as pbar:
        doc_id = generate_id(markdown)
        doc = Document(id=doc_id, title=path.stem, filename=path.name, markdown=markdown, checksum=doc_id)
        pbar.update(1)

        doc.chunks = chunk_markdown(markdown, doc_id)
        pbar.set_postfix_str(f"{len(doc.chunks)} chunks")
        pbar.update(1)

        db = VectorDB()
        db.ingest(doc.chunks)
        pbar.update(1)

    print(f"✅ Done — {len(doc.chunks)} chunks indexed")

    uploads = Path(UPLOAD_DIR)
    uploads.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(path), str(uploads / path.name))

    return 0


def cmd_query(question: str):
    rag = RAG()
    result = rag.query(question)
    print(f"\n💬 Answer:\n{result['answer']}\n")
    if result["sources"]:
        print("📚 Sources:")
        for s in result["sources"]:
            print(f"   › [{s['heading']}] {s['text'][:120]}...")
    return 0


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ccep ingest <pdf-file>")
        print("  ccep query <question>")
        return 1

    cmd = sys.argv[1]
    if cmd == "ingest" and len(sys.argv) >= 3:
        return cmd_ingest(sys.argv[2])
    elif cmd == "query" and len(sys.argv) >= 3:
        return cmd_query(" ".join(sys.argv[2:]))
    else:
        print(f"Unknown command: {cmd}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
