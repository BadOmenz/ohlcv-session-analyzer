"""
SESSION ASSIGNMENT MODULE

This module assigns each OHLCV row to a trading session and a session date.

Sessions:
- Asia:    18:00 – 02:00 (crosses midnight)
- Europe:  02:00 – 08:00
- New York: 08:00 – 16:00

Key challenge:
The Asia session spans two calendar days. Rows between 00:00–02:00 must be
assigned to the PREVIOUS session date.
"""

import pandas as pd


# ---------------------------------------------------------------------------
# SESSION CLASSIFICATION FUNCTION
#
# This function takes a timestamp and returns:
# - session_name
# - session_date
#
# The logic is explicitly written using hour-based conditions so it is
# transparent and easy to audit.
# ---------------------------------------------------------------------------

def get_session_info(ts: pd.Timestamp):
    hour = ts.hour

    # ---------------------------------------------------------------
    # ASIA SESSION (18:00 → 02:00)
    #
    # Two cases:
    # 1. 18:00–23:59 → same calendar day
    # 2. 00:00–01:59 → belongs to PREVIOUS day
    # ---------------------------------------------------------------

    if hour >= 18:
        return "asia", ts.date()

    elif hour < 2:
        return "asia", (ts - pd.Timedelta(days=1)).date()

    # ---------------------------------------------------------------
    # EUROPE SESSION (02:00 → 08:00)
    # ---------------------------------------------------------------

    elif 2 <= hour < 8:
        return "europe", ts.date()

    # ---------------------------------------------------------------
    # NEW YORK SESSION (08:00 → 16:00)
    # ---------------------------------------------------------------

    elif 8 <= hour < 16:
        return "ny", ts.date()

    # ---------------------------------------------------------------
    # OUTSIDE DEFINED SESSIONS
    #
    # This should not normally happen in futures data, but we handle it
    # explicitly to avoid silent errors.
    # ---------------------------------------------------------------

    else:
        return "unknown", ts.date()


# ---------------------------------------------------------------------------
# APPLY SESSION ASSIGNMENT TO DATAFRAME
#
# This function:
# - iterates over all timestamps
# - assigns session_name and session_date
# - returns updated DataFrame
#
# We use vectorized apply for clarity (not micro-optimized yet).
# ---------------------------------------------------------------------------

def assign_sessions(df: pd.DataFrame):
    session_data = df["timestamp"].apply(get_session_info)

    df["session_name"] = session_data.apply(lambda x: x[0])
    df["session_date"] = session_data.apply(lambda x: x[1])

    return df