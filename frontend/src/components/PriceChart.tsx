import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  Brush,
  ResponsiveContainer,
} from "recharts";

/*
PRICE CHART WITH SESSION COLORING

This version:
- splits data into 3 series (asia, europe, ny)
- each line only renders when its session matches
- creates visual color segmentation across time
*/

function PriceChart({ data }: { data: any[] }) {
  // ---------------------------------------------------------
  // PREPARE DATA SERIES
  //
  // Each row keeps only one value depending on session.
  // Others are set to null so Recharts breaks the line.
  // ---------------------------------------------------------

  const chartData = data.map((row) => ({
    timestamp: row.timestamp,
    session: row.session,

    asia: row.session === "asia" ? row.close : null,
    europe: row.session === "europe" ? row.close : null,
    ny: row.session === "ny" ? row.close : null,
  }));

  // ---------------------------------------------------------
// FORMAT TIMESTAMP
//
// Converts ISO timestamp into readable format
// Example: 2026-02-02T10:30:00 → Feb 2, 10:30
// ---------------------------------------------------------

function formatTimestamp(ts: string) {
  const date = new Date(ts);

  return date.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
}

  // ---------------------------------------------------------
// CUSTOM TOOLTIP
//
// Shows clean timestamp, session, and price
// ---------------------------------------------------------

function CustomTooltip({ active, payload }: any) {
  if (!active || !payload || payload.length === 0) return null;

  const point = payload.find((p: any) => p.value !== null);

  if (!point) return null;

  const { payload: row } = point;

  return (
    <div
      style={{
        background: "#111",
        color: "#fff",
        padding: "10px",
        borderRadius: "6px",
        fontSize: "12px",
      }}
    >
      <div>{formatTimestamp(row.timestamp)}</div>
      <div style={{ textTransform: "uppercase" }}>
        {row.session}
      </div>
      <div>Close: {point.value}</div>
    </div>
  );
}

  return (
  <div style={{ marginTop: "30px", textAlign: "center" }}>
    <h3>Price by Session</h3>

    <div style={{ width: "100%", height: "400px", marginTop: "10px" }}>
      <ResponsiveContainer>
        <LineChart data={chartData}>
          <XAxis dataKey="timestamp" hide />
          <YAxis domain={["auto", "auto"]} />
          <Tooltip content={<CustomTooltip />} />
          <Legend />

          {/* Asia */}
          <Line
            type="monotone"
            dataKey="asia"
            stroke="#3b82f6"
            dot={false}
            isAnimationActive={false}
          />

          {/* Europe */}
          <Line
            type="monotone"
            dataKey="europe"
            stroke="#22c55e"
            dot={false}
            isAnimationActive={false}
          />

          {/* New York */}
          <Line
            type="monotone"
            dataKey="ny"
            stroke="#eab308"
            dot={false}
            isAnimationActive={false}
          />

          <Brush
            dataKey="timestamp"
            height={30}
            stroke="#888"
            tickFormatter={formatTimestamp}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  </div>
);
}

export default PriceChart;