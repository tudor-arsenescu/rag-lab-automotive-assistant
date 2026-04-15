#!/usr/bin/env bash
# Pull the required Ollama models for the RAG Pipeline Lab.
# Usage: bash scripts/pull_models.sh

set -e

echo "Pulling embedding model: nomic-embed-text..."
ollama pull nomic-embed-text

echo ""
echo "Pulling language model: llama3.2:3b..."
ollama pull llama3.2:3b

echo ""
echo "Done. Verify with: ollama list"
ollama list
