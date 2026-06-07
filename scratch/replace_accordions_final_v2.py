import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'frontend/src/components/modules/ResearchHub.jsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the CAPE audit engine within Step 3 renderAccordionStep
# Let's search for "CAPE AUDIT ENGINE: RADIOSONDE EVOLUTION"
target_str = """                      {/* CAPE AUDIT ENGINE & DYNAMICTY PANEL */}
                      <div className="panel-surface" style={{ backgroundColor: "#0b0f19", padding: "14px", border: "1px solid #10b981", borderRadius: "8px", marginTop: "16px" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "8px", borderBottom: "1px solid rgba(16, 185, 129, 0.2)", paddingBottom: "6px" }}>
                          <span style={{ color: "#10b981" }}>🛡️</span>
                          <strong style={{ fontSize: "11px", color: "#10b981", fontFamily: "JetBrains Mono" }}>CAPE AUDIT ENGINE: RADIOSONDE EVOLUTION & FRESHNESS DYNAMICTY</strong>
                        </div>
                        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", fontSize: "11px", color: "#cbd5e1" }}>
                          <div>"""

replacement_str = """                      {/* CAPE AUDIT ENGINE & DYNAMICTY PANEL */}
                      <div className="panel-surface" style={{ backgroundColor: "#0b0f19", padding: "14px", border: "1px solid #10b981", borderRadius: "8px", marginTop: "16px" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "8px", borderBottom: "1px solid rgba(16, 185, 129, 0.2)", paddingBottom: "6px" }}>
                          <span style={{ color: "#10b981" }}>🛡️</span>
                          <strong style={{ fontSize: "11px", color: "#10b981", fontFamily: "JetBrains Mono" }}>CAPE AUDIT ENGINE: RADIOSONDE EVOLUTION & FRESHNESS DYNAMICTY</strong>
                        </div>
                        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", fontSize: "11px", color: "#cbd5e1" }}>
                          <div>
                            <span style={{ color: "#64748b", display: "block", fontSize: "9px", fontWeight: "bold" }}>CAPE INGESTION REASONING:</span>
                            <code style={{ fontSize: "12px", color: "#eab308", fontWeight: "bold", fontFamily: "JetBrains Mono" }}>
                              {(() => {
                                const t1 = historicalAnalysis.evolution?.t_minus_1?.cape ?? 0;
                                const t0 = historicalAnalysis.evolution?.t_zero?.cape ?? 0;
                                const tP1 = historicalAnalysis.evolution?.t_plus_1?.cape ?? 0;
                                if (t1 === t0 && t0 === tP1) {
                                  if (t0 === 3000) return "SOLVER_REUSE";
                                  if (t0 === 2500) return "SEED_PROFILE_REUSE";
                                  if (t0 === 0) return "LIVE_INGESTION_FAILURE";
                                  if (t0 === 1200) return "STALE_CACHE";
                                  return "CACHE_LOCK";
                                }
                                return "LIVE_INGESTION_ACTIVE";
                              })()}
                            </code>
                          </div>
                          <div>
                            <span style={{ color: "#64748b", display: "block", fontSize: "9px", fontWeight: "bold" }}>TELEMETRY STATUS:</span>
                            <span style={{ fontSize: "12px", color: "#10b981", fontWeight: "bold" }}>
                              {(() => {
                                const t1 = historicalAnalysis.evolution?.t_minus_1?.cape ?? 0;
                                const t0 = historicalAnalysis.evolution?.t_zero?.cape ?? 0;
                                const tP1 = historicalAnalysis.evolution?.t_plus_1?.cape ?? 0;
                                if (t1 === t0 && t0 === tP1) {
                                  if (t0 === 0) return "✗ LIVE INGESTION FAILURE (FALLBACK ON)";
                                  if (t0 === 1200) return "✗ STALE CACHE DETECTED";
                                  return "⚠️ STATIC CACHE LOCK TRIGGERED";
                                }
                                return "✓ DYNAMIC TELEMETRY SYNCED (100% FRESH)";
                              })()}
                            </span>
                          </div>"""

if target_str in content:
    content = content.replace(target_str, replacement_str)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ CAPE audit engine segments updated.")
else:
    print("✗ CAPE audit engine target string not found.")
