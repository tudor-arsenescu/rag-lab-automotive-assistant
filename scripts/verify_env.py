#!/usr/bin/env python3
"""
Environment verification script for the RAG Pipeline Lab.
Run this before the session to confirm everything is set up correctly.

Usage:
    python scripts/verify_env.py
"""

import sys
import shutil
import subprocess
import importlib


def check(label: str, ok: bool, detail: str = ""):
    status = "PASS" if ok else "FAIL"
    marker = "+" if ok else "!"
    msg = f"  [{marker}] {label}: {status}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return ok


def main():
    print()
    print("=" * 60)
    print("  RAG Pipeline Lab — Environment Check")
    print("=" * 60)
    print()

    results = []

    # --- Python version ---
    py_version = sys.version_info
    py_ok = py_version >= (3, 10)
    results.append(
        check(
            "Python >= 3.10",
            py_ok,
            f"found {py_version.major}.{py_version.minor}.{py_version.micro}",
        )
    )

    # --- pip ---
    pip_ok = shutil.which("pip") is not None or shutil.which("pip3") is not None
    results.append(check("pip available", pip_ok))

    # --- Required Python packages ---
    packages = {
        "langchain": "langchain",
        "langchain_ollama": "langchain-ollama",
        "langchain_chroma": "langchain-chroma",
        "langchain_community": "langchain-community",
        "chromadb": "chromadb",
        "pypdf": "pypdf",
    }

    print()
    print("  Python packages:")
    for import_name, pip_name in packages.items():
        try:
            mod = importlib.import_module(import_name)
            version = getattr(mod, "__version__", "installed")
            results.append(check(f"  {pip_name}", True, version))
        except ImportError:
            results.append(
                check(f"  {pip_name}", False, f"pip install {pip_name}")
            )

    # --- Ollama ---
    print()
    print("  Ollama:")
    ollama_path = shutil.which("ollama")
    ollama_available = ollama_path is not None
    results.append(
        check("Ollama installed", ollama_available, ollama_path or "not found in PATH")
    )

    if ollama_available:
        # Check if Ollama is running by listing models
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            ollama_running = result.returncode == 0
            results.append(
                check(
                    "Ollama service running",
                    ollama_running,
                    "" if ollama_running else "start Ollama and try again",
                )
            )

            if ollama_running:
                model_output = result.stdout.lower()
                for model_name in ["nomic-embed-text", "llama3.2:3b"]:
                    # Check if model name appears in the output
                    found = model_name.replace(":", "") in model_output.replace(":", "") or model_name in model_output
                    results.append(
                        check(
                            f"  Model: {model_name}",
                            found,
                            "" if found else f"run: ollama pull {model_name}",
                        )
                    )
        except subprocess.TimeoutExpired:
            results.append(check("Ollama service running", False, "timed out"))
        except Exception as e:
            results.append(check("Ollama service running", False, str(e)))

    # --- Summary ---
    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    if passed == total:
        print(f"  All {total} checks passed. You're ready for the lab!")
    else:
        failed = total - passed
        print(f"  {passed}/{total} checks passed. {failed} issue(s) to fix.")
        print("  See PREREQS.md for setup instructions.")
        print("  See TROUBLESHOOTING.md if you're stuck.")
    print("=" * 60)
    print()

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
