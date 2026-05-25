import sys
import shutil
from pathlib import Path
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

    print(f"📄 Extracting: {path.name}")
    markdown = extract_pdf(str(path))
    print(f"   Extracted {len(markdown.split())} words")

    doc_id = generate_id(markdown)
    doc = Document(id=doc_id, title=path.stem, filename=path.name, markdown=markdown, checksum=doc_id)

    doc.chunks = chunk_markdown(markdown, doc_id)
    print(f"   Created {len(doc.chunks)} chunks")

    db = VectorDB()
    db.ingest(doc.chunks)
    print(f"✅ Ingested into vector DB (collection: 'documents')")

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
