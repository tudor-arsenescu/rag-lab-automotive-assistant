#!/usr/bin/env python3
"""
Stage 2, Step 2 — Embed and Store [CHECKPOINT]
===============================================
Complete reference implementation. Use this if you fell behind.

IMPORTANT: You must RUN this script to populate the ChromaDB store.
           Stage 3 depends on the data this generates.

Usage:
    python stage_2_pipeline/checkpoint/03_embed_and_store.py
"""

import os
import sys
import time

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# --- Configuration ---
PDF_PATH = os.path.join("corpus", "Taycan_2021_EN_excerpt.pdf")
CHUNK_SIZE = 920
CHUNK_OVERLAP = 230
CHROMA_PERSIST_DIR = os.path.join("stage_2_pipeline", "checkpoint", "chroma_data")
COLLECTION_NAME = "taycan_manual"

OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"


def load_and_chunk(pdf_path: str, chunk_size: int, chunk_overlap: int):
    """Load a PDF and split into chunks."""
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(pages)


def create_vector_store(chunks, persist_directory: str):
    """Create a ChromaDB vector store from document chunks."""
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL,
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=COLLECTION_NAME,
    )

    return vectorstore


def main():
    print()
    print("=" * 50)
    print("  Stage 2, Step 2 — Embed and Store [CHECKPOINT]")
    print("=" * 50)
    print()

    if not os.path.exists(PDF_PATH):
        print(f"ERROR: PDF not found at '{PDF_PATH}'")
        sys.exit(1)

    print(f"Loading and chunking: {PDF_PATH}")
    chunks = load_and_chunk(PDF_PATH, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"Prepared {len(chunks)} chunks for embedding.")
    print()

    print(f"Embedding with {EMBEDDING_MODEL} and storing in ChromaDB...")
    print(f"Persist directory: {CHROMA_PERSIST_DIR}")
    print("This may take a few minutes on the first run.")
    print()

    start_time = time.time()
    vectorstore = create_vector_store(chunks, CHROMA_PERSIST_DIR)
    elapsed = time.time() - start_time

    count = vectorstore._collection.count()
    print(f"Done in {elapsed:.1f} seconds.")
    print(f"Stored {count} document chunks in ChromaDB.")
    print(f"Data persisted at: {os.path.abspath(CHROMA_PERSIST_DIR)}")
    print()
    print("Step 2 complete. Proceed to 04_retrieval_qa.py")


if __name__ == "__main__":
    main()
