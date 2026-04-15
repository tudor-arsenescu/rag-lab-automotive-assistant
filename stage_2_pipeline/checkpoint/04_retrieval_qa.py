#!/usr/bin/env python3
"""
Stage 2, Step 3 — Retrieval QA [CHECKPOINT]
============================================
Complete reference implementation. Use this if you fell behind.

IMPORTANT: Requires a populated ChromaDB store from Step 2.
           Run 03_embed_and_store.py first if you haven't.

Usage:
    python stage_2_pipeline/checkpoint/04_retrieval_qa.py
    python stage_2_pipeline/checkpoint/04_retrieval_qa.py --chroma-path path/to/chroma_data
"""

import os
import sys
import time

from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- Configuration ---
COLLECTION_NAME = "taycan_manual"

OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LANGUAGE_MODEL = "llama3.2:3b"

RETRIEVER_TOP_K = 10
RETRIEVER_SCORE_THRESHOLD = 0.3

# Candidate paths for autodetection (tried in order)
CHROMA_CANDIDATE_PATHS = [
    os.path.join("stage_2_pipeline", "starter", "chroma_data"),
    os.path.join("stage_2_pipeline", "checkpoint", "chroma_data"),
    "chroma_data",  # notebook root-level
]

PROMPT_TEMPLATE = """Based on the following context, answer the question. \
If the answer is not in the context, say 'I don't have enough information to answer that.'

Context:
{context}

Question: {question}

Answer:"""


def detect_chroma_path(explicit_path=None):
    """Find the ChromaDB store: use explicit path if given, otherwise autodetect."""
    if explicit_path:
        if os.path.exists(explicit_path):
            return explicit_path
        print(f"ERROR: Specified ChromaDB path not found: '{explicit_path}'")
        sys.exit(1)

    for path in CHROMA_CANDIDATE_PATHS:
        if os.path.exists(path):
            return path

    print("ERROR: No ChromaDB store found. Searched:")
    for path in CHROMA_CANDIDATE_PATHS:
        print(f"  - {path}")
    print("Run 03_embed_and_store.py first to create the vector store.")
    sys.exit(1)


def load_existing_store(chroma_path: str):
    """Load the persisted ChromaDB vector store."""
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL,
    )

    vectorstore = Chroma(
        persist_directory=chroma_path,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )

    return vectorstore


def build_retrieval_chain(vectorstore):
    """Build a retrieval-augmented QA chain using LCEL.

    Returns (chain, retriever, llm) so we can measure retrieval and
    generation times separately.
    """
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

    return chain, retriever, llm


def query_with_metrics(chain, retriever, question: str):
    """Run a query and return the answer along with timing metrics."""
    # --- Retrieval timing ---
    t0 = time.perf_counter()
    retrieved_docs = retriever.invoke(question)
    t_retrieval = time.perf_counter() - t0

    # --- End-to-end timing (retrieval + prompt + generation) ---
    t1 = time.perf_counter()
    answer = chain.invoke(question)
    t_total = time.perf_counter() - t1

    # Generation time is approximately total minus retrieval
    t_generation = max(t_total - t_retrieval, 0.0)

    metrics = {
        "chunks_retrieved": len(retrieved_docs),
        "retrieval_time_s": round(t_retrieval, 3),
        "generation_time_s": round(t_generation, 3),
        "total_time_s": round(t_total, 3),
    }

    return answer, metrics


def print_metrics(metrics: dict):
    """Print timing metrics in a readable format."""
    print(f"  Chunks retrieved : {metrics['chunks_retrieved']}")
    print(f"  Retrieval time   : {metrics['retrieval_time_s']:.3f}s")
    print(f"  Generation time  : {metrics['generation_time_s']:.3f}s")
    print(f"  Total time       : {metrics['total_time_s']:.3f}s")


def main():
    print()
    print("=" * 50)
    print("  Stage 2, Step 3 — Retrieval QA [CHECKPOINT]")
    print("=" * 50)
    print()

    # Parse optional --chroma-path argument
    explicit_path = None
    if "--chroma-path" in sys.argv:
        idx = sys.argv.index("--chroma-path")
        if idx + 1 < len(sys.argv):
            explicit_path = sys.argv[idx + 1]

    chroma_path = detect_chroma_path(explicit_path)
    print(f"Using ChromaDB store: {chroma_path}")

    vectorstore = load_existing_store(chroma_path)

    count = vectorstore._collection.count()
    print(f"Loaded {count} document chunks.")
    if count == 0:
        print("ERROR: The vector store is empty. Re-run 03_embed_and_store.py.")
        sys.exit(1)
    print()

    print("Building retrieval chain...")
    chain, retriever, llm = build_retrieval_chain(vectorstore)
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
            answer, metrics = query_with_metrics(chain, retriever, question)
            print(f"\nBot: {answer}\n")
            print("--- Metrics ---")
            print_metrics(metrics)
            print()
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
