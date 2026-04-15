#!/usr/bin/env python3
"""
Reset the local ChromaDB vector store for a clean re-run.
This deletes the chroma_data/ directory in the current working directory.

Usage:
    python scripts/reset_chroma.py
    python scripts/reset_chroma.py --path stage_2_pipeline/starter/chroma_data
"""

import argparse
import shutil
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Reset local ChromaDB data")
    parser.add_argument(
        "--path",
        default="chroma_data",
        help="Path to the chroma_data directory to delete (default: chroma_data)",
    )
    args = parser.parse_args()

    chroma_path = Path(args.path)

    if not chroma_path.exists():
        print(f"Nothing to reset — {chroma_path} does not exist.")
        sys.exit(0)

    print(f"Deleting {chroma_path.resolve()}...")
    shutil.rmtree(chroma_path)
    print("Done. The vector store has been reset.")
    print("Re-run the ingest step (Stage 2) to rebuild it.")


if __name__ == "__main__":
    main()
