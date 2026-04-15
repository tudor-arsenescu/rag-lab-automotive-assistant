#!/usr/bin/env python3
"""
Stage 3, Step 1 — Prompt Playground
====================================
Experiment with different prompts, retrieval parameters, and corpus files.
Requires a populated ChromaDB store from Stage 2.

Usage:
    python stage_3_exploration/starter/05_prompt_playground.py
"""

import os
import sys

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

# Try starter path first, fall back to checkpoint path
CHROMA_PATHS = [
    os.path.join("stage_2_pipeline", "starter", "chroma_data"),
    os.path.join("stage_2_pipeline", "checkpoint", "chroma_data"),
]

# --- Prompt Templates to Experiment With ---
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


def find_chroma_path():
    """Find the first available ChromaDB store path."""
    for path in CHROMA_PATHS:
        if os.path.exists(path):
            return path
    return None


def load_store(chroma_path: str):
    """Load existing ChromaDB store."""

    # TODO: Initialize OllamaEmbeddings and load the Chroma store
    #       (same pattern as Stage 2, Step 3)
    #
    # Hint:
    #   embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)
    #   vectorstore = Chroma(
    #       persist_directory=chroma_path,
    #       embedding_function=embeddings,
    #       collection_name=COLLECTION_NAME,
    #   )
    #   return vectorstore

    pass  # Replace this with your implementation


def build_chain(vectorstore, prompt_template: str, top_k: int = 10, score_threshold: float = 0.8):
    """Build a retrieval chain with configurable prompt and parameters."""

    # TODO: Build a retrieval chain (same pattern as Stage 2, Step 3)
    #       but use the provided prompt_template, top_k, and score_threshold
    #
    # Hint:
    #   retriever = vectorstore.as_retriever(
    #       search_type="similarity_score_threshold",
    #       search_kwargs={"k": top_k, "score_threshold": score_threshold},
    #   )
    #   llm = OllamaLLM(model=LANGUAGE_MODEL, base_url=OLLAMA_BASE_URL, temperature=0.0)
    #   prompt = ChatPromptTemplate.from_template(prompt_template)
    #   chain = (
    #       {"context": retriever, "question": RunnablePassthrough()}
    #       | prompt
    #       | llm
    #       | StrOutputParser()
    #   )
    #   return chain

    pass  # Replace this with your implementation


def main():
    print()
    print("=" * 60)
    print("  Stage 3 — Prompt Playground")
    print("=" * 60)
    print()

    # Find and load store
    chroma_path = find_chroma_path()
    if chroma_path is None:
        print("ERROR: No ChromaDB store found.")
        print("Complete Stage 2 first (run 03_embed_and_store.py).")
        sys.exit(1)

    print(f"Using ChromaDB store at: {chroma_path}")
    vectorstore = load_store(chroma_path)
    if vectorstore is None:
        print("ERROR: load_store() returned None. Did you complete the TODO?")
        sys.exit(1)

    count = vectorstore._collection.count()
    print(f"Loaded {count} document chunks.")
    if count == 0:
        print("ERROR: Store is empty. Re-run Stage 2.")
        sys.exit(1)
    print()

    # Menu
    current_prompt = "default"
    current_top_k = 10
    current_threshold = 0.8

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
            chain = build_chain(vectorstore, PROMPTS[current_prompt], current_top_k, current_threshold)
            if chain is None:
                print("ERROR: build_chain() returned None. Did you complete the TODO?")
                continue
            print("Thinking...")
            try:
                answer = chain.invoke(arg)
                print(f"\n[{current_prompt}] Bot: {answer}\n")
            except Exception as e:
                print(f"Error: {e}\n")

        elif command == "compare":
            if not arg:
                print("Usage: compare <your question>")
                continue
            print(f"\nComparing all prompt templates for: '{arg}'\n")
            for name, template in PROMPTS.items():
                chain = build_chain(vectorstore, template, current_top_k, current_threshold)
                if chain is None:
                    print(f"[{name}] ERROR: build_chain() returned None.")
                    continue
                try:
                    answer = chain.invoke(arg)
                    print(f"[{name}]")
                    print(f"  {answer}")
                    print()
                except Exception as e:
                    print(f"[{name}] Error: {e}")
                    print()

        else:
            print(f"Unknown command: {command}. Type 'quit' to exit.")

        print()


if __name__ == "__main__":
    main()
