"""
Utility Module: data_profiler.py

Description:
------------
Provides reusable utilities for profiling tabular datasets.
The generated profile offers a quick overview of dataset structure,
quality, and composition before EDA or preprocessing.

Author : Rishav Poddar
Project: AI Credit Risk Analysis Platform
"""

import pandas as pd


def profile_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a high-level summary of a dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.

    Returns
    -------
    pd.DataFrame
        Dataset profiling report.
    """

    total_rows = df.shape[0]
    total_columns = df.shape[1]

    numerical_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).shape[1]

    categorical_columns = df.select_dtypes(
        include=["object"]
    ).shape[1]

    boolean_columns = df.select_dtypes(
        include=["bool"]
    ).shape[1]

    duplicate_rows = df.duplicated().sum()

    total_missing = df.isnull().sum().sum()

    memory_mb = round(
        df.memory_usage(deep=True).sum() / (1024 ** 2),
        2
    )

    report = {

        "Metric": [

            "Rows",
            "Columns",
            "Numerical Columns",
            "Categorical Columns",
            "Boolean Columns",
            "Duplicate Rows",
            "Missing Values",
            "Memory Usage (MB)"

        ],

        "Value": [

            total_rows,
            total_columns,
            numerical_columns,
            categorical_columns,
            boolean_columns,
            duplicate_rows,
            total_missing,
            memory_mb

        ]

    }

    return pd.DataFrame(report)