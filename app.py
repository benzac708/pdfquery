import streamlit as st
import tempfile
from pathlib import Path
from ccep.extractor import extract_pdf
from ccep.chunker import chunk_markdown
from ccep.vectordb import VectorDB
from ccep.rag import RAG
from ccep.models import generate_id

st.set_page_config(page_title="CCEP-RAG", page_icon="📄", layout="centered")

st.title("📄 CCEP-RAG")
st.markdown("Upload a PDF, ask questions. RAG pipeline: extract → chunk → embed → retrieve → generate.")

rag = RAG()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_file" not in st.session_state:
    st.session_state.last_file = None
if "doc_ingested" not in st.session_state:
    st.session_state.doc_ingested = False

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file and (uploaded_file.name != st.session_state.last_file or not st.session_state.doc_ingested):
    st.session_state.messages = []
    st.session_state.last_file = uploaded_file.name
    bar = st.progress(0, text="📄 Extracting pages...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(uploaded_file.getvalue())
        pdf_path = f.name

    total_pages = [0]
    def track_page(n, total):
        total_pages[0] = total
        bar.progress(int(n / total * 100), text=f"📄 Page {n}/{total}...")
    markdown = extract_pdf(pdf_path, on_page=track_page)
    words = len(markdown.split())
    bar.progress(30, text=f"📄 {words} words from {total_pages[0]} pages")

    doc_id = generate_id(markdown)
    chunks = chunk_markdown(markdown, doc_id)
    bar.progress(60, text=f"✂️  {len(chunks)} chunks")

    db = VectorDB()
    db.clear()
    db.ingest(chunks)
    bar.progress(90, text="🧠 Embedded + stored in vector DB")

    Path(pdf_path).unlink(missing_ok=True)
    st.session_state.doc_ingested = True
    bar.progress(100, text="✅ Done!")
    st.success(f"✅ Document indexed: {len(chunks)} chunks")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = rag.query(prompt)
            st.markdown(result["answer"])
            if result["sources"]:
                with st.expander("📚 Sources"):
                    for s in result["sources"]:
                        st.markdown(f"**{s['heading']}**")
                        st.markdown(f"> {s['text']}")
            st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
