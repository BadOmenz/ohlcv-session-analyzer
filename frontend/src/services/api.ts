import axios from "axios";

/*
API SERVICE MODULE

This file contains frontend functions that communicate with the FastAPI backend.

Keeping API calls in a separate service file helps keep React components focused
on UI behavior instead of HTTP request details.
*/

const API_BASE_URL = "http://127.0.0.1:8000";

// ---------------------------------------------------------
// ANALYZE OHLCV FILE
//
// Sends one uploaded CSV file to the backend /analyze endpoint.
// The file is wrapped in FormData because FastAPI expects multipart upload.
// ---------------------------------------------------------

export async function analyzeOhlcvFile(file: File) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await axios.post(`${API_BASE_URL}/analyze`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}