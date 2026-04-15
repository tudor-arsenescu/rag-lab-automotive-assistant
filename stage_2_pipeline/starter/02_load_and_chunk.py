#!/usr/bin/env python3
"""
Stage 2, Step 1 — Load and Chunk a PDF
=======================================
Loads a PDF document and splits it into overlapping text chunks
suitable for embedding.

Usage:
    python stage_2_pipeline/starter/02_load_and_chunk.py
"""

import os
import sys

# --- Configuration ---
# Path to the PDF corpus (relative to repo root)
PDF_PATH = os.path.join("corpus", "Taycan_2021_EN_excerpt.pdf")

# Chunking parameters (mirrored from the production Java pipeline)
CHUNK_SIZE = 920            # characters per chunk
CHUNK_OVERLAP = 230         # overlap between consecutive chunks


def load_pdf(pdf_path: str):
    """Load a PDF file and return a list of Document objects (one per page)."""

    # TODO: Import PyPDFLoader from langchain_community.document_loaders
    # TODO: Create a PyPDFLoader instance with the pdf_path
    # TODO: Call .load() to get the list of page documents
    # TODO: Return the list of documents

    # Hint:
    #   from langchain_community.document_loaders import PyPDFLoader
    #   loader = PyPDFLoader(pdf_path)
    #   pages = loader.load()

    pass  # Replace this with your implementation


def chunk_documents(pages, chunk_size: int, chunk_overlap: int):
    """Split page documents into smaller overlapping chunks."""

    # TODO: Import RecursiveCharacterTextSplitter from langchain.text_splitter
    # TODO: Create a splitter with the given chunk_size and chunk_overlap
    # TODO: Call .split_documents(pages) to get the list of chunks
    # TODO: Return the list of chunks

    # Hint:
    #   from langchain.text_splitter import RecursiveCharacterTextSplitter
    #   splitter = RecursiveCharacterTextSplitter(
    #       chunk_size=chunk_size,
    #       chunk_overlap=chunk_overlap,
    #   )
    #   chunks = splitter.split_documents(pages)

    pass  # Replace this with your implementation


def main():
    print()
    print("=" * 50)
    print("  Stage 2, Step 1 — Load and Chunk PDF")
    print("=" * 50)
    print()

    # Check that the PDF exists
    if not os.path.exists(PDF_PATH):
        print(f"ERROR: PDF not found at '{PDF_PATH}'")
        print("Make sure you are running from the repo root directory.")
        sys.exit(1)

    # Load
    print(f"Loading PDF: {PDF_PATH}")
    pages = load_pdf(PDF_PATH)
    if pages is None:
        print("ERROR: load_pdf() returned None. Did you complete the TODO?")
        sys.exit(1)
    print(f"Loaded {len(pages)} pages.")
    print()

    # Chunk
    print(f"Splitting into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    chunks = chunk_documents(pages, CHUNK_SIZE, CHUNK_OVERLAP)
    if chunks is None:
        print("ERROR: chunk_documents() returned None. Did you complete the TODO?")
        sys.exit(1)
    print(f"Created {len(chunks)} chunks.")
    print()

    # Preview
    print("Preview of first chunk:")
    print("-" * 40)
    print(chunks[0].page_content[:300])
    print("...")
    print("-" * 40)
    print()
    print("Step 1 complete. Proceed to 03_embed_and_store.py")


if __name__ == "__main__":
    main()
