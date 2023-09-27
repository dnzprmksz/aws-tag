import os
from pathlib import Path

import pandas as pd
import pathvalidate


def validate_file_path(file_path: str):
    """
    Validate the file path.

    :param file_path: File path to validate.
    """
    pathvalidate.validate_filepath(file_path)

    if pathvalidate.sanitize_filepath(file_path) != file_path:
        raise ValueError(f'Invalid file path: {file_path}')

    if not file_path.endswith('.csv'):
        raise ValueError('File path must end with ".csv"')


def validate_file_exists(file_path: str):
    """
    Validate the file exists.

    :param file_path: File path to validate.
    """
    if not os.path.isfile(file_path):
        raise ValueError(f'File not found: {file_path}')


def write_df_to_csv(df: pd.DataFrame, file_path: str):
    """
    Write the DataFrame to a CSV file.

    :param df: DataFrame to write to a CSV file.
    :param file_path: File path to write the DataFrame to.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def read_csv_to_df(file_path: str) -> pd.DataFrame:
    """
    Read the CSV file to a DataFrame.

    :param file_path: File path to read the CSV file from.
    :return: DataFrame.
    """
    return pd.read_csv(file_path, dtype=str)
