"""
SESSION TYPE SUMMARY MODULE

This module aggregates all classified sessions into summary statistics
by session type:

- asia
- europe
- ny

Unlike earlier steps, this does NOT operate at the individual session level.
Instead, it summarizes the entire dataset to answer questions like:

- Which session has the highest average range?
- Which session trends the most?
- Which session is most often ranging?

This is the layer that feeds both:
- the summary UI
- the insight generation
"""

import pandas as pd


# ---------------------------------------------------------------------------
# MAIN SUMMARY FUNCTION
#
# This function receives the classified session DataFrame and produces
# aggregated statistics grouped by session_name.
#
# It returns a dictionary structured for direct API output.
# ---------------------------------------------------------------------------

def build_session_summary(sessions: pd.DataFrame):
    summary = {}

    grouped = sessions.groupby("session_name")

    for session_name, group in grouped:
        total_sessions = len(group)

        # -------------------------------------------------------------------
        # CORE METRICS
        # -------------------------------------------------------------------

        avg_range = round(group["range"].mean(), 2)
        avg_net_change = round(group["net_change"].mean(), 2)
        avg_close_in_range = round(group["close_in_range_pct"].mean(), 4)

        # -------------------------------------------------------------------
        # DIRECTIONAL STATS
        # -------------------------------------------------------------------

        bullish_pct = round((group["direction"] == "up").mean(), 4)
        bearish_pct = round((group["direction"] == "down").mean(), 4)

        # -------------------------------------------------------------------
        # BEHAVIOR CLASSIFICATION STATS
        # -------------------------------------------------------------------

        ranging_pct = round((group["classification"] == "ranging").mean(), 4)
        trending_pct = round((group["classification"] == "trending").mean(), 4)
        neutral_pct = round((group["classification"] == "neutral").mean(), 4)

        # -------------------------------------------------------------------
        # BUILD SUMMARY ENTRY
        # -------------------------------------------------------------------

        summary[session_name] = {
            "total_sessions": total_sessions,
            "avg_range": avg_range,
            "avg_net_change": avg_net_change,
            "avg_close_in_range_pct": avg_close_in_range,
            "percent_bullish": bullish_pct,
            "percent_bearish": bearish_pct,
            "percent_trending": trending_pct,
            "percent_ranging": ranging_pct,
            "percent_neutral": neutral_pct
        }

    return summary