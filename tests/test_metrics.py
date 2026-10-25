import pandas as pd
import numpy as np
from src.metrics import calculate_continuous_metrics, calculate_categorical_metrics

def test_calculate_continuous_metrics():
    data = {
        "val1":[10.0, 20.0, 30.0, np.nan],
        "val2":[1.0, 1.0, 1.0, 1.0]
    }
    df = pd.DataFrame(data)
    metrics_df = calculate_continuous_metrics(df)
    print(metrics_df)

    assert len(metrics_df) == 2
    val1_row = metrics_df[metrics_df["Feature"] == "val1"].iloc[0]
    assert val1_row["Total Count"] == 4
    assert val1_row["Valid Count"] == 3
    assert val1_row["Null Count"] == 1
    assert val1_row["Null Pct (%)"]  == 25.0
    assert val1_row["Mean"] == 20.0

def test_calculate_categorical_metrics():
    data = {
        "cat1": ["Apple", "Apple", "Banana", None]
    }
    df = pd.DataFrame(data)
    metrics_df = calculate_categorical_metrics(df)

    assert len(metrics_df) == 1
    row = metrics_df.iloc[0]
    assert row["Feature"] == "cat1"
    assert row["Total Count"] == 4
    assert row["Valid Count"] == 3
    assert row["Unique Count (Cardinality)"] == 2
    assert row["Top Mode"] == "Apple"
