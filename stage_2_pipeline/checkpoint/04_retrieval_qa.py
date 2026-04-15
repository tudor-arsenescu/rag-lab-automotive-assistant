#!/usr/bin/env python3
"""
Stage 2, Step 3 — Retrieval QA [CHECKPOINT]
============================================
Complete reference implementation. Use this if you fell behind.

IMPORTANT: Requires a populated ChromaDB store from Step 2.
           Run 03_embed_and_store.py first if you haven't.

Usage:
    python stage_2_pipeline/checkpoint/04_retrieval_qa.py
"""

import os
import sys

from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- Configuration ---
CHROMA_PERSIST_DIR = os.path.join("stage_2_pipeline", "checkpoint", "chroma_data")
COLLECTION_NAME = "taycan_manual"

OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LANGUAGE_MODEL = "llama3.2:3b"

RETRIEVER_TOP_K = 10
RETRIEVER_SCORE_THRESHOLD = 0.8

PROMPT_TEMPLATE = """Based on the following context, answer the question. \
If the answer is not in the context, say 'I don't have enough information to answer that.'

Context:
{context}

Question: {question}

Answer:"""


def load_existing_store():
    """Load the persisted ChromaDB vector store."""
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL,
    )

    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )

    return vectorstore


def build_retrieval_chain(vectorstore):
    """Build a retrieval-augmented QA chain using LCEL."""
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": RETRIEVER_TOP_K,
            "score_threshold": RETRIEVER_SCORE_THRESHOLD,
        },
    )

    llm = OllamaLLM(
        model=LANGUAGE_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.0,
    )

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def main():
    print()
    print("=" * 50)
    print("  Stage 2, Step 3 — Retrieval QA [CHECKPOINT]")
    print("=" * 50)
    print()

    if not os.path.exists(CHROMA_PERSIST_DIR):
        print(f"ERROR: ChromaDB store not found at '{CHROMA_PERSIST_DIR}'")
        print("Run 03_embed_and_store.py first (this checkpoint version).")
        sys.exit(1)

    print("Loading existing ChromaDB vector store...")
    vectorstore = load_existing_store()

    count = vectorstore._collection.count()
    print(f"Loaded {count} document chunks.")
    if count == 0:
        print("ERROR: The vector store is empty. Re-run 03_embed_and_store.py.")
        sys.exit(1)
    print()

    print("Building retrieval chain...")
    chain = build_retrieval_chain(vectorstore)
    print("Ready!")
    print()

    print("Ask questions about the Porsche Taycan owner's manual.")
    print("Type 'quit' or 'exit' to stop.")
    print()

    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        print("Thinking...")
        try:
            answer = chain.invoke(question)
            print(f"\nBot: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
