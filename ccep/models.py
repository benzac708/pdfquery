import hashlib
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Chunk:
    text: str
    heading: str
    index: int
    doc_id: str


@dataclass
class Document:
    id: str
    title: str
    filename: str
    markdown: str
    checksum: str
    chunks: list[Chunk] = field(default_factory=list)


def generate_id(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]
