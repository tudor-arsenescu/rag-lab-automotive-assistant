#!/usr/bin/env python3
"""
Stage 3, Step 1 — Prompt Playground [CHECKPOINT]
=================================================
Complete reference implementation. Use this if you fell behind.
Requires a populated ChromaDB store from Stage 2.

Usage:
    python stage_3_exploration/checkpoint/05_prompt_playground.py
    python stage_3_exploration/checkpoint/05_prompt_playground.py --chroma-path path/to/chroma_data
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
OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LANGUAGE_MODEL = "llama3.2:3b"
COLLECTION_NAME = "taycan_manual"

CHROMA_CANDIDATE_PATHS = [
    os.path.join("stage_2_pipeline", "starter", "chroma_data"),
    os.path.join("stage_2_pipeline", "checkpoint", "chroma_data"),
    "chroma_data",  # notebook root-level
]

# --- Prompt Templates ---
PROMPTS = {
    "default": """Based on the following context, answer the question. \
If the answer is not in the context, say 'I don't have enough information to answer that.'

Context:
{context}

Question: {question}

Answer:""",

    "concise": """Answer the question in 1-2 sentences using ONLY the context below. \
If the context doesn't contain the answer, say 'Not found in the document.'

Context:
{context}

Question: {question}

Concise answer:""",

    "detailed": """You are a helpful automotive technical assistant. Using the context \
provided from a vehicle owner's manual, give a thorough and detailed answer to the \
question. Include specific numbers, steps, or warnings if present in the context. \
If the information is not available, clearly state that.

Context:
{context}

Question: {question}

Detailed answer:""",

    "comparison": """Based on the context below, answer the question. Then briefly \
explain your confidence level: are you drawing from strong evidence in the context, \
partial information, or mostly guessing?

Context:
{context}

Question: {question}

Answer and confidence:""",
}


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
    print("Complete Stage 2 first (run 03_embed_and_store.py).")
    sys.exit(1)


def load_store(chroma_path: str):
    """Load existing ChromaDB store."""
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


def build_chain(vectorstore, prompt_template: str, top_k: int = 10, score_threshold: float = 0.3):
    """Build a retrieval chain with configurable prompt and parameters.

    Returns (chain, retriever) so we can measure retrieval and generation
    times separately.
    """
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": top_k,
            "score_threshold": score_threshold,
        },
    )

    llm = OllamaLLM(
        model=LANGUAGE_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.0,
    )

    prompt = ChatPromptTemplate.from_template(prompt_template)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever


def query_with_metrics(chain, retriever, question: str):
    """Run a query and return the answer along with timing metrics."""
    t0 = time.perf_counter()
    retrieved_docs = retriever.invoke(question)
    t_retrieval = time.perf_counter() - t0

    t1 = time.perf_counter()
    answer = chain.invoke(question)
    t_total = time.perf_counter() - t1

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
    print("=" * 60)
    print("  Stage 3 — Prompt Playground [CHECKPOINT]")
    print("=" * 60)
    print()

    # Parse optional --chroma-path argument
    explicit_path = None
    if "--chroma-path" in sys.argv:
        idx = sys.argv.index("--chroma-path")
        if idx + 1 < len(sys.argv):
            explicit_path = sys.argv[idx + 1]

    chroma_path = detect_chroma_path(explicit_path)
    print(f"Using ChromaDB store at: {chroma_path}")
    vectorstore = load_store(chroma_path)

    count = vectorstore._collection.count()
    print(f"Loaded {count} document chunks.")
    if count == 0:
        print("ERROR: Store is empty. Re-run Stage 2.")
        sys.exit(1)
    print()

    current_prompt = "default"
    current_top_k = 10
    current_threshold = 0.3

    while True:
        print(f"Current settings: prompt={current_prompt}, top_k={current_top_k}, threshold={current_threshold}")
        print()
        print("Commands:")
        print("  ask <question>       — ask a question with current settings")
        print("  prompt <name>        — switch prompt (default, concise, detailed, comparison)")
        print("  topk <number>        — change top_k retrieval count")
        print("  threshold <number>   — change similarity score threshold (0.0 - 1.0)")
        print("  compare <question>   — ask the same question with ALL prompt templates")
        print("  quit                 — exit")
        print()

        user_input = input("> ").strip()
        if not user_input:
            continue

        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if command == "quit" or command == "exit":
            print("Goodbye!")
            break

        elif command == "prompt":
            if arg in PROMPTS:
                current_prompt = arg
                print(f"Switched to '{current_prompt}' prompt template.")
            else:
                print(f"Unknown prompt. Available: {', '.join(PROMPTS.keys())}")

        elif command == "topk":
            try:
                current_top_k = int(arg)
                print(f"top_k set to {current_top_k}")
            except ValueError:
                print("Provide a number, e.g.: topk 5")

        elif command == "threshold":
            try:
                current_threshold = float(arg)
                print(f"threshold set to {current_threshold}")
            except ValueError:
                print("Provide a number, e.g.: threshold 0.5")

        elif command == "ask":
            if not arg:
                print("Usage: ask <your question>")
                continue
            chain, retriever = build_chain(vectorstore, PROMPTS[current_prompt], current_top_k, current_threshold)
            print("Thinking...")
            try:
                answer, metrics = query_with_metrics(chain, retriever, arg)
                print(f"\n[{current_prompt}] Bot: {answer}\n")
                print("--- Metrics ---")
                print_metrics(metrics)
            except Exception as e:
                print(f"Error: {e}\n")

        elif command == "compare":
            if not arg:
                print("Usage: compare <your question>")
                continue
            print(f"\nComparing all prompt templates for: '{arg}'\n")
            for name, template in PROMPTS.items():
                chain, retriever = build_chain(vectorstore, template, current_top_k, current_threshold)
                try:
                    answer, metrics = query_with_metrics(chain, retriever, arg)
                    print(f"[{name}]")
                    print(f"  {answer}")
                    print(f"  --- Metrics: {metrics['chunks_retrieved']} chunks, "
                          f"retrieval {metrics['retrieval_time_s']:.3f}s, "
                          f"generation {metrics['generation_time_s']:.3f}s, "
                          f"total {metrics['total_time_s']:.3f}s")
                    print()
                except Exception as e:
                    print(f"[{name}] Error: {e}")
                    print()

        else:
            print(f"Unknown command: {command}. Type 'quit' to exit.")

        print()


if __name__ == "__main__":
    main()
