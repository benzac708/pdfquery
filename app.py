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
if "doc_ingested" not in st.session_state:
    st.session_state.doc_ingested = False

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file and not st.session_state.doc_ingested:
    progress = st.progress(0, text="Saving uploaded file...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(uploaded_file.getvalue())
        pdf_path = f.name

    progress.progress(25, text="Extracting text from PDF...")
    markdown = extract_pdf(pdf_path)

    progress.progress(50, text=f"Chunking {len(markdown.split())} words...")
    doc_id = generate_id(markdown)
    chunks = chunk_markdown(markdown, doc_id)

    progress.progress(75, text=f"Embedding {len(chunks)} chunks via Cohere and storing in vector DB...")
    db = VectorDB()
    db.ingest(chunks)

    Path(pdf_path).unlink(missing_ok=True)
    st.session_state.doc_ingested = True
    progress.progress(100, text="✅ Done!")
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
