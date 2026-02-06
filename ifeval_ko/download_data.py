"""Download IFEval-Ko dataset from HuggingFace and convert to JSONL format.

This script downloads the Korean IFEval dataset from
https://huggingface.co/datasets/allganize/IFEval-Ko
and converts it from parquet format to JSONL format compatible with this package.

Usage:
    # As a command-line tool (after pip install):
    ifeval-ko-download

    # As a Python module:
    python -m ifeval_ko.download_data

    # With custom output path:
    ifeval-ko-download --output /path/to/output.jsonl
"""

import json
import os
from importlib import resources
from pathlib import Path

import typer


def download_and_convert(output_path: str = None) -> str:
    """Download IFEval-Ko dataset from HuggingFace and save as JSONL.

    Args:
        output_path: Path where the JSONL file should be saved.
            If None, saves to the package's data directory.

    Returns:
        The path to the saved JSONL file.
    """
    try:
        from datasets import load_dataset
    except ImportError:
        raise ImportError(
            "The 'datasets' package is required to download data from HuggingFace. "
            "Install it with: pip install datasets"
        )

    if output_path is None:
        data_dir = Path(__file__).parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(data_dir / "input_data.jsonl")

    print(f"Downloading IFEval-Ko dataset from HuggingFace...")
    dataset = load_dataset("allganize/IFEval-Ko", split="train")

    print(f"Converting {len(dataset)} examples to JSONL format...")
    with open(output_path, "w", encoding="utf-8") as f:
        for example in dataset:
            record = {
                "key": example["key"],
                "prompt": example["prompt"],
                "instruction_id_list": example["instruction_id_list"],
                "kwargs": example["kwargs"],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Successfully saved {len(dataset)} examples to: {output_path}")
    return output_path


def main(
    output: str = typer.Option(
        None,
        help="Output path for the JSONL file. "
        "If not specified, saves to the package's data directory.",
    ),
):
    """Download IFEval-Ko dataset from HuggingFace and convert to JSONL."""
    download_and_convert(output)


if __name__ == "__main__":
    typer.run(main)
