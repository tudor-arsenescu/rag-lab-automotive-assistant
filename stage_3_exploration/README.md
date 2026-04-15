# Stage 3 — Exploration & Comparison (~30 min)

## Objectives

By the end of this stage you will have:

- Experimented with different prompts and observed how they affect retrieval quality
- Compared local model responses with what a cloud-based model might produce
- Understood the trade-offs between local and cloud-hosted inference
- Seen how this pipeline connects to the real-world Android Virtual Assistant project

## Prerequisites

**You must have a populated ChromaDB vector store from Stage 2.**

If you completed Stage 2 using the starter code, your store is at:
`stage_2_pipeline/starter/chroma_data/`

If you used the Stage 2 checkpoint, your store is at:
`stage_2_pipeline/checkpoint/chroma_data/`

The exploration scripts will look for the starter path first, then fall back to the checkpoint path.

## Steps

### Step 1: Prompt Playground

Open `starter/05_prompt_playground.py`. This script lets you experiment with:

- **Different prompt templates** — see how phrasing affects the quality of answers
- **Different retrieval parameters** — adjust how many chunks are retrieved and the similarity threshold
- **Different corpus files** — try the full Taycan manual or the VW ID.3 manual (if available)

Run it:

```bash
python stage_3_exploration/starter/05_prompt_playground.py
```

**Things to try:**

1. Ask the same question with the default prompt, then switch to a more specific prompt template
2. Reduce `top_k` from 10 to 3 and see how answers change — watch how retrieval time stays roughly the same but generation time drops (less context to process)
3. Ask a question that is NOT in the document — does the model correctly say it doesn't know?
4. Use the `compare` command to ask the same question with all 4 prompt templates side by side — observe how generation time varies with prompt complexity
5. If you have the VW ID.3 manual, ingest it and compare answers across both manuals

**Reading the metrics:** Each query displays chunks retrieved, retrieval time, generation time, and total time. Use these to observe how retrieval parameters (top_k, threshold) affect performance. See Stage 2's README for a detailed explanation of each metric.

### Step 2: Local vs. Cloud Discussion

Read through `06_local_vs_cloud_notes.md` for a structured comparison of local and cloud-based LLM inference. This forms the basis for the group discussion.

**Discussion questions:**

- What are the latency and cost implications of running a 3B model on a laptop vs. calling GPT-4 via API?
- In an automotive context (no reliable internet), why is local inference the only viable option?
- What quality trade-offs do you accept with a smaller local model?
- How does RAG reduce the need for larger models?

## Falling Behind?

Use `checkpoint/05_prompt_playground.py` for the complete implementation.

## What's Next

This is the final hands-on stage. The wrap-up session will connect what you've built to the full Android Virtual Assistant architecture running on automotive hardware.
