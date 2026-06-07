import os

ops_path = "frontend/src/components/modules/Phase3OpsModule.jsx"

with open(ops_path, "r", encoding="utf-8") as f:
    content = f.read()

# Locate LEVEL 2 - EXPANDABLE DIAGNOSTICS in Phase3OpsModule.jsx
target_start = content.find('{/* LEVEL 2 — EXPANDABLE DIAGNOSTICS */}')
if target_start == -1:
    print("Could not find Level 2 diagnostics block start!")
    exit(1)

# Find the end of the diagnostics block
# It ends at the next Level 3 review mode comment or similar
target_end = content.find('{/* LEVEL 3 — IMD REVIEW MODE: Complete Engineering Diagnostics */}', target_start)
if target_end == -1:
    print("Could not find Level 3 diagnostics block start!")
    exit(1)

# Let's inspect the target block
target_block = content[target_start:target_end]
print(f"Diagnostics block length: {len(target_block)}")

# Let's design the replacement block incorporating the LIVE CAPE AUDIT ENGINE
replacement_block = """{/* LEVEL 2 — EXPANDABLE DIAGNOSTICS */}
            {(showDiagnostics || reviewMode) && (
              <div style={{
                backgroundColor: "#020617",
                border: "1px solid #334155",
                borderRadius: "10px",
                padding: "14px",
                marginBottom: "12px",
                fontFamily: "JetBrains Mono",
                fontSize: "11px",
                color: "#cbd5e1"
              }}>
                <div style={{ borderBottom: "1px solid #1e293b", paddingBottom: "6px", marginBottom: "8px", color: "#eab308", fontWeight: "bold" }}>
                  ● LIVE CAPE AUDIT ENGINE & DIAGNOSTICS
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px", marginBottom: "12px", borderBottom: "1px solid #1e293b", paddingBottom: "10px" }}>
                  <div>Current CAPE: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{stationTrace?.timeline?.[0]?.cape !== undefined ? `${stationTrace.timeline[0].cape} J/kg` : "N/A"}</span></div>
                  <div>Previous CAPE: <span style={{ color: "#ffffff" }}>{stationTrace?.timeline?.[0]?.previous_cape !== undefined ? `${stationTrace.timeline[0].previous_cape} J/kg` : "N/A"}</span></div>
                  <div>Delta CAPE: <span style={{ 
                    color: (stationTrace?.timeline?.[0]?.delta_cape || 0) === 0 ? "#64748b" : (stationTrace?.timeline?.[0]?.delta_cape || 0) > 0 ? "#10b981" : "#ef4444",
                    fontWeight: "bold"
                  }}>{stationTrace?.timeline?.[0]?.delta_cape !== undefined ? `${stationTrace.timeline[0].delta_cape} J/kg` : "N/A"}</span></div>
                  <div>CAPE Trend: <span style={{ 
                    color: (stationTrace?.timeline?.[0]?.delta_cape || 0) === 0 ? "#64748b" : (stationTrace?.timeline?.[0]?.delta_cape || 0) > 0 ? "#10b981" : "#ef4444",
                    fontWeight: "bold"
                  }}>
                    {(stationTrace?.timeline?.[0]?.delta_cape || 0) > 0 ? "📈 RISING" : (stationTrace?.timeline?.[0]?.delta_cape || 0) < 0 ? "📉 FALLING" : "➡️ STEADY"}
                  </span></div>
                  <div>Expected Range: <span style={{ color: "#94a3b8" }}>{selectedStationName === "Visakhapatnam" ? "1000 - 4500 J/kg" : "500 - 3500 J/kg"}</span></div>
                  <div>Wyoming Source Ingest: <span style={{ color: "#ffffff" }}>{stationTrace?.source_type || "N/A"}</span></div>
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", lineHeight: "1.6" }}>
                  <div>Cache Age: <span style={{ color: "#ffffff" }}>{stationTrace?.cache_age || "N/A"} ({stationTrace?.cache_age_hours || 0.0}h)</span></div>
                  <div>Ingestion Status: <span style={{ color: "#ffffff" }}>{stationTrace?.source_status === "LIVE" ? "ACTIVE / SYNCED" : "RECOVERY ACTIVE"}</span></div>
                  <div>Recovery Queue: <span style={{ color: (stationTrace?.retry_count || 0) > 0 ? "#f59e0b" : "#10b981" }}>{stationTrace?.retry_count || 0}/5 retry attempts</span></div>
                  <div>Solver Timestamp: <span style={{ color: "#ffffff" }}>{stationTrace?.last_successful_calculation ? new Date(stationTrace.last_successful_calculation).toLocaleString() : "N/A"}</span></div>
                  <div>Last Successful Cycle: <span style={{ color: "#ffffff" }}>{stationTrace?.last_successful_download ? new Date(stationTrace.last_successful_download).toLocaleString() : "N/A"}</span></div>
                  <div>Wyoming Connectivity: <span style={{ color: stationTrace?.error ? "#ef4444" : "#10b981" }}>{stationTrace?.error ? `FAILED: ${stationTrace.error}` : "STABLE CONNECTION"}</span></div>
                </div>

                {/* Root Cause Analysis & Remediation Path */}
                {(stationTrace?.static_data_warning === "STATIC_DATA_WARNING" || (stationTrace?.cache_age_hours || 0) > 12.0) && (
                  <div style={{
                    marginTop: "12px",
                    borderTop: "1px solid #1e293b",
                    paddingTop: "10px",
                    color: "#fca5a5",
                    fontSize: "10.5px"
                  }}>
                    <div style={{ color: "#ef4444", fontWeight: "bold", fontSize: "11px", marginBottom: "6px" }}>
                      🚨 STATIC DATA DETECTED!
                    </div>
                    <strong>Identified Root Cause:</strong> <span style={{ color: "#ffffff", backgroundColor: "#ef4444", padding: "1px 6px", borderRadius: "3px", fontWeight: "bold" }}>{stationTrace?.static_data_reason || "STALE_TELEMETRY"}</span>
                    <div style={{ marginTop: "4px", color: "#cbd5e1" }}>
                      {stationTrace?.static_data_reason === "LIVE_INGESTION_FAILURE" && "Wyoming sounding scraping failed due to remote network timeouts or server offline. Fallback profiles loaded."}
                      {stationTrace?.static_data_reason === "SEED_PROFILE_REUSE" && "Local Excel/CSV database connections timed out, forcing a rollback to Climatological sounding seeds."}
                      {stationTrace?.static_data_reason === "STALE_TELEMETRY" && "Ingestion age has exceeded the 12-hour validity window. Synoptic observation flow delayed."}
                      {stationTrace?.static_data_reason === "CACHE_LOCK" && "Directory file permissions or filesystem lock prevents cached file updates."}
                      {stationTrace?.static_data_reason === "SOLVER_REUSE" && "Convective solver integrated identical temperature lapse profiles across consecutive runs."}
                    </div>
                    <div style={{ color: "#94a3b8", marginTop: "6px" }}>
                      <strong>Remediation Path:</strong>
                      <ul style={{ margin: "2px 0 0 16px", padding: 0 }}>
                        <li>Verify firewall rules allow TCP outbound requests to `weather.uwyo.edu`.</li>
                        <li>Force cache refresh via manual override, or check fallback profiles configurations.</li>
                        <li>Ensure the Bolton thermodynamic solver integrates moisture variables without numerical instability.</li>
                      </ul>
                    </div>
                  </div>
                )}
              </div>
            )}
            """

updated_content = content.replace(target_block, replacement_block)

with open(ops_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

print("Ops cockpit HUD warning and Live CAPE Audit engine updated in Phase3OpsModule.jsx")
