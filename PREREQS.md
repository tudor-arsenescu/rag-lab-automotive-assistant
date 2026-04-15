# Pre-requisites

Complete these steps **before the lab session** to ensure you can code along with the demonstrations.

## 1. Python >= 3.10

Download from [python.org](https://www.python.org/downloads/) if not already installed.

Verify:

```bash
python --version    # or python3 --version on macOS/Linux
pip --version       # or pip3 --version
```

> **Windows note:** During installation, check "Add Python to PATH". If `python` is not recognized after install, restart your terminal.

> **macOS note:** macOS ships with an older Python. Use `python3` and `pip3` if `python` points to 2.x.

> **Linux note:** Install via your package manager, e.g. `sudo apt install python3 python3-pip python3-venv`.

## 2. An IDE

**VS Code** (recommended) — download from [code.visualstudio.com](https://code.visualstudio.com/). Install the Python extension.

Alternatively: PyCharm Community Edition.

## 3. Ollama

Download the desktop app from [ollama.com](https://ollama.com/) (available for Windows, macOS, and Linux).

After installing, open a terminal and pull the required models:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

Verify Ollama is running and both models are available:

```bash
ollama list
```

You should see both `nomic-embed-text` and `llama3.2:3b` in the output.

> **Tip:** You can also run `scripts/pull_models.sh` (macOS/Linux) or `scripts/pull_models.ps1` (Windows) from this repo to pull both models in one step.

## 4. Git (optional)

Needed only if you want to clone this repo. Alternatively, download the repo as a ZIP from GitHub.

```bash
git clone https://github.com/tudor-arsenescu/rag-lab-automotive-assistant.git
cd rag-lab-automotive-assistant
```

## 5. Python Virtual Environment and Packages

Create and activate a virtual environment, then install the lab dependencies:

```bash
# Create the virtual environment
python -m venv .venv

# Activate it
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (cmd):
.venv\Scripts\activate.bat
# macOS / Linux:
source .venv/bin/activate

# Install pinned dependencies
pip install -r requirements.txt
```

## 6. Verify Everything

Run the environment check script:

```bash
python scripts/verify_env.py
```

This will check Python version, installed packages, and Ollama availability. Fix any reported issues before the session.

## Summary Checklist

- [ ] Python >= 3.10 installed and in PATH
- [ ] pip available
- [ ] VS Code (or PyCharm) installed with Python extension
- [ ] Ollama installed and running
- [ ] `nomic-embed-text` model pulled
- [ ] `llama3.2:3b` model pulled
- [ ] Virtual environment created and activated
- [ ] `pip install -r requirements.txt` completed successfully
- [ ] `python scripts/verify_env.py` reports all green
