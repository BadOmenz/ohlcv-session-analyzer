"""
VALIDATION MODULE

This module is responsible for validating the structure and integrity of the
incoming OHLCV dataset before any analytical processing occurs.

The validation layer ensures:
- required columns exist
- timestamp is valid
- data is sorted correctly
- no duplicate timestamps exist
- numeric fields are valid

This prevents downstream logic from operating on corrupted or malformed data.
"""

import pandas as pd


# ---------------------------------------------------------------------------
# REQUIRED COLUMN DEFINITIONS
#
# This section defines the exact set of columns that must exist in the dataset
# after normalization. These names must match the output from the parsing step.
# ---------------------------------------------------------------------------

REQUIRED_COLUMNS = {
    "date",
    "time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "timestamp"
}


# ---------------------------------------------------------------------------
# MAIN VALIDATION FUNCTION
#
# This function takes a pandas DataFrame and performs a series of structural
# and data integrity checks. Instead of raising exceptions immediately, it
# collects all validation errors and returns them as a list.
#
# This allows the API to return user-friendly validation feedback instead of
# crashing on the first issue.
# ---------------------------------------------------------------------------

def validate_ohlcv_dataframe(df: pd.DataFrame):
    errors = []

    # -----------------------------------------------------------------------
    # COLUMN EXISTENCE CHECK
    #
    # Ensures that all required columns are present after normalization.
    # -----------------------------------------------------------------------

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        errors.append(f"Missing columns: {list(missing_columns)}")


    # -----------------------------------------------------------------------
    # TIMESTAMP VALIDITY CHECK
    #
    # Ensures that the timestamp column is a valid datetime type.
    # -----------------------------------------------------------------------

    if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        errors.append("Timestamp column is not a valid datetime type")


    # -----------------------------------------------------------------------
    # SORT ORDER CHECK
    #
    # Ensures timestamps are strictly increasing (ascending).
    # -----------------------------------------------------------------------

    if not df["timestamp"].is_monotonic_increasing:
        errors.append("Timestamps are not sorted in ascending order")


    # -----------------------------------------------------------------------
    # DUPLICATE TIMESTAMP CHECK
    #
    # Detects duplicate timestamps, which would break session logic.
    # -----------------------------------------------------------------------

    if df["timestamp"].duplicated().any():
        errors.append("Duplicate timestamps found")


    # -----------------------------------------------------------------------
    # NUMERIC FIELD VALIDATION
    #
    # Ensures OHLCV fields are numeric.
    # -----------------------------------------------------------------------

    numeric_fields = ["open", "high", "low", "close", "volume"]

    for col in numeric_fields:
        if not pd.api.types.is_numeric_dtype(df[col]):
            errors.append(f"Column '{col}' is not numeric")


    # -----------------------------------------------------------------------
    # RESULT
    #
    # Returns a list of errors. If empty, validation passed.
    # -----------------------------------------------------------------------

    return errors