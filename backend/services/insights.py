"""
INSIGHT GENERATION MODULE

This module converts summary metrics into short, human-readable observations.

The insights are deterministic:
- no AI
- no prediction
- no hardcoded result text tied to a specific dataset

Each statement is based only on computed summary values.
"""


# ---------------------------------------------------------------------------
# MAIN INSIGHT FUNCTION
#
# This function receives the session summary dictionary created by summary.py.
#
# It compares Asia, Europe, and New York across several metrics:
# - average range
# - bullish percentage
# - ranging percentage
# - trending percentage
#
# The output is a short list of plain-English insight strings.
# ---------------------------------------------------------------------------

def generate_insights(summary: dict):
    insights = []

    # -----------------------------------------------------------------------
    # HIGHEST VOLATILITY SESSION
    #
    # Average range is used as the volatility proxy.
    # The session with the largest avg_range is described as having the
    # widest average movement.
    # -----------------------------------------------------------------------

    highest_range_session = max(
        summary,
        key=lambda session_name: summary[session_name]["avg_range"]
    )

    insights.append(
        f"{highest_range_session.upper()} has the highest average range, "
        f"with an average session range of {summary[highest_range_session]['avg_range']} points."
    )

    # -----------------------------------------------------------------------
    # STRONGEST BULLISH BIAS
    #
    # Percent bullish measures how often the session closed above its open.
    # The highest value identifies the session with the most frequent upside
    # close behavior.
    # -----------------------------------------------------------------------

    most_bullish_session = max(
        summary,
        key=lambda session_name: summary[session_name]["percent_bullish"]
    )

    insights.append(
        f"{most_bullish_session.upper()} shows the strongest bullish bias, "
        f"closing up in {round(summary[most_bullish_session]['percent_bullish'] * 100, 2)}% of sessions."
    )

    # -----------------------------------------------------------------------
    # MOST RANGING SESSION
    #
    # Percent ranging measures how often the session produced a low trend_ratio.
    # The highest value identifies the session most likely to rotate rather
    # than follow through directionally.
    # -----------------------------------------------------------------------

    most_ranging_session = max(
        summary,
        key=lambda session_name: summary[session_name]["percent_ranging"]
    )

    insights.append(
        f"{most_ranging_session.upper()} is the most frequently ranging session, "
        f"classified as ranging in {round(summary[most_ranging_session]['percent_ranging'] * 100, 2)}% of sessions."
    )

    # -----------------------------------------------------------------------
    # MOST TRENDING SESSION
    #
    # Percent trending measures how often the session had strong directional
    # follow-through relative to its own range.
    # -----------------------------------------------------------------------

    most_trending_session = max(
        summary,
        key=lambda session_name: summary[session_name]["percent_trending"]
    )

    insights.append(
        f"{most_trending_session.upper()} has the highest trending-session frequency, "
        f"classified as trending in {round(summary[most_trending_session]['percent_trending'] * 100, 2)}% of sessions."
    )

    return insights