#!/usr/bin/env python3
"""
Stage 2, Step 3 — Retrieval QA
===============================
Loads the ChromaDB store from Step 2 and builds a retrieval chain
that answers questions grounded in the document.

Usage:
    python stage_2_pipeline/starter/04_retrieval_qa.py
    python stage_2_pipeline/starter/04_retrieval_qa.py --chroma-path path/to/chroma_data
"""

import os
import sys
import time

# --- Configuration ---
COLLECTION_NAME = "taycan_manual"

OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LANGUAGE_MODEL = "llama3.2:3b"

# Retrieval parameters (mirrored from the production Java pipeline)
RETRIEVER_TOP_K = 10
RETRIEVER_SCORE_THRESHOLD = 0.3

# Candidate paths for autodetection (tried in order)
CHROMA_CANDIDATE_PATHS = [
    os.path.join("stage_2_pipeline", "starter", "chroma_data"),
    os.path.join("stage_2_pipeline", "checkpoint", "chroma_data"),
    "chroma_data",  # notebook root-level
]

# The prompt template used by the Java pipeline, adapted for LangChain
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

    # TODO: Import OllamaEmbeddings from langchain_ollama
    # TODO: Import Chroma from langchain_chroma
    # TODO: Initialize the embedding model (same as in Step 2)
    # TODO: Load the existing store using Chroma(
    #           persist_directory=chroma_path,
    #           embedding_function=embeddings,
    #           collection_name=COLLECTION_NAME,
    #       )
    # TODO: Return the vector store

    # Hint:
    #   from langchain_ollama import OllamaEmbeddings
    #   from langchain_chroma import Chroma
    #
    #   embeddings = OllamaEmbeddings(
    #       model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL
    #   )
    #   vectorstore = Chroma(
    #       persist_directory=chroma_path,
    #       embedding_function=embeddings,
    #       collection_name=COLLECTION_NAME,
    #   )

    pass  # Replace this with your implementation


def build_retrieval_chain(vectorstore):
    """Build a retrieval-augmented QA chain.

    Returns (chain, retriever, llm) so we can measure retrieval and
    generation times separately.
    """

    # TODO: Import OllamaLLM from langchain_ollama
    # TODO: Import ChatPromptTemplate from langchain_core.prompts
    # TODO: Import StrOutputParser from langchain_core.output_parsers
    # TODO: Import RunnablePassthrough from langchain_core.runnables
    #
    # TODO: Create the retriever from the vectorstore:
    #   retriever = vectorstore.as_retriever(
    #       search_type="similarity_score_threshold",
    #       search_kwargs={"k": RETRIEVER_TOP_K, "score_threshold": RETRIEVER_SCORE_THRESHOLD},
    #   )
    #
    # TODO: Initialize the LLM:
    #   llm = OllamaLLM(
    #       model=LANGUAGE_MODEL,
    #       base_url=OLLAMA_BASE_URL,
    #       temperature=0.0,
    #   )
    #
    # TODO: Create the prompt template:
    #   prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    #
    # TODO: Build the chain using LCEL (LangChain Expression Language):
    #   chain = (
    #       {"context": retriever, "question": RunnablePassthrough()}
    #       | prompt
    #       | llm
    #       | StrOutputParser()
    #   )
    #
    # TODO: Return (chain, retriever, llm)

    pass  # Replace this with your implementation


def query_with_metrics(chain, retriever, question: str):
    """Run a query and return the answer along with timing metrics.

    Metrics returned:
      - chunks_retrieved : how many document chunks matched the query
      - retrieval_time_s : time to embed the question and search ChromaDB
      - generation_time_s: time for the LLM to produce the answer
      - total_time_s     : end-to-end wall-clock time
    """
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
    print("  Stage 2, Step 3 — Retrieval QA")
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

    # Load store
    vectorstore = load_existing_store(chroma_path)
    if vectorstore is None:
        print("ERROR: load_existing_store() returned None. Did you complete the TODO?")
        sys.exit(1)

    count = vectorstore._collection.count()
    print(f"Loaded {count} document chunks.")
    if count == 0:
        print("ERROR: The vector store is empty. Re-run 03_embed_and_store.py.")
        sys.exit(1)
    print()

    # Build chain
    print("Building retrieval chain...")
    result = build_retrieval_chain(vectorstore)
    if result is None:
        print("ERROR: build_retrieval_chain() returned None. Did you complete the TODO?")
        sys.exit(1)
    chain, retriever, llm = result
    print("Ready!")
    print()

    # Interactive Q&A loop
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
