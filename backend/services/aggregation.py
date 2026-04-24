"""
SESSION AGGREGATION MODULE

This module converts row-level OHLCV data into session-level summary rows.

Each output row represents one complete trading session, such as:
- Asia on 2026-01-29
- Europe on 2026-01-30
- New York on 2026-01-30

The aggregation step is where raw bars become analytical records.
"""

import pandas as pd


# ---------------------------------------------------------------------------
# SESSION AGGREGATION FUNCTION
#
# This function excludes "unknown" rows from analytical session statistics,
# then groups the remaining data by session_date and session_name.
#
# For each session group, it calculates:
# - open: first open of the session
# - high: highest high
# - low: lowest low
# - close: final close of the session
# - volume: total volume
# ---------------------------------------------------------------------------

def aggregate_sessions(df: pd.DataFrame):
    session_df = df[df["session_name"] != "unknown"].copy()

    grouped = (
        session_df
        .groupby(["session_date", "session_name"], as_index=False)
        .agg(
            open=("open", "first"),
            high=("high", "max"),
            low=("low", "min"),
            close=("close", "last"),
            volume=("volume", "sum"),
            bar_count=("timestamp", "count")
        )
    )

    # -----------------------------------------------------------------------
    # DERIVED SESSION METRICS
    #
    # These columns describe the behavior of each session after the basic OHLCV
    # values have been calculated.
    #
    # range: total high-low movement
    # net_change: close minus open
    # direction: up if close is above open, otherwise down
    # close_in_range_pct: where the close occurred inside the session range
    # -----------------------------------------------------------------------

    grouped["range"] = grouped["high"] - grouped["low"]
    grouped["net_change"] = grouped["close"] - grouped["open"]

    grouped["direction"] = grouped["net_change"].apply(
        lambda value: "up" if value > 0 else "down"
    )

    grouped["close_in_range_pct"] = grouped.apply(
        lambda row: 0 if row["range"] == 0 else round((row["close"] - row["low"]) / row["range"], 4),
        axis=1
    )

    return grouped