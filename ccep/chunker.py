import re
from ccep.config import CHUNK_SIZE
from ccep.models import Chunk


def chunk_markdown(markdown: str, doc_id: str) -> list[Chunk]:
    heading_pattern = r'^(#{1,6}\s+.+)$'
    parts = re.split(heading_pattern, markdown, flags=re.MULTILINE)

    chunks: list[Chunk] = []
    current_heading = "Introduction"
    current_lines: list[str] = []
    current_words = 0
    chunk_idx = 0

    def flush():
        nonlocal chunk_idx
        if not current_lines:
            return
        text = '\n\n'.join(current_lines).strip()
        if not text:
            return
        chunks.append(Chunk(text=text, heading=current_heading, index=chunk_idx, doc_id=doc_id))
        chunk_idx += 1

    i = 0
    while i < len(parts):
        part = parts[i]
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', part, re.MULTILINE)
        if heading_match:
            flush()
            current_heading = heading_match.group(2).strip()
            current_lines = []
            current_words = 0
        else:
            paras = [p.strip() for p in part.split('\n\n') if p.strip()]
            for para in paras:
                wc = len(para.split())
                if current_words + wc > CHUNK_SIZE and current_lines:
                    flush()
                    overlap = current_lines[-1:] if current_lines else []
                    current_lines = overlap + [para]
                    current_words = sum(len(p.split()) for p in current_lines)
                else:
                    current_lines.append(para)
                    current_words += wc
        i += 1

    flush()
    return chunks
