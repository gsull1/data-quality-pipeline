"""Dataset ingestion and file validation module."""

from pathlib import Path
import pandas as pd

def load_dataset(file_path: str) -> pd.DataFrame:
    """Loads a tabular dataset from a CSV or Parquet format with path validation.
    
    Args:
        file_path: Relative or absolute string path to target data file.

    Returns:
        pd.DataFrame: Ingested pandas DataFrame.
    
    Raises:
        FileNotFoundError: If target path does not exist on disk.
        ValueError: If file extension is unsupported or file is empty 
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found at specified path: {file_path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(path)
    elif suffix in [".parquet", ".pq"]:
        df = pd.read_parquet(path)
    else:
        raise ValueError(f"Unsupported file extension '{suffix}'. Expected .csv or .parquet")

    if df.empty:
        raise ValueError(f"Ingested file at '{file_path}' contains no data rows")

    return df
