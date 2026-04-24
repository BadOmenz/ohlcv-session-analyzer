import FileUpload from "./components/FileUpload";

function App() {
  return (
    <main
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "10px",
        padding: "40px 20px",
      }}
    >
      <div style={{ width: "100%", maxWidth: "1000px", textAlign: "center" }}>
        <h1>OHLCV Session Analyzer</h1>
        <p>Upload intraday OHLCV data to analyze sessions.</p>

        <FileUpload />
      </div>
    </main>
  );
}

export default App;