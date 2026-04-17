"""
Data Transformation and Management Utilities

This module provides utilities for loading, transforming, and managing dataframes
from the fetchAPI skill output. It handles CSV data from AdventureWorks datasets
and provides tools for data cleaning, transformation, and aggregation.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from pandas import DataFrame


# Configuration
SKILL_BASE = Path(__file__).resolve().parent
DATA_DIR = SKILL_BASE / ".claude" / "skills" / "fetchAPI" / "data"
LOG_DIR = SKILL_BASE / ".claude" / "skills" / "fetchAPI" / "logs"


def setup_logger(log_file: Optional[Path] = None) -> logging.Logger:
    """
    Configure and return a logger for data operations.

    Args:
        log_file: Optional path to log file. If None, creates one in logs directory.

    Returns:
        Configured logger instance.
    """
    if log_file is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_dir = LOG_DIR / timestamp
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "dataframe_operations.log"

    logger = logging.getLogger("dataframe_manager")
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def load_csv_data(file_path: Path, logger: logging.Logger) -> Optional[DataFrame]:
    """
    Load CSV data from file into a pandas DataFrame.

    Args:
        file_path: Path to the CSV file.
        logger: Logger instance for tracking operations.

    Returns:
        DataFrame if successful, None otherwise.
    """
    try:
        df = pd.read_csv(file_path)
        logger.info("Loaded %s with shape %s", file_path.name, df.shape)
        return df
    except Exception as e:
        logger.error("Failed to load %s: %s", file_path, e)
        return None


def load_latest_data(logger: logging.Logger) -> dict[str, DataFrame]:
    """
    Load the latest dataset from the most recent timestamped directory.

    Args:
        logger: Logger instance for tracking operations.

    Returns:
        Dictionary mapping file names to DataFrames.
    """
    if not DATA_DIR.exists():
        logger.warning("Data directory does not exist: %s", DATA_DIR)
        return {}

    # Find the latest timestamped directory
    timestamped_dirs = sorted([d for d in DATA_DIR.iterdir() if d.is_dir()])
    if not timestamped_dirs:
        logger.warning("No timestamped data directories found in %s", DATA_DIR)
        return {}

    latest_dir = timestamped_dirs[-1]
    logger.info("Loading data from %s", latest_dir.name)

    data = {}
    for csv_file in latest_dir.glob("*.csv"):
        df = load_csv_data(csv_file, logger)
        if df is not None:
            data[csv_file.stem] = df

    return data


def validate_dataframe(df: DataFrame, logger: logging.Logger) -> dict:
    """
    Validate and provide statistics about a DataFrame.

    Args:
        df: DataFrame to validate.
        logger: Logger instance for tracking operations.

    Returns:
        Dictionary with validation results.
    """
    validation = {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
        "duplicates": df.duplicated().sum(),
    }

    logger.info("Validation: %s rows, %s columns", validation["shape"][0], validation["shape"][1])
    logger.info("Null values: %s", validation["null_counts"])
    logger.info("Duplicates: %s", validation["duplicates"])

    return validation


def clean_dataframe(df: DataFrame, drop_nulls: bool = False, logger: Optional[logging.Logger] = None) -> DataFrame:
    """
    Clean dataframe by handling null values and duplicates.

    Args:
        df: DataFrame to clean.
        drop_nulls: If True, drop rows with any null values.
        logger: Optional logger instance.

    Returns:
        Cleaned DataFrame.
    """
    df_clean = df.copy()
    initial_rows = len(df_clean)

    if drop_nulls:
        df_clean = df_clean.dropna()
        removed = initial_rows - len(df_clean)
        if logger:
            logger.info("Removed %s rows with null values", removed)

    df_clean = df_clean.drop_duplicates()
    removed_dups = initial_rows - len(df_clean)
    if removed_dups > 0 and logger:
        logger.info("Removed %s duplicate rows", removed_dups)

    return df_clean


def merge_dataframes(df1: DataFrame, df2: DataFrame, on: str, how: str = "inner", logger: Optional[logging.Logger] = None) -> DataFrame:
    """
    Merge two DataFrames on a common column.

    Args:
        df1: First DataFrame.
        df2: Second DataFrame.
        on: Column name to merge on.
        how: Type of merge ('inner', 'outer', 'left', 'right').
        logger: Optional logger instance.

    Returns:
        Merged DataFrame.
    """
    try:
        merged_df = pd.merge(df1, df2, on=on, how=how)
        if logger:
            logger.info("Merged dataframes on '%s' using %s join. Result shape: %s", on, how, merged_df.shape)
        return merged_df
    except Exception as e:
        if logger:
            logger.error("Failed to merge dataframes: %s", e)
        raise


def aggregate_data(df: DataFrame, group_by: str | list, agg_dict: dict, logger: Optional[logging.Logger] = None) -> DataFrame:
    """
    Aggregate DataFrame data using groupby and aggregation functions.

    Args:
        df: DataFrame to aggregate.
        group_by: Column name(s) to group by.
        agg_dict: Dictionary of column names and aggregation functions.
        logger: Optional logger instance.

    Returns:
        Aggregated DataFrame.
    """
    try:
        agg_df = df.groupby(group_by).agg(agg_dict).reset_index()
        if logger:
            logger.info("Aggregated data grouped by %s. Result shape: %s", group_by, agg_df.shape)
        return agg_df
    except Exception as e:
        if logger:
            logger.error("Failed to aggregate data: %s", e)
        raise


def filter_dataframe(df: DataFrame, column: str, condition, logger: Optional[logging.Logger] = None) -> DataFrame:
    """
    Filter DataFrame based on column condition.

    Args:
        df: DataFrame to filter.
        column: Column name to filter on.
        condition: Condition or value to filter by.
        logger: Optional logger instance.

    Returns:
        Filtered DataFrame.
    """
    try:
        filtered_df = df[df[column] == condition]
        if logger:
            logger.info("Filtered %s on column '%s'. Result shape: %s", df.shape, column, filtered_df.shape)
        return filtered_df
    except Exception as e:
        if logger:
            logger.error("Failed to filter dataframe: %s", e)
        raise


def save_dataframe(df: DataFrame, output_path: Path, logger: Optional[logging.Logger] = None) -> bool:
    """
    Save DataFrame to CSV file.

    Args:
        df: DataFrame to save.
        output_path: Path where to save the CSV file.
        logger: Optional logger instance.

    Returns:
        True if successful, False otherwise.
    """
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False, encoding="utf-8")
        if logger:
            logger.info("Saved dataframe to %s. Shape: %s", output_path, df.shape)
        return True
    except Exception as e:
        if logger:
            logger.error("Failed to save dataframe: %s", e)
        return False


def get_summary_statistics(df: DataFrame, logger: Optional[logging.Logger] = None) -> dict:
    """
    Get summary statistics for numeric columns in DataFrame.

    Args:
        df: DataFrame to analyze.
        logger: Optional logger instance.

    Returns:
        Dictionary containing summary statistics.
    """
    try:
        summary = {
            "numeric_columns": df.select_dtypes(include=["number"]).columns.tolist(),
            "object_columns": df.select_dtypes(include=["object"]).columns.tolist(),
            "statistics": df.describe().to_dict(),
        }
        if logger:
            logger.info("Generated summary statistics for dataframe with shape %s", df.shape)
        return summary
    except Exception as e:
        if logger:
            logger.error("Failed to generate summary statistics: %s", e)
        return {}


def main() -> None:
    """Main execution function demonstrating data loading and transformation."""
    logger = setup_logger()
    logger.info("Starting dataframe operations")

    # Load latest data
    data = load_latest_data(logger)

    if not data:
        logger.warning("No data available for processing")
        return

    logger.info("Loaded %s dataframes", len(data))

    # Validate each dataframe
    for name, df in data.items():
        logger.info("Validating %s", name)
        validate_dataframe(df, logger)

    # Example: Clean one dataframe if available
    if "AdventureWorks_Calendar" in data:
        logger.info("Cleaning Calendar dataframe")
        cleaned = clean_dataframe(data["AdventureWorks_Calendar"], drop_nulls=True, logger=logger)
        logger.info("Cleaned dataframe shape: %s", cleaned.shape)

    logger.info("Dataframe operations completed")


if __name__ == "__main__":
    main()
