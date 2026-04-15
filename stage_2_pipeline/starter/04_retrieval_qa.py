#!/usr/bin/env python3
"""
Stage 2, Step 3 — Retrieval QA
===============================
Loads the ChromaDB store from Step 2 and builds a retrieval chain
that answers questions grounded in the document.

Usage:
    python stage_2_pipeline/starter/04_retrieval_qa.py
"""

import os
import sys

# --- Configuration ---
CHROMA_PERSIST_DIR = os.path.join("stage_2_pipeline", "starter", "chroma_data")
COLLECTION_NAME = "taycan_manual"

OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LANGUAGE_MODEL = "llama3.2:3b"

# Retrieval parameters (mirrored from the production Java pipeline)
RETRIEVER_TOP_K = 10
RETRIEVER_SCORE_THRESHOLD = 0.3

# The prompt template used by the Java pipeline, adapted for LangChain
PROMPT_TEMPLATE = """Based on the following context, answer the question. \
If the answer is not in the context, say 'I don't have enough information to answer that.'

Context:
{context}

Question: {question}

Answer:"""


def load_existing_store():
    """Load the persisted ChromaDB vector store."""

    # TODO: Import OllamaEmbeddings from langchain_ollama
    # TODO: Import Chroma from langchain_chroma
    # TODO: Initialize the embedding model (same as in Step 2)
    # TODO: Load the existing store using Chroma(
    #           persist_directory=CHROMA_PERSIST_DIR,
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
    #       persist_directory=CHROMA_PERSIST_DIR,
    #       embedding_function=embeddings,
    #       collection_name=COLLECTION_NAME,
    #   )

    pass  # Replace this with your implementation


def build_retrieval_chain(vectorstore):
    """Build a retrieval-augmented QA chain."""

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
    # TODO: Return the chain

    pass  # Replace this with your implementation


def main():
    print()
    print("=" * 50)
    print("  Stage 2, Step 3 — Retrieval QA")
    print("=" * 50)
    print()

    # Check that the vector store exists
    if not os.path.exists(CHROMA_PERSIST_DIR):
        print(f"ERROR: ChromaDB store not found at '{CHROMA_PERSIST_DIR}'")
        print("You need to run 03_embed_and_store.py first (or use the checkpoint).")
        sys.exit(1)

    # Load store
    print("Loading existing ChromaDB vector store...")
    vectorstore = load_existing_store()
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
    chain = build_retrieval_chain(vectorstore)
    if chain is None:
        print("ERROR: build_retrieval_chain() returned None. Did you complete the TODO?")
        sys.exit(1)
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
            answer = chain.invoke(question)
            print(f"\nBot: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
