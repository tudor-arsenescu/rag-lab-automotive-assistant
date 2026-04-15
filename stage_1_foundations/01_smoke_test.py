#!/usr/bin/env python3
"""
Stage 1 — Smoke Test
====================
Verifies that Ollama is running and both required models respond.

Usage:
    python stage_1_foundations/01_smoke_test.py
"""

from langchain_ollama import OllamaEmbeddings, OllamaLLM

OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LANGUAGE_MODEL = "llama3.2:3b"


def test_language_model():
    """Send a simple prompt to the language model and print the response."""
    print(f"Testing language model: {LANGUAGE_MODEL}")
    print("-" * 40)

    llm = OllamaLLM(
        model=LANGUAGE_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.0,
    )

    response = llm.invoke("Say hello in one sentence.")
    print(f"Response: {response}")
    print()
    return True


def test_embedding_model():
    """Generate an embedding vector and confirm its dimensionality."""
    print(f"Testing embedding model: {EMBEDDING_MODEL}")
    print("-" * 40)

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL,
    )

    vector = embeddings.embed_query("This is a test sentence.")
    print(f"Embedding dimensions: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")
    print()
    return len(vector) > 0


def main():
    print()
    print("=" * 50)
    print("  Stage 1 — Ollama Smoke Test")
    print("=" * 50)
    print()

    try:
        llm_ok = test_language_model()
    except Exception as e:
        print(f"FAILED: {e}")
        print("Is Ollama running? Did you pull the model?")
        print(f"  ollama pull {LANGUAGE_MODEL}")
        llm_ok = False

    try:
        embed_ok = test_embedding_model()
    except Exception as e:
        print(f"FAILED: {e}")
        print("Is Ollama running? Did you pull the model?")
        print(f"  ollama pull {EMBEDDING_MODEL}")
        embed_ok = False

    print("=" * 50)
    if llm_ok and embed_ok:
        print("  Both models are working. You're ready for Stage 2!")
    else:
        print("  One or more models failed. Fix the issues above,")
        print("  then re-run this script.")
    print("=" * 50)
    print()


if __name__ == "__main__":
    main()
