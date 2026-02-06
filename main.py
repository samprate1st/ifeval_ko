#!/usr/bin/env python3
"""
Main script for processing the entire Korean IFEval dataset.

This script demonstrates how to work with the complete Korean Instruction Following
Evaluation dataset. It loads the dataset and performs basic analysis and statistics.

Usage:
    python main.py
    python main.py --data-path /path/to/input_data.jsonl
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

try:
    from ifeval_ko.evaluation import get_examples
except ImportError:
    print("Error: ifeval_ko package not installed.")
    print("Install it with: pip install -e .")
    sys.exit(1)


def analyze_dataset(examples: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze the Korean IFEval dataset and return statistics.

    Args:
        examples: List of examples from the dataset

    Returns:
        Dictionary containing dataset statistics
    """
    stats = {
        "total_examples": len(examples),
        "instruction_stats": defaultdict(int),
        "instruction_combinations": defaultdict(int),
        "prompt_stats": {
            "min_length": float('inf'),
            "max_length": 0,
            "avg_length": 0,
        },
    }

    total_prompt_length = 0

    for example in examples:
        # Track individual instructions
        for inst_id in example["instruction_id_list"]:
            stats["instruction_stats"][inst_id] += 1

        # Track instruction combinations
        combo_key = ",".join(sorted(example["instruction_id_list"]))
        stats["instruction_combinations"][combo_key] += 1

        # Track prompt length statistics
        prompt_length = len(example["prompt"])
        total_prompt_length += prompt_length
        stats["prompt_stats"]["min_length"] = min(
            stats["prompt_stats"]["min_length"], prompt_length
        )
        stats["prompt_stats"]["max_length"] = max(
            stats["prompt_stats"]["max_length"], prompt_length
        )

    # Calculate average prompt length
    stats["prompt_stats"]["avg_length"] = (
        total_prompt_length / len(examples) if examples else 0
    )

    return stats


def print_statistics(stats: Dict[str, Any]):
    """Print formatted statistics about the dataset.

    Args:
        stats: Dictionary containing dataset statistics
    """
    print("=" * 70)
    print("Korean IFEval Dataset Analysis")
    print("=" * 70)
    print()

    # Basic statistics
    print(f"Total Examples: {stats['total_examples']}")
    print()

    # Prompt statistics
    print("Prompt Length Statistics:")
    print(f"  Minimum: {stats['prompt_stats']['min_length']} characters")
    print(f"  Maximum: {stats['prompt_stats']['max_length']} characters")
    print(f"  Average: {stats['prompt_stats']['avg_length']:.2f} characters")
    print()

    # Instruction statistics
    print("Top 10 Most Common Instructions:")
    sorted_instructions = sorted(
        stats["instruction_stats"].items(), key=lambda x: x[1], reverse=True
    )
    for inst_id, count in sorted_instructions[:10]:
        percentage = (count / stats["total_examples"]) * 100
        print(f"  {inst_id}: {count} ({percentage:.1f}%)")
    print()

    # Instruction combination statistics
    print("Top 10 Most Common Instruction Combinations:")
    sorted_combos = sorted(
        stats["instruction_combinations"].items(), key=lambda x: x[1], reverse=True
    )
    for combo, count in sorted_combos[:10]:
        instructions = combo.split(",")
        combo_str = " + ".join(instructions) if len(instructions) <= 3 else f"{len(instructions)} instructions"
        percentage = (count / stats["total_examples"]) * 100
        print(f"  {combo_str}: {count} ({percentage:.1f}%)")
    print()

    print("=" * 70)


def main():
    """Main entry point for dataset analysis."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze the Korean IFEval dataset"
    )
    parser.add_argument(
        "--data-path",
        type=str,
        default=None,
        help="Path to the input JSONL file. If not specified, uses the default package data.",
    )

    args = parser.parse_args()

    try:
        print("Loading Korean IFEval dataset...")
        examples = get_examples(args.data_path)
        print(f"Successfully loaded {len(examples)} examples.")
        print()

        # Analyze the dataset
        stats = analyze_dataset(examples)

        # Print statistics
        print_statistics(stats)

        # Save statistics to file
        stats_file = Path("dataset_statistics.json")
        # Convert defaultdict to regular dict for JSON serialization
        stats_for_json = {
            "total_examples": stats["total_examples"],
            "instruction_stats": dict(stats["instruction_stats"]),
            "instruction_combinations": dict(stats["instruction_combinations"]),
            "prompt_stats": stats["prompt_stats"],
        }
        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(stats_for_json, f, ensure_ascii=False, indent=2)
        print(f"Statistics saved to: {stats_file}")

    except FileNotFoundError as e:
        print(f"Error: Dataset file not found. {e}", file=sys.stderr)
        print(
            "Please run 'ifeval-ko-download' first to download the dataset.",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
