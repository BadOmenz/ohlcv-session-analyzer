"""
OHLCV Session Analyzer — Backend Entry Point

This file defines the FastAPI application and the initial /analyze endpoint.
At this stage, the goal is not to perform any data processing yet, but to:

1. Prove that the API server runs correctly
2. Accept a CSV file upload
3. Return a basic confirmation response

Later, this file will orchestrate the full processing pipeline by calling
separate service modules (validation, session assignment, aggregation, etc.).
"""

from fastapi import FastAPI, UploadFile, File
from services.validation import validate_ohlcv_dataframe
from services.sessions import assign_sessions
from services.aggregation import aggregate_sessions
from services.classification import classify_sessions
from services.summary import build_session_summary
from services.insights import generate_insights
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------------------------------------
# APPLICATION INITIALIZATION
#
# This section creates and configures the FastAPI application instance.
#
# The FastAPI object (`app`) is the central registry for:
# - API routes (endpoints)
# - automatic OpenAPI documentation (/docs)
# - request/response handling
#
# At this stage, we are not connecting to any database or external system.
# This project is intentionally designed as a stateless, file-based processor:
# input = CSV file, output = computed JSON.
# ---------------------------------------------------------------------------

app = FastAPI(
    title="OHLCV Session Analyzer",
    description="Session-based analysis of intraday OHLCV data",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# HEALTH CHECK ENDPOINT
#
# This is a minimal endpoint used to verify that the API is running.
#
# It does not depend on file uploads, pandas, or any processing logic.
# If this endpoint works, it confirms:
# - FastAPI is initialized correctly
# - Uvicorn is serving requests
#
# This is useful for debugging before introducing more complex logic.
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "API is running"
    }


# ---------------------------------------------------------------------------
# ANALYZE ENDPOINT (INITIAL VERSION)
#
# This endpoint will eventually:
# - accept a CSV file
# - validate its structure
# - assign trading sessions
# - compute session statistics
# - classify behavior (trend/range)
# - generate summary metrics and insights
# - return chart-ready data
#
# For this first step, it ONLY:
# - receives the uploaded file
# - reads it into memory
# - returns basic metadata
#
# This isolates file upload handling before introducing pandas or logic.
# ---------------------------------------------------------------------------

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # -----------------------------------------------------------------------
    # FILE INGESTION AND CSV PARSING
    #
    # This section reads the uploaded file and converts it into a pandas
    # DataFrame. The raw file arrives as bytes, so we decode it into a string
    # and wrap it in a StringIO object so pandas can treat it like a file.
    #
    # This step is critical because ALL downstream processing depends on having
    # a correctly structured DataFrame.
    # -----------------------------------------------------------------------

    import pandas as pd
    from io import StringIO

    file_content = await file.read()
    decoded = file_content.decode("utf-8")

    df = pd.read_csv(StringIO(decoded))


    # -----------------------------------------------------------------------
    # COLUMN NORMALIZATION
    #
    # The input CSV contains column names like:
    # "<Date>", "<Time>", "<Open>", etc.
    #
    # We:
    # - remove angle brackets
    # - strip whitespace
    # - convert to lowercase
    #
    # This ensures consistent internal naming across all datasets.
    # -----------------------------------------------------------------------

    df.columns = (
        df.columns
        .str.replace("<", "", regex=False)
        .str.replace(">", "", regex=False)
        .str.strip()
        .str.lower()
    )


    # -----------------------------------------------------------------------
    # TIMESTAMP CONSTRUCTION
    #
    # The dataset provides separate 'date' and 'time' columns.
    #
    # We combine them into a single 'timestamp' column, which will be used
    # for:
    # - sorting
    # - session assignment
    # - charting
    #
    # After construction, we convert it to pandas datetime type.
    # -----------------------------------------------------------------------

    df["timestamp"] = pd.to_datetime(df["date"] + " " + df["time"])


    # -----------------------------------------------------------------------
    # BASIC STRUCTURE CHECK (TEMPORARY)
    #
    # For now, we return:
    # - column names
    # - first 5 rows
    #
    # This allows us to confirm parsing is correct before moving into
    # validation logic.
    # -----------------------------------------------------------------------

    validation_errors = validate_ohlcv_dataframe(df)

    if validation_errors:
        return {
            "status": "validation_failed",
            "errors": validation_errors
        }
    
    df =  assign_sessions(df)
    sessions = aggregate_sessions(df)
    sessions = classify_sessions(sessions)
    summary = build_session_summary(sessions)
    insights = generate_insights(summary)

    return {
    "sessions": sessions.to_dict(orient="records"),
    "summary": summary,
    "insights": insights,
    "chart_data": df[["timestamp", "close", "session_name"]]
        .rename(columns={"session_name": "session"})
        .to_dict(orient="records")
}