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

    with tqdm(total=4, desc="📄 Ingesting", unit="step") as pbar:
        pbar.set_description(f"📄 Extracting: {path.name}")
        pbar.update(0)

        markdown = extract_pdf(str(path))
        word_count = len(markdown.split())
        pbar.set_postfix_str(f"{word_count} words")
        pbar.update(1)

        doc_id = generate_id(markdown)
        doc = Document(id=doc_id, title=path.stem, filename=path.name, markdown=markdown, checksum=doc_id)
        pbar.set_description("✂️  Chunking")
        pbar.update(1)

        doc.chunks = chunk_markdown(markdown, doc_id)
        pbar.set_postfix_str(f"{len(doc.chunks)} chunks")
        pbar.set_description("🧠 Embedding + storing")
        pbar.update(1)

        db = VectorDB()
        db.ingest(doc.chunks)
        pbar.set_description("✅ Done")
        pbar.update(1)

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
