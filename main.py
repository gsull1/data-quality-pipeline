"""Command-Line Interface (CLI) Entry Point for Data Quality and Profiling Engine"""

import argparse
import sys
from pathlib import Path

from src.ingestion import load_dataset
from src.metrics import calculate_continuous_metrics, calculate_categorical_metrics
from src.formatter import create_quality_report_workbook

def parse_args():
    """Parses command-line argumentsusing argparse."""
    parser = argparse.ArgumentParser(
        description="Enterprise Data Quality and Profiling Engine: Ingests CSV/Parquet files and generates executive Excel reports."
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="Path to input tabular dataset (.csv or .parquet)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="data/output/data_quality_report.xlsx",
        help="Path for destination Excel report (.xlsx). Defaults to data/output/data_quality_report.xlsx"
    )
    return parser.parse_args()

def main():
    """Orchestrates dataingestion, profiling calculation, and workbook formatting."""
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    print(f"[*] Ingesting dataset from: {input_path.resolve()}")
    try:
        df = load_dataset(str(input_path))
        print(f"[*] Successfully loaded {df.shape[0]} rows and {df.shape[1]} columns")
    except Exception as e:
        print(f"[Error] Failed to load dataset: {e}", file=sys.stderr)
        sys.exit(1)

    print("[*] Calculating continuous and categorical statistical metrics...")
    df_continuous = calculate_continuous_metrics(df)
    df_categorical = calculate_categorical_metrics(df)

    print("[*] Building openpxyl styled Excel workbook...")
    wb = create_quality_report_workbook(df_continuous,df_categorical)

    # Ensure output parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        wb.save(output_path)
        print(f"[SUCCESS] Data quality report successfully saved to: {output_path.resolve()}")
    except Exception as e:
        print(f"[ERROR] Failed to save Excel workbook: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()