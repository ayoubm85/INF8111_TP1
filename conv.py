"""Convert the semicolon-separated household power data to Parquet.

Usage:
    python conv.py
    python conv.py --input data.txt --output data.parquet

The Parquet conversion requires pandas and pyarrow:
    python -m pip install pandas pyarrow
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def convert_to_parquet(input_path: Path, output_path: Path) -> None:
    """Read ``input_path`` and write the same tabular data as Parquet."""
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(input_path, sep=";", na_values=["?"], low_memory=False)

    try:
        data.to_parquet(output_path, engine="pyarrow", index=False)
    except ImportError as exc:
        raise RuntimeError(
            "Parquet support is unavailable. Install it with: "
            "python -m pip install pyarrow"
        ) from exc

    print(f"Wrote {len(data):,} rows to {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert data.txt from semicolon-separated text to Parquet."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).with_name("data.txt"),
        help="Input text file (default: data.txt beside this script).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("data.parquet"),
        help="Output Parquet file (default: data.parquet beside this script).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    convert_to_parquet(arguments.input, arguments.output)