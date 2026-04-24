import { useState } from "react";
import { analyzeOhlcvFile } from "../services/api";
import PriceChart from "./PriceChart";

/*
FILE UPLOAD COMPONENT

This component handles the first major frontend workflow:
select a CSV file, send it to the FastAPI backend, store the returned
analysis result, and render the first visible analysis outputs.

For now, this component displays:
- upload controls
- result counts
- generated insights
- session summary cards
*/

function FileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  // ---------------------------------------------------------
  // HANDLE FILE SELECTION
  //
  // Stores the selected CSV file in React state.
  // ---------------------------------------------------------
  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  }

  // ---------------------------------------------------------
  // HANDLE UPLOAD CLICK
  //
  // Sends the selected CSV file to the backend and stores the
  // returned analysis result so the UI can render it.
  // ---------------------------------------------------------
  async function handleUpload() {
    if (!file) {
      alert("Please select a file first");
      return;
    }

    const result = await analyzeOhlcvFile(file);
    setAnalysisResult(result);
    console.log("Analysis result:", result);
  }

  return (
    <div style={{ marginTop: "20px" }}>
      {/* Upload controls */}
      <div style={{ textAlign: "center" }}>
        <div style={{ display: "inline-block" }}>
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            style={{ marginRight: "10px" }}
          />

          <button onClick={handleUpload}>Upload</button>
        </div>
      </div>

      {/* Analysis result area */}
      {analysisResult && (
        <div style={{ marginTop: "20px", textAlign: "center" }}>
          <p>Analysis complete.</p>
          <p>Sessions: {analysisResult.sessions.length}</p>
          <p>Chart rows: {analysisResult.chart_data.length}</p>

          {/* Price chart */}
          <PriceChart data={analysisResult.chart_data} />

          {/* Insights panel */}
          <div style={{ marginTop: "20px" }}>
            <h3>Insights</h3>

            <ul style={{ listStyle: "none", padding: 0 }}>
              {analysisResult.insights.map((insight: string, index: number) => (
                <li key={index} style={{ marginBottom: "8px" }}>
                  {insight}
                </li>
              ))}
            </ul>
          </div>

          {/* Session summary cards */}
          <div style={{ marginTop: "30px" }}>
            <h3>Session Summary</h3>

            <div
              style={{
                display: "flex",
                justifyContent: "center",
                gap: "20px",
                flexWrap: "wrap",
                marginTop: "10px",
              }}
            >
              {Object.entries(analysisResult.summary).map(
                ([sessionName, data]: any) => (
                  <div
                    key={sessionName}
                    style={{
                      border: "1px solid #ccc",
                      borderRadius: "8px",
                      padding: "15px",
                      width: "250px",
                      textAlign: "left",
                    }}
                  >
                    <h4
                        style={{
                            textTransform: "uppercase",
                            color:
                            sessionName === "asia"
                                ? "#3b82f6"
                                : sessionName === "europe"
                                ? "#22c55e"
                                : "#eab308",
                        }}
                        >
                        {sessionName}
                        </h4>

                    <p>Avg Range: {data.avg_range}</p>
                    <p>Avg Session Net: {data.avg_net_change}</p>
                    <p>Bullish: {(data.percent_bullish * 100).toFixed(1)}%</p>
                    <p>Ranging: {(data.percent_ranging * 100).toFixed(1)}%</p>
                    <p>Trending: {(data.percent_trending * 100).toFixed(1)}%</p>
                  </div>
                )
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default FileUpload;