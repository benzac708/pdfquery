from setuptools import setup

setup(
    name="ccep-rag",
    version="0.1.0",
    packages=["ccep"],
    install_requires=[
        "pdfplumber>=0.10",
        "psycopg2-binary>=2.9",
        "cohere>=5.0",
        "groq>=0.8",
        "streamlit>=1.28",
        "pyyaml>=6.0",
        "tqdm>=4.65",
    ],

    entry_points={
        "console_scripts": [
            "ccep=ccep.cli:main",
        ],
    },
)
