# Build Your Own AI Assistant: A RAG Pipeline Proof of Concept with Python & Ollama

**Liga AC LABS** — Universitatea Politehnica Timisoara, April 2026

---

Ever wondered how AI assistants answer questions about *your* documents — not just what they learned during training? In this hands-on lab, you'll build a **Retrieval-Augmented Generation (RAG)** pipeline from scratch using Python, Ollama, and ChromaDB.

This is the same core technology behind the **Android Virtual Assistant** project, where an in-car infotainment chatbot answers questions from the vehicle owner's manual.

You'll go from zero to a working prototype that can ingest a PDF document, store it as searchable vector embeddings, and answer natural-language questions about its content — all running locally on your laptop, with no cloud API keys required.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Your Laptop                          │
│                                                             │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  PDF     │───>│  Text        │───>│  Ollama          │   │
│  │  Document│    │  Splitter    │    │  (nomic-embed-   │   │
│  └──────────┘    │  (chunks)    │    │   text)          │   │
│                  └──────────────┘    └────────┬─────────┘   │
│                                               │             │
│                                               v             │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  Answer  │<───│  Ollama      │<──>│  ChromaDB        │   │
│  │          │    │  (llama3.2:  │    │  (vector store)  │   │
│  └──────────┘    │   3b)        │    └──────────────────┘   │
│                  └──────────────┘                            │
│                                                             │
│  LangChain orchestrates the entire pipeline                 │
└─────────────────────────────────────────────────────────────┘
```

**Ingest phase:** PDF -> split into chunks -> generate embeddings -> store in ChromaDB

**Query phase:** User question -> find relevant chunks via semantic search -> feed chunks + question to LLM -> get grounded answer

## What You'll Learn

- What RAG is, why it matters, and how it compares to fine-tuning
- How to run open-source LLMs locally using Ollama
- How vector databases (ChromaDB) enable semantic search over documents
- How to wire everything together with LangChain into a working Q&A pipeline
- The trade-offs between local and cloud-hosted models in real-world applications

## Lab Structure (Single 2-Hour Session)

| Part | Topic | Duration | Folder |
|------|-------|----------|--------|
| 1 | Foundations & Setup | ~30 min | `stage_1_foundations/` |
| 2 | Building the Pipeline | ~50 min | `stage_2_pipeline/` |
| 3 | Exploration & Comparison | ~30 min | `stage_3_exploration/` |
| -- | Wrap-up & Q&A | ~10 min | -- |

## How to Use This Repo

### Before the session

Complete the steps in [PREREQS.md](PREREQS.md) — install Python, Ollama, pull the required models, and set up a virtual environment.

Run the environment check to make sure everything is ready:

```bash
python scripts/verify_env.py
```

### During the session

Work through each stage in order. Each stage folder contains:

- **README.md** — concepts and step-by-step instructions
- **starter/** — code files with TODO placeholders for you to complete
- **checkpoint/** — completed reference code you can use if you fall behind

**Important:** Stages build on each other. Stage 3 requires the ChromaDB vector store created during Stage 2. If you fall behind during a stage, use that stage's `checkpoint/` code to catch up, but you still need to *run* it to generate the required outputs before moving on.

### Scripts or Notebooks?

This repo provides both `.py` scripts and a Jupyter notebook (`lab.ipynb`).

**If you're comfortable with the terminal**, use the `.py` scripts — they match the folder structure and are easier to follow along with the live demo.

**If you prefer an interactive environment** (or if your terminal setup has issues), open `lab.ipynb` in VS Code or Jupyter and work through the cells. The notebook mirrors the same stages.

> **Presenter note:** At the start of the session, ask students:
> 1. "Can everyone run `python --version` in their terminal?" — if yes, scripts are the primary track.
> 2. "Who has used Jupyter notebooks before?" — those students can optionally use the notebook.

## Corpus

The `corpus/` folder contains vehicle owner's manual PDFs used as the document source for the RAG pipeline:

- **`Taycan_2021_EN.pdf`** (7.5 MB) — Porsche Taycan owner's manual (primary corpus)
- **`Taycan_2021_EN_excerpt.pdf`** (~780 KB) — first 10 pages only (use for quick testing)

An additional corpus (Volkswagen ID.3 manual, ~40 MB) will be distributed separately at the session for the exploration stage.

## Hardware Recommendations

- **RAM:** 8 GB minimum (16 GB recommended for comfortable model loading)
- **Disk:** ~5 GB free (for Ollama models + ChromaDB data)
- **No GPU required** — the lab runs entirely on CPU

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common issues with Ollama, ChromaDB, and package installation.

## Context: The Android Virtual Assistant Project

This lab builds a simplified version of the RAG pipeline used in an automotive infotainment proof of concept. The production system runs on a Samsung Exynos Auto V9 head unit with Android 12L, using on-device LLM inference via llama.cpp and JNI. The pipeline you build today is the same retrieve-and-generate pattern — just in Python instead of Java, and on your laptop instead of a car dashboard.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
