# Troubleshooting

Common issues and solutions for the RAG pipeline lab.

## Ollama

### "command not found: ollama"

Ollama is not in your PATH. On macOS/Linux, try restarting your terminal. On Windows, ensure the Ollama installer completed and restart PowerShell.

### "Error: pull model manifest: ... connection refused"

The Ollama service is not running. Start it:

- **macOS:** Open the Ollama app from Applications.
- **Windows:** Launch Ollama from the Start menu or system tray.
- **Linux:** Run `ollama serve` in a separate terminal.

### Model pull is very slow or times out

Large models can take several minutes to download. If the network is slow:

1. Check your connection speed.
2. If at the lab venue and wifi is congested, ask the presenter for a local copy.
3. The `llama3.2:3b` model is ~2 GB. `nomic-embed-text` is ~274 MB.

### "Error: model 'xxx' not found"

Run `ollama list` to see which models are available. Pull missing models:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

## Python / pip

### "python: command not found"

- Try `python3` instead of `python` (common on macOS/Linux).
- On Windows, ensure Python was installed with "Add to PATH" checked. If not, reinstall or add manually.

### "No module named 'venv'"

On some Linux distributions, venv is a separate package:

```bash
sudo apt install python3-venv    # Debian/Ubuntu
sudo dnf install python3-venv    # Fedora
```

### pip install fails with dependency conflicts

The `requirements.txt` uses pinned versions tested together. If you see conflicts:

1. Make sure you are in a clean virtual environment (not using system Python).
2. Delete and recreate the venv:

```bash
# Deactivate first if active
deactivate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate    # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
```

3. If conflicts persist, try installing without version pins as a fallback:

```bash
pip install langchain langchain-ollama langchain-chroma chromadb pypdf
```

### "Microsoft Visual C++ 14.0 or greater is required" (Windows)

ChromaDB's dependencies may need C++ build tools on Windows. Install them from:
[Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

Select "Desktop development with C++" workload during installation.

## ChromaDB

### "sqlite3.OperationalError: no such module: fts5"

Your system SQLite is too old. Solutions:

- **macOS:** `brew install sqlite3` and restart your terminal.
- **Linux:** `sudo apt install libsqlite3-dev` and reinstall Python.
- **Windows:** This is rare; update Python to the latest 3.10+ release.

### ChromaDB data seems stale / wrong results

Reset the local vector store:

```bash
python scripts/reset_chroma.py
```

Then re-run the ingest step from Stage 2.

## Jupyter Notebook

### "jupyter: command not found"

Install Jupyter in your virtual environment:

```bash
pip install jupyter
```

Or open the `.ipynb` file directly in VS Code (it handles Jupyter kernels automatically).

### Notebook kernel does not see installed packages

Make sure the notebook kernel is using your virtual environment:

1. In VS Code: click the kernel selector (top right of notebook) and choose the `.venv` Python interpreter.
2. In Jupyter: install the kernel explicitly:

```bash
pip install ipykernel
python -m ipykernel install --user --name=rag-lab
```

Then select "rag-lab" as the kernel.

## Stage-Specific Issues

### Stage 2: Embedding takes a very long time

On machines with limited RAM (< 8 GB), embedding large PDFs can be slow. Options:

1. Use the smaller excerpt PDF: `corpus/Taycan_2021_EN_excerpt.pdf`
2. Reduce `chunk_size` in the splitter configuration.
3. Use the checkpoint code from `stage_2_pipeline/checkpoint/` to continue.

### Stage 3: "No documents found in vector store"

You need to complete Stage 2 first — the vector store must be populated. If you used checkpoint code, make sure you actually ran it (not just copied the files).

## Still Stuck?

Raise your hand during the lab session. The presenter will help you debug, or you can follow along with the live demo while your environment issue is resolved.
