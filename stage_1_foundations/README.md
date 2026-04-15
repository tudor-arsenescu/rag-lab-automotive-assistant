# Stage 1 — Foundations & Setup (~30 min)

## Objectives

By the end of this stage you will understand:

- What RAG (Retrieval-Augmented Generation) is and why it exists
- How RAG compares to fine-tuning as an approach to grounding LLM responses
- How Ollama lets you run open-source LLMs locally
- That your environment is fully working

## Key Concepts

### What is RAG?

Large Language Models are trained on massive text corpora, but they have a knowledge cutoff and they don't know anything about *your* private documents. RAG solves this by adding a **retrieval step** before generation:

1. **Index** your documents into a searchable store (vector database)
2. When a user asks a question, **retrieve** the most relevant document chunks
3. **Feed** those chunks to the LLM as context alongside the question
4. The LLM **generates** an answer grounded in your actual documents

This means the model doesn't need to "know" the answer from training — it reads the relevant parts of your documents on the fly.

### RAG vs. Fine-tuning

| | RAG | Fine-tuning |
|---|---|---|
| Updates knowledge | Instantly (re-index documents) | Requires retraining |
| Cost | Low (no GPU training needed) | High (GPU hours) |
| Hallucination control | High (answers tied to retrieved text) | Lower (model may still confabulate) |
| Best for | Q&A over documents, support bots | Style/behavior changes, domain adaptation |

### Ollama

Ollama is a tool that lets you download and run open-source LLMs on your own machine. No API keys, no cloud costs, no data leaving your laptop. For this lab we use two models:

- **nomic-embed-text** — converts text into numerical vectors (embeddings) for semantic search
- **llama3.2:3b** — a 3-billion parameter language model that generates answers

## Steps

### 1. Verify your environment

If you haven't already, run the environment check:

```bash
python scripts/verify_env.py
```

Fix any issues before proceeding. See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) for help.

### 2. Run the smoke test

This script verifies that Ollama is reachable and both models respond correctly:

```bash
python stage_1_foundations/01_smoke_test.py
```

You should see:

- A short text response from `llama3.2:3b`
- A vector (list of numbers) from `nomic-embed-text`
- Confirmation that both models are working

If both checks pass, your environment is ready. Move on to [Stage 2](../stage_2_pipeline/README.md).

## What's Next

In Stage 2, you'll use these building blocks to build a complete RAG pipeline: load a PDF, split it into chunks, embed those chunks into ChromaDB, and query them with the language model.
