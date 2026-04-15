# Pull the required Ollama models for the RAG Pipeline Lab.
# Usage: .\scripts\pull_models.ps1

Write-Host "Pulling embedding model: nomic-embed-text..."
ollama pull nomic-embed-text

Write-Host ""
Write-Host "Pulling language model: llama3.2:3b..."
ollama pull llama3.2:3b

Write-Host ""
Write-Host "Done. Verify with: ollama list"
ollama list
