"""Update IFEval-Ko dataset from HuggingFace.

This script downloads the latest Korean IFEval dataset from
https://huggingface.co/datasets/allganize/IFEval-Ko
and updates the local JSONL file.

Usage:
    # As a command-line tool (after pip install):
    ifeval-ko-update

    # As a Python module:
    python -m ifeval_ko.update_data

    # With custom output path:
    ifeval-ko-update --output /path/to/output.jsonl
"""

import json
import os
from datetime import datetime
from pathlib import Path

import typer


def update_dataset(output_path: str = None) -> str:
    """Update IFEval-Ko dataset from HuggingFace and save as JSONL.

    Downloads the latest version of the dataset from HuggingFace and saves it
    to the specified location. If a backup already exists, creates a timestamped backup.

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

    # Create backup if file exists
    output_path_obj = Path(output_path)
    if output_path_obj.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = output_path_obj.parent / f"{output_path_obj.stem}_backup_{timestamp}{output_path_obj.suffix}"
        import shutil
        shutil.copy2(output_path, backup_path)
        print(f"Backup created at: {backup_path}")

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

    print(f"Successfully updated dataset with {len(dataset)} examples at: {output_path}")
    return output_path


def main(
    output: str = typer.Option(
        None,
        help="Output path for the JSONL file. "
        "If not specified, saves to the package's data directory.",
    ),
):
    """Update IFEval-Ko dataset from HuggingFace and convert to JSONL."""
    update_dataset(output)


if __name__ == "__main__":
    typer.run(main)
