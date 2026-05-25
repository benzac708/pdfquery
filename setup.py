from setuptools import setup

setup(
    name="ccep-rag",
    version="0.1.0",
    packages=["ccep"],
    install_requires=[
        "pdfplumber>=0.10",
        "chromadb>=0.4",
        "sentence-transformers>=2.2",
        "cohere>=5.0",
        "groq>=0.8",
        "streamlit>=1.28",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "ccep=ccep.cli:main",
        ],
    },
)
