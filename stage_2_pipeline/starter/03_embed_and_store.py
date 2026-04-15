#!/usr/bin/env python3
"""
Stage 2, Step 2 — Embed and Store
==================================
Loads chunks from Step 1, generates embeddings via Ollama,
and stores them in a persistent ChromaDB vector store.

Usage:
    python stage_2_pipeline/starter/03_embed_and_store.py
"""

import os
import sys
import time

# We reuse the loading/chunking from Step 1
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Configuration ---
PDF_PATH = os.path.join("corpus", "Taycan_2021_EN_excerpt.pdf")
CHUNK_SIZE = 920
CHUNK_OVERLAP = 230
CHROMA_PERSIST_DIR = os.path.join("stage_2_pipeline", "starter", "chroma_data")
COLLECTION_NAME = "taycan_manual"

OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"


def load_and_chunk(pdf_path: str, chunk_size: int, chunk_overlap: int):
    """Load a PDF and split into chunks (reuses Step 1 logic)."""
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(pages)


def create_vector_store(chunks, persist_directory: str):
    """Create a ChromaDB vector store from document chunks."""

    # TODO: Import OllamaEmbeddings from langchain_ollama
    # TODO: Import Chroma from langchain_chroma
    # TODO: Initialize OllamaEmbeddings with model=EMBEDDING_MODEL and base_url=OLLAMA_BASE_URL
    # TODO: Create the vector store using Chroma.from_documents(
    #           documents=chunks,
    #           embedding=embeddings,
    #           persist_directory=persist_directory,
    #           collection_name=COLLECTION_NAME,
    #       )
    # TODO: Return the vector store

    # Hint:
    #   from langchain_ollama import OllamaEmbeddings
    #   from langchain_chroma import Chroma
    #
    #   embeddings = OllamaEmbeddings(
    #       model=EMBEDDING_MODEL,
    #       base_url=OLLAMA_BASE_URL,
    #   )
    #
    #   vectorstore = Chroma.from_documents(
    #       documents=chunks,
    #       embedding=embeddings,
    #       persist_directory=persist_directory,
    #       collection_name=COLLECTION_NAME,
    #   )

    pass  # Replace this with your implementation


def main():
    print()
    print("=" * 50)
    print("  Stage 2, Step 2 — Embed and Store")
    print("=" * 50)
    print()

    if not os.path.exists(PDF_PATH):
        print(f"ERROR: PDF not found at '{PDF_PATH}'")
        sys.exit(1)

    # Load and chunk
    print(f"Loading and chunking: {PDF_PATH}")
    chunks = load_and_chunk(PDF_PATH, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"Prepared {len(chunks)} chunks for embedding.")
    print()

    # Embed and store
    print(f"Embedding with {EMBEDDING_MODEL} and storing in ChromaDB...")
    print(f"Persist directory: {CHROMA_PERSIST_DIR}")
    print("This may take a few minutes on the first run.")
    print()

    start_time = time.time()
    vectorstore = create_vector_store(chunks, CHROMA_PERSIST_DIR)
    elapsed = time.time() - start_time

    if vectorstore is None:
        print("ERROR: create_vector_store() returned None. Did you complete the TODO?")
        sys.exit(1)

    # Verify
    count = vectorstore._collection.count()
    print(f"Done in {elapsed:.1f} seconds.")
    print(f"Stored {count} document chunks in ChromaDB.")
    print(f"Data persisted at: {os.path.abspath(CHROMA_PERSIST_DIR)}")
    print()
    print("Step 2 complete. Proceed to 04_retrieval_qa.py")


if __name__ == "__main__":
    main()
