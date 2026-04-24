# OHLCV Session Analyzer

A full-stack web application that analyzes intraday OHLCV data by trading session (Asia, Europe, New York), computes session-level metrics, classifies behavior, and visualizes results with an interactive chart.

---

## Overview

This project demonstrates a complete data pipeline:

- CSV ingestion and validation
- Session segmentation (including midnight-crossing logic)
- Session-level aggregation and derived metrics
- Behavioral classification (trending / ranging / neutral)
- Summary statistics across session types
- Deterministic insight generation
- Interactive frontend visualization

---

## Tech Stack

### Frontend
- React (Vite)
- TypeScript
- Axios
- Recharts

### Backend
- FastAPI
- Python
- Pandas

---

## Features

### 1. File Upload
- Accepts CSV files containing OHLCV data
- Validates required columns and structure

### 2. Session Segmentation

Data is segmented into:

- Asia: 18:00 – 02:00 (crosses midnight)
- Europe: 02:00 – 08:00
- New York: 08:00 – 16:00

Includes correct handling of session dates for overnight sessions.

---

### 3. Session Metrics

For each session:

- Open, High, Low, Close
- Range (high - low)
- Net Change (close - open)
- Volume
- Close position within range

---

### 4. Behavioral Classification

Each session is classified using:


trend_ratio = abs(net_change) / range


- Trending: > 0.6
- Ranging: < 0.3
- Neutral: otherwise

---

### 5. Summary Statistics

Aggregated by session type:

- Average range
- Average net move
- % bullish / bearish
- % trending / ranging / neutral

---

### 6. Insight Generation

Automatically generates observations such as:

- Highest volatility session
- Strongest directional bias
- Most ranging session
- Most trending session

---

### 7. Interactive Chart

- Line chart of price over time
- Session-colored segments:
  - Asia = blue
  - Europe = green
  - New York = yellow
- Tooltip with formatted timestamp and session
- Zoom and pan using Recharts Brush

---

## Example Insight

> "New York has the highest average range, indicating the greatest volatility across sessions."

---

## Project Structure


project03_ohlcv_session_analyzer/
│
├── backend/
│ ├── main.py
│ └── services/
│ ├── validation.py
│ ├── sessions.py
│ ├── aggregation.py
│ ├── classification.py
│ ├── summary.py
│ └── insights.py
│
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ │ ├── FileUpload.tsx
│ │ │ └── PriceChart.tsx
│ │ └── services/
│ │ └── api.ts
│
└── README.md


---

## How to Run

### Backend

```powershell
cd backend
.\venv\Scripts\activate
python -m uvicorn main:app --reload
Frontend
cd frontend
npm install
npm run dev
API
POST /analyze

Upload a CSV file in format:  
<Date>, <Time>, <Open>, <High>, <Low>, <Close>, <Volume>
1/29/2026,17:15:00,7041.25,7044.25,7023.50,7024.00,9681


Returns:

sessions
summary
insights
chart_data
Design Notes

This project emphasizes:

clear separation of concerns
deterministic logic (no machine learning)
explicit data transformations
explainable metrics
rapid prototyping using AI-assisted development
Future Enhancements
Session-isolated chart mode (stitching sessions together)
Normalized session performance visualization
Downloadable analysis report
Multi-file comparison
Author: David Folkerth, Ottawa, Canada

Built as part of a portfolio demonstrating full-stack development, data processing, and analytical system design.