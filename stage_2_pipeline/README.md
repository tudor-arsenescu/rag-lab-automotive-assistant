# Stage 2 — Building the Pipeline (~50 min)

## Objectives

By the end of this stage you will have:

- Loaded a PDF document and split it into text chunks
- Generated vector embeddings for each chunk using Ollama
- Stored those embeddings in a ChromaDB vector database
- Built a retrieval-augmented Q&A chain that answers questions from the document

## Pipeline Overview

The pipeline has three scripts, run in order:

| Script | What it does |
|--------|--------------|
| `02_load_and_chunk.py` | Loads a PDF and splits it into overlapping text chunks |
| `03_embed_and_store.py` | Embeds the chunks and stores them in ChromaDB |
| `04_retrieval_qa.py` | Takes a user question, retrieves relevant chunks, and generates an answer |

## Key Concepts

### Document Chunking

LLMs have a limited context window. We can't feed an entire 200-page manual into the model at once. Instead, we split the document into smaller pieces (chunks) that overlap slightly so we don't lose information at chunk boundaries.

**Parameters** (mirrored from the production Java pipeline):

- `chunk_size = 920` characters — how long each chunk is
- `chunk_overlap = 230` characters — how much consecutive chunks share

### Vector Embeddings

An embedding is a list of numbers that captures the *meaning* of a text. Texts with similar meaning have similar embeddings. This is what makes semantic search work — we can find document chunks that are relevant to a question even if they don't share the exact same words.

### ChromaDB

ChromaDB is a vector database that stores embeddings and lets you search them. We use it in **persistent mode** (data saved to disk) so you don't have to re-embed every time you restart.

### Retrieval Chain

LangChain's retrieval chain ties it all together:

1. Your question gets embedded
2. ChromaDB finds the most similar document chunks
3. Those chunks are injected into a prompt template as context
4. The LLM generates an answer based only on that context

## Steps

### Step 1: Load and chunk the PDF

Open `starter/02_load_and_chunk.py`. You'll see TODO comments where you need to fill in code.

**What you'll implement:**

- Load a PDF file using `PyPDFLoader`
- Split the loaded pages into chunks using `RecursiveCharacterTextSplitter`
- Print chunk statistics to verify the split worked

Run it:

```bash
python stage_2_pipeline/starter/02_load_and_chunk.py
```

Expected output: a count of pages loaded and chunks created, plus a preview of the first chunk.

### Step 2: Embed chunks and store in ChromaDB

Open `starter/03_embed_and_store.py`. This script builds on Step 1.

**What you'll implement:**

- Initialize `OllamaEmbeddings` with the `nomic-embed-text` model
- Create a persistent `Chroma` vector store from the document chunks
- Print the number of documents stored

Run it:

```bash
python stage_2_pipeline/starter/03_embed_and_store.py
```

Expected output: confirmation of how many chunks were embedded and stored. This step may take a few minutes depending on your hardware.

### Step 3: Query the pipeline

Open `starter/04_retrieval_qa.py`. This is where the magic happens.

**What you'll implement:**

- Load the existing ChromaDB store
- Initialize the `OllamaLLM` language model
- Build a retrieval chain with a prompt template
- Ask a question and print the answer

Run it:

```bash
python stage_2_pipeline/starter/04_retrieval_qa.py
```

Try these sample questions about the Porsche Taycan:

- "What is the maximum charging power of the Taycan?"
- "How do I activate the lane keeping assistant?"
- "What is the recommended tire pressure?"

## Falling Behind?

If you can't complete a step in time, use the checkpoint code:

```bash
# Example: run the checkpoint version of step 2
python stage_2_pipeline/checkpoint/03_embed_and_store.py
```

**Important:** You still need to *run* the checkpoint code — it generates the ChromaDB data that Stage 3 depends on. Simply copying the files without running them will not work.

## What's Next

In Stage 3, you'll experiment with different prompts, compare model responses, and discuss local vs. cloud trade-offs.
