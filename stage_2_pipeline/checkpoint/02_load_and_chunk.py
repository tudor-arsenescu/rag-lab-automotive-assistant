#!/usr/bin/env python3
"""
Stage 2, Step 1 — Load and Chunk a PDF [CHECKPOINT]
====================================================
Complete reference implementation. Use this if you fell behind.

Usage:
    python stage_2_pipeline/checkpoint/02_load_and_chunk.py
"""

import os
import sys

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Configuration ---
PDF_PATH = os.path.join("corpus", "Taycan_2021_EN_excerpt.pdf")
CHUNK_SIZE = 920
CHUNK_OVERLAP = 230


def load_pdf(pdf_path: str):
    """Load a PDF file and return a list of Document objects (one per page)."""
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    return pages


def chunk_documents(pages, chunk_size: int, chunk_overlap: int):
    """Split page documents into smaller overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_documents(pages)
    return chunks


def main():
    print()
    print("=" * 50)
    print("  Stage 2, Step 1 — Load and Chunk PDF [CHECKPOINT]")
    print("=" * 50)
    print()

    if not os.path.exists(PDF_PATH):
        print(f"ERROR: PDF not found at '{PDF_PATH}'")
        print("Make sure you are running from the repo root directory.")
        sys.exit(1)

    print(f"Loading PDF: {PDF_PATH}")
    pages = load_pdf(PDF_PATH)
    print(f"Loaded {len(pages)} pages.")
    print()

    print(f"Splitting into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    chunks = chunk_documents(pages, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"Created {len(chunks)} chunks.")
    print()

    print("Preview of first chunk:")
    print("-" * 40)
    print(chunks[0].page_content[:300])
    print("...")
    print("-" * 40)
    print()
    print("Step 1 complete. Proceed to 03_embed_and_store.py")


if __name__ == "__main__":
    main()
