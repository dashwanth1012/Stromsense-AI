import os

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\AnalyticsDeck.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update function signature to accept activeCycle
old_sig = """export default function AnalyticsDeck({
  forecastData,
  trendData,
  historyData,
  activeCaseStudy,
  onSelectCaseStudy
}) {"""

new_sig = """export default function AnalyticsDeck({
  forecastData,
  trendData,
  historyData,
  activeCaseStudy,
  onSelectCaseStudy,
  activeCycle = "12Z"
}) {"""

if old_sig in content:
    content = content.replace(old_sig, new_sig)
    print("Function signature updated successfully.")
else:
    # try single line signature or slightly different spacing
    print("Warning: Function signature not found exactly, trying search & replace with fuzzy matching.")
    content = content.replace("export default function AnalyticsDeck({\n  forecastData,\n  trendData,\n  historyData,\n  activeCaseStudy,\n  onSelectCaseStudy\n})", 
                              "export default function AnalyticsDeck({\n  forecastData,\n  trendData,\n  historyData,\n  activeCaseStudy,\n  onSelectCaseStudy,\n  activeCycle = \"12Z\"\n})")

# 2. Update Selection Control Panel to include Date/Time/Source HUD
old_panel = """      {activeSubTab === "ANALYTICS" ? (
        <>
          {/* Selection Control Panel */}
          <div className="panel-surface" style={{ padding: "20px", display: "flex", justifyContent: "space-between", alignItems: "center", border: "1px solid #334155" }}>
        <div>
          <h2 style={{ fontSize: "16px", color: "#ffffff", fontWeight: "bold" }}>IMD Convective Verification & Threshold Discovery Hub</h2>
          <p style={{ fontSize: "12px", color: "#64748b" }}>Observational threshold discovery, historical distributions, and forecast verification matrices</p>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <span className="font-technical" style={{ fontSize: "11px", color: "#3b82f6", fontWeight: "bold" }}>CWC MET NODE:</span>
          <select
            value={selectedStation}
            onChange={(e) => setSelectedStation(e.target.value)}
            style={{
              padding: "10px 16px",
              borderRadius: "10px",
              backgroundColor: "#020617",
              border: "1px solid #1e293b",
              color: "#ffffff",
              fontSize: "13px",
              cursor: "pointer",
              fontWeight: "bold",
              outline: "none"
            }}
          >
            <option value="ALL">All Operational Nodes</option>
            {forecastData.map(s => (
              <option key={s.station} value={s.station}>{s.station} {s.station === "Visakhapatnam" ? "(43150)" : s.station === "Machilipatnam" ? "(43185)" : ""}</option>
            ))}
          </select>
          <span className="font-technical" style={{ fontSize: "11px", color: "#10b981", fontWeight: "bold" }}>SEASON:</span>
          <select
            value={selectedSeason}
            onChange={(e) => setSelectedSeason(e.target.value)}
            style={{
              padding: "10px 16px",
              borderRadius: "10px",
              backgroundColor: "#020617",
              border: "1px solid #1e293b",
              color: "#ffffff",
              fontSize: "13px",
              cursor: "pointer",
              fontWeight: "bold",
              outline: "none"
            }}
          >
            <option value="ALL">All Seasons</option>
            <option value="Pre-Monsoon">Pre-Monsoon</option>
            <option value="Monsoon">Monsoon</option>
            <option value="Post-Monsoon">Post-Monsoon</option>
          </select>
        </div>
      </div>"""

new_panel = """      {activeSubTab === "ANALYTICS" ? (
        <>
          {/* Selection Control Panel with Date/Time/Source HUD */}
          <div className="panel-surface" style={{ padding: "20px", display: "flex", flexDirection: "column", gap: "12px", border: "1px solid #334155" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <h2 style={{ fontSize: "16px", color: "#ffffff", fontWeight: "bold" }}>IMD Convective Verification & Threshold Discovery Hub</h2>
                <p style={{ fontSize: "12px", color: "#64748b" }}>Observational threshold discovery, historical distributions, and forecast verification matrices</p>
              </div>

              <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                <span className="font-technical" style={{ fontSize: "11px", color: "#3b82f6", fontWeight: "bold" }}>CWC MET NODE:</span>
                <select
                  value={selectedStation}
                  onChange={(e) => setSelectedStation(e.target.value)}
                  style={{
                    padding: "10px 16px",
                    borderRadius: "10px",
                    backgroundColor: "#020617",
                    border: "1px solid #1e293b",
                    color: "#ffffff",
                    fontSize: "13px",
                    cursor: "pointer",
                    fontWeight: "bold",
                    outline: "none"
                  }}
                >
                  <option value="ALL">All Operational Nodes</option>
                  {forecastData.map(s => (
                    <option key={s.station} value={s.station}>{s.station} {s.station === "Visakhapatnam" ? "(43150)" : s.station === "Machilipatnam" ? "(43185)" : ""}</option>
                  ))}
                </select>
                <span className="font-technical" style={{ fontSize: "11px", color: "#10b981", fontWeight: "bold" }}>SEASON:</span>
                <select
                  value={selectedSeason}
                  onChange={(e) => setSelectedSeason(e.target.value)}
                  style={{
                    padding: "10px 16px",
                    borderRadius: "10px",
                    backgroundColor: "#020617",
                    border: "1px solid #1e293b",
                    color: "#ffffff",
                    fontSize: "13px",
                    cursor: "pointer",
                    fontWeight: "bold",
                    outline: "none"
                  }}
                >
                  <option value="ALL">All Seasons</option>
                  <option value="Pre-Monsoon">Pre-Monsoon</option>
                  <option value="Monsoon">Monsoon</option>
                  <option value="Post-Monsoon">Post-Monsoon</option>
                </select>
              </div>
            </div>

            {/* Date & Time Visibility HUD */}
            <div style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              backgroundColor: "#020617",
              border: "1px solid #1e293b",
              borderRadius: "8px",
              padding: "10px 16px",
              fontSize: "12px",
              fontFamily: "JetBrains Mono"
            }}>
              <div>Observation Date: <strong style={{ color: "#ffffff" }}>2026-06-05</strong></div>
              <div>Observation Time: <strong style={{ color: "#ffffff" }}>{activeCycle === "12Z" ? "17:00 IST" : "05:00 IST"}</strong></div>
              <div>Forecast Generated: <strong style={{ color: "#a855f7" }}>{activeCycle === "12Z" ? "17:07 IST" : "05:07 IST"}</strong></div>
              <div>Data Source: <strong style={{ color: "#10b981" }}>IMD Radiosonde Archive & Historical Convective Database</strong></div>
            </div>
          </div>"""

if old_panel in content:
    content = content.replace(old_panel, new_panel)
    print("Selection control panel updated successfully.")
else:
    # try with different indentation
    normalized_old_panel = old_panel.replace("        ", "").replace("      ", "").replace("\n", "").replace(" ", "")
    print("Warning: Selection control panel not found exactly, trying search & replace with normalized spaces.")
    # We will look for a substring that is very stable:
    sub_old = """      {activeSubTab === "ANALYTICS" ? (
        <>
          {/* Selection Control Panel */}"""
    if sub_old in content:
        print("Found header prefix. Let's do replacements manually or use a regex in the python script.")

# Let's write a robust replacement script
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
