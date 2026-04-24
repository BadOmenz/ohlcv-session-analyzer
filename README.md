# OHLCV Session Analyzer

A full-stack web application that analyzes intraday OHLCV data by trading session, computes session-level metrics, classifies behavior, and visualizes results with an interactive chart.

---

## Overview

This project demonstrates a complete data pipeline:

- CSV ingestion and validation
- Session segmentation, including midnight-crossing logic
- Session-level aggregation and derived metrics
- Behavioral classification
- Summary statistics across session types
- Deterministic insight generation
- Interactive frontend visualization

---

## Tech Stack

### Frontend

- React with Vite
- TypeScript
- Axios
- Recharts

### Backend

- FastAPI
- Python
- Pandas

---

## Features

### File Upload

- Accepts CSV files containing OHLCV data
- Validates required columns and structure

### Session Segmentation

Data is segmented into:

- Asia: 18:00 to 02:00
- Europe: 02:00 to 08:00
- New York: 08:00 to 16:00

The Asia session crosses midnight, so rows after midnight are assigned to the previous session date.

### Session Metrics

For each session:

- Open, high, low, close
- Range
- Net change
- Volume
- Close position within range

### Behavioral Classification

Each session is classified using:

```text
trend_ratio = abs(net_change) / range
```

Classification rules:

- Trending: greater than 0.6
- Ranging: less than 0.3
- Neutral: otherwise

### Interactive Chart

- Session-colored price chart
- Asia = blue
- Europe = green
- New York = yellow
- Tooltip with formatted timestamp and session
- Zoom and pan using Recharts Brush

---

## Project Structure

```text
project03_ohlcv_session_analyzer/
│
├── backend/
│   ├── main.py
│   └── services/
│       ├── validation.py
│       ├── sessions.py
│       ├── aggregation.py
│       ├── classification.py
│       ├── summary.py
│       └── insights.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.tsx
│   │   │   └── PriceChart.tsx
│   │   └── services/
│   │       └── api.ts
│
├── sample_data/
│   └── sample_data_mes15m.csv
│
└── README.md
```

---

## How to Run

### 1. Clone the repository

```powershell
git clone https://github.com/BadOmenz/ohlcv-session-analyzer.git
cd ohlcv-session-analyzer
```

### 2. Run Backend

```powershell
cd backend
py -m venv venv
.\venv\Scripts\activate
pip install fastapi uvicorn python-multipart pandas
python -m uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

### 3. Run Frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

### 4. Test the Application

A sample dataset is included:

```text
sample_data/mes_15m_sample.csv
```

Upload that file in the UI to test the application.

---

## API

### POST /analyze

Accepts a CSV file with this format:

```csv
<Date>, <Time>, <Open>, <High>, <Low>, <Close>, <Volume>
1/29/2026,17:15:00,7041.25,7044.25,7023.50,7024.00,9681
```

Returns:

- sessions
- summary
- insights
- chart_data

---

## Design Notes

This project emphasizes:

- clear separation of concerns
- deterministic logic with no machine learning
- explicit data transformations
- explainable metrics
- rapid prototyping using AI-assisted development

---

## Future Enhancements

- Session-isolated chart mode
- Normalized session performance visualization
- Downloadable analysis report
- Multi-file comparison

---

## Author

David Folkerth  
Ottawa, Canada

Built as part of a portfolio demonstrating full-stack development, data processing, and analytical system design.