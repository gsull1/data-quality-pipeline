import pytest
import pandas as pd
from src.ingestion import load_dataset

def test_load_dataset_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    df_mock = pd.DataFrame({"col1": [1, 2], "col2": ["a","b"]})
    df_mock.to_csv(csv_file, index=False)

    df_loaded = load_dataset(str(csv_file))
    assert len(df_loaded) == 2
    assert list(df_loaded.columns) == ["col1","col2"]

def test_load_dataset_missing_file():
    with pytest.raises(FileNotFoundError):
        load_dataset("non_existent_file.csv")

def test_load_dataset_invalid_extension(tmp_path):
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("hello world")
    with pytest.raises(ValueError):
        load_dataset(str(txt_file))