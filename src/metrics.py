""" Statistical metrics calculatorengine for continuous and categorial features. """

import pandas as pd
import numpy as np

def calculate_continuous_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """ Calculates central tendency, dispersion, quantities, and sparsity for continuous numeric features."""
    if df is None or df.empty:
        return pd.DataFrame

    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) == 0:
        return pd.DataFrame()

    results = []
    for col in numeric_cols:
        series = df[col].dropna()
        total_count = len(df[col])
        valid_count = len(series)
        null_count = total_count - valid_count
        null_pct = (null_count / total_count * 100) if total_count > 0 else 0.0

        if valid_count > 0:
            mean_val = float(series.mean())
            std_val = float(series.std(ddof=1)) if valid_count > 1 else 0.0
            min_val = float(series.min())
            q1_val = float(series.quantile(0.25))
            median_val = float(series.median())
            q3_val = float(series.quantile(0.75))
            max_val = float(series.max())
        else:
            mean_val = std_val = min_val = q1_val = median_val = q3_val = max_val

        results.append({
            "Feature": col,
            "Total Count": total_count,
            "Valid Count": valid_count,
            "Null Count": null_count,
            "Null Pct (%)": null_pct,
            "Mean": mean_val,
            "Std Dev": std_val,
            "Min": min_val,
            "Q1": q1_val,
            "Median": median_val,
            "Q3": q3_val,
            "Max": max_val
        })

    return pd.DataFrame(results) if results else pd.DataFrame()

def calculate_categorical_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates cardinality, mode, modal dominance, and sparsity for categorical features."""
    cat_cols = df.select_dtypes(exclude=[np.number]).columns

    if len(cat_cols) == 0:
        return pd.DataFrame()

    results = []
    for col in cat_cols:
        raw_series = df[col]
        total_count = len(df[col])

        valid_elements = [
            str(x) for x in raw_series
            if pd.notna(x) and x is not None and str(x).strip().lower() not in ["na", "none", "<na>"]
        ]

        valid_count = len(valid_elements)
        null_count = total_count - valid_count
        null_pct = (null_count / total_count * 100) if total_count > 0 else 0.0
        unique_count = len(set(valid_elements))

        if valid_count > 0:
            valid_series = pd.Series(valid_elements)
            modes = valid_series.mode()
            mode_val = modes.iloc[0] if not modes.empty else "N/A"
            mode_freq =int((valid_series == mode_val).sum())
            mode_pct = (mode_freq / valid_count * 100)
        else:
            mode_val = "N/A"
            mode_freq = 0
            mode_pct = 0.0

        results.append({
            "Feature": col,
            "Total Count": total_count,
            "Valid Count": valid_count,
            "Null Count": null_count,
            "Null Percent (%)": null_pct,
            "Unique Count (Cardinality)": unique_count,
            "Top Mode": mode_val,
            "Mode Frequency": mode_freq,
            "Mode Percent (%)": mode_pct
        })
    return pd.DataFrame(results)