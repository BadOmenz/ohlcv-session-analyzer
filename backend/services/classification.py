"""
SESSION CLASSIFICATION MODULE

This module adds behavior labels to each aggregated session.

The classification is based on how much of the session's total range was
captured by the net open-to-close move.

A session with a large net move compared to its full range is considered
directional. A session with a small net move compared to its full range is
considered ranging.
"""

import pandas as pd


# ---------------------------------------------------------------------------
# CLASSIFICATION CONSTANTS
#
# These thresholds define how session behavior is categorized.
#
# trend_ratio = abs(net_change) / range
#
# - above 0.6 means the session had strong directional follow-through
# - below 0.3 means the session moved around but closed near its open
# - everything between those values is treated as neutral
# ---------------------------------------------------------------------------

TRENDING_THRESHOLD = 0.6
RANGING_THRESHOLD = 0.3


# ---------------------------------------------------------------------------
# MAIN CLASSIFICATION FUNCTION
#
# This function receives the session-level DataFrame produced by aggregation.
#
# It adds:
# - trend_ratio
# - classification
#
# The function copies the DataFrame first so it does not unexpectedly mutate
# the original object passed in from another part of the pipeline.
# ---------------------------------------------------------------------------

def classify_sessions(sessions: pd.DataFrame):
    sessions = sessions.copy()

    # -----------------------------------------------------------------------
    # TREND RATIO CALCULATION
    #
    # trend_ratio measures how directional the session was.
    #
    # Example:
    # - range = 100
    # - net_change = 75
    # - trend_ratio = 0.75
    #
    # That means 75% of the full high-low range was captured by the
    # open-to-close movement.
    # -----------------------------------------------------------------------

    sessions["trend_ratio"] = sessions.apply(
        lambda row: 0 if row["range"] == 0 else round(abs(row["net_change"]) / row["range"], 4),
        axis=1
    )

    # -----------------------------------------------------------------------
    # BEHAVIOR CLASSIFICATION
    #
    # This converts the numeric trend_ratio into a simple descriptive label.
    #
    # The label is intentionally simple because it will be used later in:
    # - session tables
    # - weekly summaries
    # - generated insight text
    # -----------------------------------------------------------------------

    def classify_row(row):
        if row["trend_ratio"] > TRENDING_THRESHOLD:
            return "trending"

        if row["trend_ratio"] < RANGING_THRESHOLD:
            return "ranging"

        return "neutral"

    sessions["classification"] = sessions.apply(classify_row, axis=1)

    return sessions