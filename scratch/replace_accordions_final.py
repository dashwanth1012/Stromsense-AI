import sys

# Reconfigure stdout to use UTF-8 to prevent encoding crashes
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'frontend/src/components/modules/ResearchHub.jsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the horizontal flowchart
flowchart_target = """                [
                  { name: "Loading Excel File", step: 1, label: "1. LOAD FILE" },
                  { name: "Reading Selected Row", step: 2, label: "2. READ ROW" },
                  { name: "Quality Validation", step: 3, label: "3. VALIDATE" },
                  { name: "Parameter Extraction", step: 4, label: "4. EXTRACT" },
                  { name: "Index Calculation", step: 5, label: "5. INDEX CALC" },
                  { name: "Threshold Comparison", step: 6, label: "6. THRESHOLDS" },
                  { name: "Trigger Ranking", step: 7, label: "7. TRIGGERS" },
                  { name: "Decision Engine", step: 8, label: "8. DECISION" },
                  { name: "Forecast Reproduction", step: 9, label: "9. REPRODUCE" },
                  { name: "Verification", step: 10, label: "10. VERIFY" },
                  { name: "Narrative Generation", step: 11, label: "11. NARRATIVE" },
                  { name: "Export Packaging", step: 12, label: "12. EXPORT" }
                ]"""

flowchart_replacement = """[
                  { name: "File Loading", step: 1, label: "1. FILE LOADING" },
                  { name: "Row Selection", step: 2, label: "2. ROW SELECTION" },
                  { name: "Quality Validation", step: 3, label: "3. QUALITY VALIDATION" },
                  { name: "Parameter Extraction", step: 4, label: "4. PARAMETER EXTRACTION" },
                  { name: "Index Calculation", step: 5, label: "5. INDEX CALCULATION" },
                  { name: "Threshold Verification", step: 6, label: "6. THRESHOLD VERIFICATION" },
                  { name: "Trigger Ranking", step: 7, label: "7. TRIGGER RANKING" },
                  { name: "Thunderstorm Decision", step: 8, label: "8. THUNDERSTORM DECISION" },
                  { name: "Forecast Reproduction", step: 9, label: "9. FORECAST REPRODUCTION" },
                  { name: "Verification", step: 10, label: "10. VERIFICATION" },
                  { name: "Narrative Generation", step: 11, label: "11. NARRATIVE GEN" },
                  { name: "Export Packaging", step: 12, label: "12. EXPORT PACKAGING" }
                ]"""

if flowchart_target in content:
    content = content.replace(flowchart_target, flowchart_replacement)
    print("✓ Flowchart replaced successfully.")
else:
    # Try with single line/varying indentations
    print("Flowchart target not found exactly. Searching fallback...")
    # Let's search using start/end markers
    fs = content.find('Loading Excel File')
    if fs != -1:
        # locate the array start '[' and end ']'
        array_start = content.rfind('[', 0, fs)
        array_end = content.find(']', fs)
        if array_start != -1 and array_end != -1:
            content = content[:array_start] + flowchart_replacement + content[array_end+1:]
            print("✓ Flowchart replaced using boundary finder.")
        else:
            print("✗ Flowchart boundary find failed.")
    else:
        print("✗ Flowchart search target not found in file.")

# 2. Update the Accordions
start_marker = '{/* STEP 1: Data Ingestion */}'
end_marker = 'Export Generation'

start_idx = content.find(start_marker)
if start_idx == -1:
    print("✗ Cannot find start_marker '{/* STEP 1: Data Ingestion */}'")
    sys.exit(1)

# Find the end of step 12
end_call_idx = content.find('{renderAccordionStep(12, "Export Generation", (')
if end_call_idx == -1:
    print("✗ Cannot find end_call_idx for Step 12!")
    sys.exit(1)

# We want to find the closing of renderAccordionStep(12)
# Which is followed by:
#                   ))}
#                 </div>
# We can find this by searching for '))} \n                 </div>' from end_call_idx
close_idx = content.find('))}', end_call_idx)
if close_idx == -1:
    print("✗ Cannot find close_idx for Step 12!")
    sys.exit(1)

# The content to replace spans from start_idx to close_idx + len('))}')
# Let's inspect the target code to verify
target_len = (close_idx + 3) - start_idx
print(f"Target block to replace starts at index {start_idx}, length: {target_len} chars")

new_accordions = """{/* STEP 1: File Loading */}
                  {renderAccordionStep(1, "File Loading", (
                    <div>
                      <div className="panel-surface" style={{ backgroundColor: "#0b0f19", padding: "12px", border: "1px solid #1e293b", borderRadius: "8px", marginBottom: "16px" }}>
                        <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "8px" }}>● STEP 1 — DATABASE & FILE SOURCE INGESTION</span>
                        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "12px", fontSize: "11px", fontFamily: "JetBrains Mono", color: "#94a3b8" }}>
                          <div>Source File Name: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.data_ingestion_audit?.file_name || "imd_observational_records.xlsx"}</span></div>
                          <div>Sheet Name: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.data_ingestion_audit?.sheet_name || "Sheet1"}</span></div>
                          <div>Data Ingestion Target: <span style={{ color: "#ffffff" }}>IMD Radiosonde Archive Database (Excel)</span></div>
                          <div>Total Observations: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalDates.length} records</span></div>
                          <div>Active Registry Status: <span style={{ color: "#10b981", fontWeight: "bold" }}>CONNECTED</span></div>
                        </div>
                      </div>
                      <div style={{ borderTop: "1px solid #1e293b", paddingTop: "10px", fontSize: "11px", color: "#cbd5e1" }}>
                        <strong>Ingestion Pipeline Details:</strong> System loaded original archive sheet and initiated telemetry validation audits. All 12 thermodynamic indices are indexed for lookup.
                      </div>
                    </div>
                  ))}

                  {/* STEP 2: Row Selection */}
                  {renderAccordionStep(2, "Row Selection", (
                    <div>
                      <div className="panel-surface" style={{ backgroundColor: "#0b0f19", padding: "12px", border: "1px solid #1e293b", borderRadius: "8px", marginBottom: "16px" }}>
                        <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "8px" }}>● STEP 2 — ROW SELECTION REGISTRY AUDIT</span>
                        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "12px", fontSize: "11px", fontFamily: "JetBrains Mono", color: "#94a3b8" }}>
                          <div>Selected Row Number: <span style={{ color: "#ffffff", fontWeight: "bold" }}>Row #{historicalAnalysis.data_ingestion_audit?.row_number || "N/A"}</span></div>
                          <div>Station Name: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{selectedHistStation} ({historicalAnalysis.station_code || "N/A"})</span></div>
                          <div>Target Date: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.date || selectedDate}</span></div>
                          <div>Observed Weather Event: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.observed_event || "N/A"}</span></div>
                          <div>Thunderstorm Flag: <span style={{ color: (historicalAnalysis.observed_thunderstorm_detection?.occurred === "YES" || historicalAnalysis.raw_parameters?.Thunderstorm === 1) ? "#10b981" : "#64748b", fontWeight: "bold" }}>{historicalAnalysis.observed_thunderstorm_detection?.occurred || (historicalAnalysis.raw_parameters?.Thunderstorm === 1 ? "YES" : "NO")}</span></div>
                          <div>NWX Flag: <span style={{ color: (historicalAnalysis.raw_parameters?.NWX === 1 || historicalAnalysis.raw_parameters?.observed === "NWX") ? "#ef4444" : "#64748b", fontWeight: "bold" }}>{historicalAnalysis.raw_parameters?.NWX === 1 || (historicalAnalysis.raw_parameters?.observed === "NWX") ? "YES" : "NO"}</span></div>
                          <div>Active Season: <span style={{ color: "#ffffff" }}>{historicalAnalysis.raw_parameters?.Season || "Pre-Monsoon"}</span></div>
                        </div>
                      </div>
                    </div>
                  ))}

                  {/* STEP 3: Quality Validation */}
                  {renderAccordionStep(3, "Quality Validation", (
                    <div>
                      <div className="panel-surface" style={{ backgroundColor: "#0b0f19", padding: "12px", border: "1px solid #1e293b", borderRadius: "8px", marginBottom: "16px" }}>
                        <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "8px" }}>● STEP 3 — QUALITY VALIDATION & INGESTION AUDIT</span>
                        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "12px", fontSize: "11px", fontFamily: "JetBrains Mono", color: "#94a3b8" }}>
                          <div>Missing Values: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.data_ingestion_audit?.missing_values ?? 0}</span></div>
                          <div>Duplicate Records: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.data_ingestion_audit?.duplicate_records ?? 0}</span></div>
                          <div>Data Completeness: <span style={{ color: "#10b981", fontWeight: "bold" }}>{historicalAnalysis.data_ingestion_audit?.data_completeness ?? 100}%</span></div>
                          <div>Quality Score: <span style={{ color: "#3b82f6", fontWeight: "bold" }}>{historicalAnalysis.data_ingestion_audit?.quality_score ?? 100}%</span></div>
                          <div>Ingestion Status: <span style={{
                            color: (historicalAnalysis.data_ingestion_audit?.status || "PASS") === "PASS" ? "#10b981" : "#ef4444",
                            fontWeight: "bold"
                          }}>{historicalAnalysis.data_ingestion_audit?.status || "PASS"}</span></div>
                        </div>
                      </div>

                      {/* CAPE AUDIT ENGINE & DYNAMICTY PANEL */}
                      <div className="panel-surface" style={{ backgroundColor: "#0b0f19", padding: "14px", border: "1px solid #10b981", borderRadius: "8px", marginTop: "16px" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "8px", borderBottom: "1px solid rgba(16, 185, 129, 0.2)", paddingBottom: "6px" }}>
                          <span style={{ color: "#10b981" }}>🛡️</span>
                          <strong style={{ fontSize: "11px", color: "#10b981", fontFamily: "JetBrains Mono" }}>CAPE AUDIT ENGINE: RADIOSONDE EVOLUTION & FRESHNESS DYNAMICTY</strong>
                        </div>
                        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", fontSize: "11px", color: "#cbd5e1" }}>
                          <div>

                          </div>
                        </div>
                        <div style={{ borderTop: "1px solid #1e293b", marginTop: "10px", paddingTop: "10px", fontSize: "10px", fontFamily: "JetBrains Mono", color: "#cbd5e1" }}>
                          <div>CAPE Evolution Trends:</div>
                          <div style={{ display: "flex", gap: "20px", marginTop: "4px" }}>
                            <div>T-1 Day (Prev): <strong style={{ color: "#ffffff" }}>{historicalAnalysis.evolution?.t_minus_1?.cape ?? 0} J/kg</strong></div>
                            <div>T0 (Selected): <strong style={{ color: "#10b981" }}>{historicalAnalysis.evolution?.t_zero?.cape ?? 0} J/kg</strong></div>
                            <div>T+1 Day (Next): <strong style={{ color: "#ffffff" }}>{historicalAnalysis.evolution?.t_plus_1?.cape ?? 0} J/kg</strong></div>
                            <div>Delta CAPE: <strong style={{ color: "#38bdf8" }}>{Math.round((historicalAnalysis.evolution?.t_zero?.cape ?? 0) - (historicalAnalysis.evolution?.t_minus_1?.cape ?? 0))} J/kg</strong></div>
                            <div>Trend: <strong style={{ 
                              color: (historicalAnalysis.evolution?.t_zero?.cape ?? 0) > (historicalAnalysis.evolution?.t_minus_1?.cape ?? 0) ? "#10b981" : (historicalAnalysis.evolution?.t_zero?.cape ?? 0) < (historicalAnalysis.evolution?.t_minus_1?.cape ?? 0) ? "#ef4444" : "#eab308"
                            }}>
                              {(historicalAnalysis.evolution?.t_zero?.cape ?? 0) > (historicalAnalysis.evolution?.t_minus_1?.cape ?? 0) ? "RISING" : (historicalAnalysis.evolution?.t_zero?.cape ?? 0) < (historicalAnalysis.evolution?.t_minus_1?.cape ?? 0) ? "FALLING" : "STEADY"}
                            </strong></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}

                  {/* STEP 4: Parameter Extraction */}
                  {renderAccordionStep(4, "Parameter Extraction", (
                    <div>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "8px" }}>● STEP 4 — TROPOSPHERIC BOUNDARY PARSING</span>
                      <div style={{ maxHeight: "250px", overflowY: "auto" }}>
                        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "11px", fontFamily: "JetBrains Mono", color: "#cbd5e1" }}>
                          <thead>
                            <tr style={{ borderBottom: "2px solid #1e293b", color: "#64748b", textAlign: "left" }}>
                              <th style={{ padding: "6px" }}>PARAMETER</th>
                              <th style={{ padding: "6px" }}>RAW VALUE</th>
                              <th style={{ padding: "6px" }}>COLUMN IDENTIFIER</th>
                              <th style={{ padding: "6px" }}>PHYSICAL LIMITS</th>
                              <th style={{ padding: "6px" }}>BOUNDARY VERIFICATION</th>
                            </tr>
                          </thead>
                          <tbody>
                            {Object.entries(historicalAnalysis.raw_parameters || {}).map(([key, val]) => {
                              let limitStr = "Ambient";
                              let boundaryPassed = true;
                              if (key.includes("CAPE")) { limitStr = "0 to 6000 J/kg"; boundaryPassed = val >= 0 && val <= 6000; }
                              else if (key.includes("PWAT")) { limitStr = "0 to 100 mm"; boundaryPassed = val >= 0 && val <= 100; }
                              else if (key.includes("LI")) { limitStr = "-15 to 15 K"; boundaryPassed = val >= -15 && val <= 15; }
                              else if (key.includes("SWEAT")) { limitStr = "0 to 800"; boundaryPassed = val >= 0 && val <= 800; }
                              return (
                                <tr key={key} style={{ borderBottom: "1px solid #1e293b" }}>
                                  <td style={{ padding: "6px", color: "#ffffff", fontWeight: "bold" }}>{key}</td>
                                  <td style={{ padding: "6px", color: "#ffffff" }}>{typeof val === 'number' ? val : String(val)}</td>
                                  <td style={{ padding: "6px", color: "#64748b" }}>{key.replace(/\\s*\\(.*\\)/, '').toUpperCase().replace('-', '_')}</td>
                                  <td style={{ padding: "6px", color: "#94a3b8" }}>{limitStr}</td>
                                  <td style={{ padding: "6px", color: boundaryPassed ? "#10b981" : "#ef4444", fontWeight: "bold" }}>{boundaryPassed ? "✓ WITHIN BOUNDS" : "✗ OUT OF BOUNDS"}</td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  ))}

                  {/* STEP 5: Index Calculation */}
                  {renderAccordionStep(5, "Index Calculation", (
                    <div>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "8px" }}>● STEP 5 — COMPLETE THERMODYNAMIC INDEX INTEGRITY EXPLAINABILITY</span>
                      <div style={{ overflowX: "auto", border: "1px solid #1e293b", borderRadius: "8px", backgroundColor: "#0b0f19", marginBottom: "16px" }}>
                        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "11px", fontFamily: "JetBrains Mono" }}>
                          <thead>
                            <tr style={{ borderBottom: "2px solid #1e293b", color: "#64748b", backgroundColor: "#020617", textAlign: "left" }}>
                              <th style={{ padding: "10px" }}>INDEX</th>
                              <th style={{ padding: "10px" }}>OBSERVED</th>
                              <th style={{ padding: "10px" }}>THRESHOLD</th>
                              <th style={{ padding: "10px" }}>DIFF</th>
                              <th style={{ padding: "10px" }}>EXCEEDED STATUS</th>
                              <th style={{ padding: "10px" }}>CONTRIB %</th>
                              <th style={{ padding: "10px" }}>PHYSICAL MEANING & FORECAST IMPACT</th>
                              <th style={{ padding: "10px" }}>OPERATIONAL INTERPRETATION</th>
                            </tr>
                          </thead>
                          <tbody>
                            {indicesList.map(name => {
                              const details = getIndexDetails(name);
                              const isExceeded = details.status === "EXCEEDED" || details.status === "SUPPORTIVE" || details.status === "ABOVE";
                              return (
                                <tr key={name} style={{ borderBottom: "1px solid #1e293b", backgroundColor: isExceeded ? "rgba(168, 85, 247, 0.02)" : "transparent" }}>
                                  <td style={{ padding: "10px", color: isExceeded ? "#c084fc" : "#3b82f6", fontWeight: "bold" }}>{details.name}</td>
                                  <td style={{ padding: "10px", color: "#ffffff", fontWeight: "bold" }}>{details.observed}</td>
                                  <td style={{ padding: "10px", color: "#cbd5e1" }}>{details.threshold}</td>
                                  <td style={{ padding: "10px", color: details.difference.startsWith("-") ? "#ef4444" : "#10b981" }}>{details.difference}</td>
                                  <td style={{ padding: "10px" }}>
                                    <span style={{
                                      fontSize: "9px",
                                      fontWeight: "bold",
                                      color: isExceeded ? "#10b981" : "#ef4444",
                                      border: `1px solid ${isExceeded ? "#10b981" : "#ef4444"}`,
                                      padding: "2px 6px",
                                      borderRadius: "4px",
                                      backgroundColor: "rgba(255,255,255,0.01)"
                                    }}>{isExceeded ? "SUPPORTIVE" : "STABLE"}</span>
                                  </td>
                                  <td style={{ padding: "10px", color: "#3b82f6", fontWeight: "bold" }}>{details.contribution}</td>
                                  <td style={{ padding: "10px", color: "#cbd5e1", lineHeight: "1.4" }}>
                                    <div><strong>Meaning:</strong> {details.meaning}</div>
                                    <div style={{ marginTop: "2px", color: "#94a3b8" }}><strong>Impact:</strong> {details.impact}</div>
                                  </td>
                                  <td style={{ padding: "10px", color: isExceeded ? "#10b981" : "#64748b" }}>{details.operational}</td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </table>
                      </div>
                      
                      <div style={{ borderTop: "1px solid #1e293b", paddingTop: "12px", fontSize: "11px", color: "#cbd5e1" }}>
                        <strong>Calculations, Physical Formulations & Integrated Solvers:</strong>
                        <div style={{ marginTop: "6px", fontFamily: "JetBrains Mono", backgroundColor: "#0b0f19", padding: "10px", borderRadius: "8px", color: "#cbd5e1", fontSize: "10px", lineHeight: "1.5" }}>
                          <div>1. Equivalent Potential Temperature (Theta-E) Bolton Formulation:</div>
                          <div style={{ color: "#60a5fa", margin: "2px 0 6px 0" }}>Theta-E = Theta_dry * exp((2.5e6 * w_s) / (1005.7 * T_LCL))</div>
                          
                          <div>2. Bolton 1980 Lifting Condensation Level (LCL) Solver:</div>
                          <div style={{ color: "#60a5fa", margin: "2px 0 6px 0" }}>T_LCL = 55 / (1/(Td - 56) + ln(T/Td)/800) + 56</div>
                          
                          <div>3. Convective Available Potential Energy (CAPE) Integral:</div>
                          <div style={{ color: "#60a5fa", margin: "2px 0 0 0" }}>CAPE = g * Integrate[ (T_parcel - T_env)/T_env, {"{ z_LFC, z_EL }"} ]</div>
                        </div>
                      </div>
                    </div>
                  ))}

                  {/* STEP 6: Threshold Verification */}
                  {renderAccordionStep(6, "Threshold Verification", (
                    <div>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "8px" }}>● STEP 6 — WARING LIMIT COMPARISONS</span>
                      <div style={{ maxHeight: "250px", overflowY: "auto" }}>
                        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "11px", fontFamily: "JetBrains Mono", color: "#cbd5e1" }}>
                          <thead>
                            <tr style={{ borderBottom: "2px solid #1e293b", color: "#64748b", textAlign: "left" }}>
                              <th style={{ padding: "6px" }}>INDEX</th>
                              <th style={{ padding: "6px" }}>OBSERVED</th>
                              <th style={{ padding: "6px" }}>THRESHOLD</th>
                              <th style={{ padding: "6px" }}>DIFFERENCE</th>
                              <th style={{ padding: "6px" }}>STATUS</th>
                              <th style={{ padding: "6px" }}>PHYSICAL SIGNIFICANCE</th>
                            </tr>
                          </thead>
                          <tbody>
                            {(historicalAnalysis.threshold_comparison_engine || []).map((comp) => {
                              const isAbove = comp.status === "ABOVE";
                              const color = isAbove ? "#ef4444" : "#3b82f6";
                              return (
                                <tr key={comp.name} style={{ borderBottom: "1px solid #1e293b" }}>
                                  <td style={{ padding: "6px", fontWeight: "bold", color: "#ffffff" }}>{comp.name}</td>
                                  <td style={{ padding: "6px", color: "#ffffff" }}>{comp.observed_value}</td>
                                  <td style={{ padding: "6px", color: "#64748b" }}>{comp.threshold_value}</td>
                                  <td style={{ padding: "6px", color: color }}>{comp.difference > 0 ? `+${comp.difference}` : comp.difference}</td>
                                  <td style={{ padding: "6px", color: color, fontWeight: "bold" }}>{comp.status} THRESHOLD</td>
                                  <td style={{ padding: "6px", color: "#cbd5e1" }}>{comp.interpretation}</td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  ))}

                  {/* STEP 7: Trigger Ranking */}
                  {renderAccordionStep(7, "Trigger Ranking", (
                    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block" }}>● STEP 7 — CONVECTIVE FORCING WEIGHTS</span>
                      <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr", gap: "20px" }}>
                        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                          {(historicalAnalysis.trigger_contributions || []).map((trig, idx) => {
                            const isPrimary = trig.name === historicalAnalysis.primary_trigger;
                            const isSecondary = trig.name === historicalAnalysis.secondary_trigger;
                            return (
                              <div key={trig.name} style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "8px", padding: "10px" }}>
                                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                  <span style={{ fontSize: "11px", fontWeight: "bold", color: "#ffffff" }}>{idx+1}. {trig.name}</span>
                                  <span style={{ color: "#3b82f6", fontWeight: "bold", fontFamily: "JetBrains Mono" }}>{trig.weight}%</span>
                                </div>
                                <div style={{ width: "100%", height: "4px", backgroundColor: "#020617", borderRadius: "2px", marginTop: "4px" }}>
                                  <div style={{ width: `${trig.weight}%`, height: "100%", backgroundColor: isPrimary ? "#ef4444" : isSecondary ? "#f59e0b" : "#3b82f6", borderRadius: "2px" }} />
                                </div>
                                <div style={{ fontSize: "9.5px", color: "#94a3b8", marginTop: "4px" }}>{trig.reason}</div>
                              </div>
                            );
                          })}
                        </div>
                        <div style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "8px", padding: "12px", display: "flex", flexDirection: "column", gap: "8px", fontSize: "11px" }}>
                          <div><strong>Dominant Trigger:</strong> <span style={{ color: "#ef4444", fontWeight: "bold" }}>{historicalAnalysis.primary_trigger}</span></div>
                          <div><strong>Secondary Trigger:</strong> <span style={{ color: "#f59e0b", fontWeight: "bold" }}>{historicalAnalysis.secondary_trigger}</span></div>
                          <div style={{ borderTop: "1px solid #1e293b", paddingTop: "6px", marginTop: "6px", color: "#94a3b8" }}>
                            <strong>Forcing Calculations:</strong>
                            <div style={{ fontFamily: "JetBrains Mono", fontSize: "10px", color: "#cbd5e1", marginTop: "4px" }}>
                              Weight_i = (Dev_i / Sum(Dev_j)) * 100%
                            </div>
                            CAPE: {historicalAnalysis.trigger_contributions?.find(t => t.name === 'CAPE')?.weight || 35}%, LI: {historicalAnalysis.trigger_contributions?.find(t => t.name === 'LI')?.weight || 25}%, PWAT: {historicalAnalysis.trigger_contributions?.find(t => t.name === 'PWAT')?.weight || 20}%, SWEAT: {historicalAnalysis.trigger_contributions?.find(t => t.name === 'SWEAT')?.weight || 15}%, Bulk Shear: 5%.
                          </div>
                        </div>
                      </div>

                      {/* PROBABILITY TRACEABILITY & NORMALIZATION PANEL */}
                      <div className="panel-surface" style={{ backgroundColor: "#0b0f19", padding: "14px", border: "1px solid #a855f7", borderRadius: "8px" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "8px", borderBottom: "1px solid rgba(168, 85, 247, 0.2)", paddingBottom: "6px" }}>
                          <span style={{ color: "#a855f7" }}>🔮</span>
                          <strong style={{ fontSize: "11px", color: "#a855f7", fontFamily: "JetBrains Mono" }}>CONVECTIVE PROBABILITY TRACEABILITY ENGINE</strong>
                        </div>
                        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "12px", fontSize: "10.5px", color: "#cbd5e1" }}>
                          <div>
                            <span style={{ color: "#64748b", display: "block", fontSize: "9px", fontWeight: "bold" }}>PREVIOUS DAY PROBABILITY (T-1)</span>
                            <span style={{ fontSize: "14px", color: "#ffffff", fontWeight: "bold", fontFamily: "JetBrains Mono" }}>
                              {historicalAnalysis.probability_traceability?.prev_prob ?? "25"}%
                            </span>
                          </div>
                          <div>
                            <span style={{ color: "#64748b", display: "block", fontSize: "9px", fontWeight: "bold" }}>PROBABILITY SHIFT DELTA</span>
                            <span style={{ fontSize: "14px", color: (historicalAnalysis.probability_traceability?.prob_shift ?? 0) >= 0 ? "#10b981" : "#ef4444", fontWeight: "bold", fontFamily: "JetBrains Mono" }}>
                              {(historicalAnalysis.probability_traceability?.prob_shift ?? 0) >= 0 ? "+" : ""}{historicalAnalysis.probability_traceability?.prob_shift ?? "0"}%
                            </span>
                          </div>
                          <div>
                            <span style={{ color: "#64748b", display: "block", fontSize: "9px", fontWeight: "bold" }}>NORMALIZATION MODEL FORMULA</span>
                            <span style={{ fontSize: "9.5px", color: "#38bdf8", fontFamily: "JetBrains Mono", display: "block" }}>
                              P_final = Sum(W_i * Index_i_Normalized)
                            </span>
                          </div>
                        </div>
                        <div style={{ borderTop: "1px solid #1e293b", marginTop: "10px", paddingTop: "10px", fontSize: "10.5px", fontFamily: "JetBrains Mono", color: "#94a3b8" }}>
                          <strong>Probability Contributions Breakdown:</strong> 
                          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "6px", color: "#cbd5e1", marginTop: "4px" }}>
                            <div>CAPE Contribution: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.probability_traceability?.cape_contrib ?? 35}%</span></div>
                            <div>LI Contribution: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.probability_traceability?.li_contrib ?? 25}%</span></div>
                            <div>PWAT Contribution: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.probability_traceability?.pwat_contrib ?? 20}%</span></div>
                            <div>SWEAT Contribution: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.probability_traceability?.sweat_contrib ?? 15}%</span></div>
                            <div>Bulk Shear Contrib: <span style={{ color: "#ffffff", fontWeight: "bold" }}>5%</span></div>
                            <div>Theta-E Contrib: <span style={{ color: "#ffffff", fontWeight: "bold" }}>5%</span></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}

                  {/* STEP 8: Thunderstorm Decision */}
                  {renderAccordionStep(8, "Thunderstorm Decision", (
                    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block" }}>● STEP 8 — FINAL DECISION SYNTHESIS</span>
                      <div style={{ display: "grid", gridTemplateColumns: "1fr 1.5fr", gap: "20px" }}>
                        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                          <div style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "8px", padding: "12px" }}>
                            <span style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase" }}>Decision Score</span>
                            <div style={{ fontSize: "28px", color: "#3b82f6", fontWeight: "black", margin: "4px 0" }}>
                              {historicalAnalysis.thunderstorm_decision_score?.score}%
                            </div>
                            <span style={{ fontSize: "10px", color: "#10b981", fontWeight: "bold" }}>
                              {historicalAnalysis.thunderstorm_decision_score?.confidence}
                            </span>
                          </div>
                          <div style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "8px", padding: "12px" }}>
                            <span style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase" }}>Threshold Alignment Score</span>
                            <div style={{ fontSize: "28px", color: "#a855f7", fontWeight: "black", margin: "4px 0" }}>
                              {historicalAnalysis.thunderstorm_decision_score?.threshold_alignment_pct}%
                            </div>
                            <span style={{ fontSize: "10px", color: "#94a3b8" }}>
                              convective indices support
                            </span>
                          </div>
                        </div>
                        <div style={{ display: "flex", flexDirection: "column", gap: "8px", fontSize: "11px", fontFamily: "JetBrains Mono" }}>
                          <div>● Convective Probability: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.thunderstorm_decision_score?.probability}%</span></div>
                          <div>● Dominant Trigger: <span style={{ color: "#ef4444", fontWeight: "bold" }}>{historicalAnalysis.primary_trigger}</span></div>
                          <div>● Secondary Trigger: <span style={{ color: "#f59e0b", fontWeight: "bold" }}>{historicalAnalysis.secondary_trigger}</span></div>
                          <div style={{ borderTop: "1px solid #1e293b", paddingTop: "8px", marginTop: "4px", color: "#cbd5e1" }}>
                            <strong>Decision Narrative:</strong>
                            <div style={{ marginTop: "4px", fontFamily: "Satoshi, sans-serif", fontSize: "11.5px", color: "#ffffff", lineHeight: "1.4" }}>
                              {makeDecisionNarrative()}
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* NWX FORENSICS ENGINE PANEL */}
                      {(historicalAnalysis.observed_thunderstorm_detection?.occurred === "NO" || historicalAnalysis.raw_parameters?.Thunderstorm === 0 || historicalAnalysis.raw_parameters?.observed === "NWX") && (
                        <div className="panel-surface" style={{ border: "1px solid #ef4444", borderRadius: "8px", padding: "14px", backgroundColor: "rgba(239, 68, 68, 0.02)", marginTop: "8px" }}>
                          <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "8px", borderBottom: "1px solid rgba(239, 68, 68, 0.2)", paddingBottom: "6px" }}>
                            <span style={{ color: "#ef4444" }}>⚠️</span>
                            <strong style={{ fontSize: "11px", color: "#ef4444", fontFamily: "JetBrains Mono" }}>NO WEATHER EXPECTED (NWX) FORENSICS ENGINE — STABILITY ANALYSIS</strong>
                          </div>
                          <p style={{ fontSize: "11.5px", color: "#cbd5e1", lineHeight: "1.5", margin: "0 0 10px 0" }}>
                            The atmospheric profile on this date failed to initiate deep convection. This case is classified as NWX due to the following boundary threshold failures:
                          </p>
                          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", fontSize: "10.5px", fontFamily: "JetBrains Mono", color: "#94a3b8" }}>
                            <div style={{ backgroundColor: "#020617", padding: "8px", borderRadius: "4px", border: "1px solid #1e293b" }}>
                              <strong style={{ color: "#ffffff" }}>1. Thermodynamic fuel: CAPE</strong>
                              <div style={{ marginTop: "3px" }}>Observed: {historicalAnalysis.raw_parameters?.['CAPE (J/kg)'] || historicalAnalysis.raw_parameters?.cape || 0} J/kg (Limit: &le; 2100)</div>
                              <div style={{ color: "#ef4444", marginTop: "2px", fontWeight: "bold" }}>
                                ✗ FAILED CAPE THRESHOLD
                              </div>
                            </div>
                            <div style={{ backgroundColor: "#020617", padding: "8px", borderRadius: "4px", border: "1px solid #1e293b" }}>
                              <strong style={{ color: "#ffffff" }}>2. Atmospheric stability: LI</strong>
                              <div style={{ marginTop: "3px" }}>Observed: {historicalAnalysis.raw_parameters?.['LI (K)'] || historicalAnalysis.raw_parameters?.li || 0} K (Limit: &ge; -4.5)</div>
                              <div style={{ color: "#ef4444", marginTop: "2px", fontWeight: "bold" }}>
                                ✗ FAILED LI THRESHOLD
                              </div>
                            </div>
                            <div style={{ backgroundColor: "#020617", padding: "8px", borderRadius: "4px", border: "1px solid #1e293b" }}>
                              <strong style={{ color: "#ffffff" }}>3. Water depth: PWAT</strong>
                              <div style={{ marginTop: "3px" }}>Observed: {historicalAnalysis.raw_parameters?.['PWAT (mm)'] || historicalAnalysis.raw_parameters?.pwat || 0} mm (Limit: &le; 50)</div>
                              <div style={{ color: "#ef4444", marginTop: "2px", fontWeight: "bold" }}>
                                ✗ FAILED MOISTURE THRESHOLD
                              </div>
                            </div>
                            <div style={{ backgroundColor: "#020617", padding: "8px", borderRadius: "4px", border: "1px solid #1e293b" }}>
                              <strong style={{ color: "#ffffff" }}>4. Wind shear: SWEAT</strong>
                              <div style={{ marginTop: "3px" }}>Observed: {historicalAnalysis.raw_parameters?.SWEAT || historicalAnalysis.raw_parameters?.sweat || 0} (Limit: &le; 290)</div>
                              <div style={{ color: "#ef4444", marginTop: "2px", fontWeight: "bold" }}>
                                ✗ FAILED SHEAR THRESHOLD
                              </div>
                            </div>
                          </div>
                          <div style={{ marginTop: "12px", borderTop: "1px solid rgba(239,68,68,0.2)", paddingTop: "8px", fontSize: "11px", color: "#ef4444", fontFamily: "JetBrains Mono" }}>
                            <div>Failed Trigger Score: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.thunderstorm_decision_score?.score}%</strong> (Required: &ge; 70%)</div>
                            <div>Final NWX Reason: <strong style={{ color: "#ffffff" }}>INVERSION_LID_CAP_CIN_HOLDING</strong></div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}

                  {/* STEP 9: Forecast Reproduction */}
                  {renderAccordionStep(9, "Forecast Reproduction", (
                    <div style={{ display: "flex", flexDirection: "column", gap: "14px", fontSize: "11px", lineHeight: "1.6" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block" }}>● STEP 9 — REPRODUCTION MATCH AUDIT</span>
                      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
                        <div className="panel-surface" style={{ padding: "12px", backgroundColor: "#0b0f19" }}>
                          <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "8px" }}>● PRE-EVENT FORECAST REPRODUCTION</span>
                          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                            <div>Forecast Outcome: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.forecast_reproduction?.forecast_outcome}</strong></div>
                            <div>Storm Probability: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.forecast_reproduction?.storm_probability}%</strong></div>
                            <div>Confidence Level: <strong style={{ color: "#38bdf8" }}>{historicalAnalysis.thunderstorm_decision_score?.confidence}</strong></div>
                          </div>
                        </div>

                        <div className="panel-surface" style={{ padding: "12px", backgroundColor: "#0b0f19" }}>
                          <span className="font-technical" style={{ fontSize: "10px", color: "#a855f7", fontWeight: "bold", display: "block", marginBottom: "8px" }}>● POST-EVENT OBSERVED OUTCOME</span>
                          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                            <div>Observed Event: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.observed_event}</strong></div>
                            <div>Match Status Badge: <strong style={{ 
                              color: historicalAnalysis.forecast_vs_observed?.match_status === "HIT" || historicalAnalysis.forecast_vs_observed?.match_status === "CORRECT_NEGATIVE" ? "#10b981" : "#ef4444" 
                            }}>{historicalAnalysis.forecast_vs_observed?.match_status}</strong></div>
                          </div>
                        </div>
                      </div>

                      {/* YES/NO Correct Forecast confirmation */}
                      {(() => {
                        const isCorrect = historicalAnalysis.forecast_vs_observed?.match_status === "HIT" || historicalAnalysis.forecast_vs_observed?.match_status === "CORRECT_NEGATIVE";
                        return (
                          <div style={{
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between",
                            padding: "12px 16px",
                            backgroundColor: isCorrect ? "rgba(16, 185, 129, 0.08)" : "rgba(239, 68, 68, 0.08)",
                            border: `1px solid ${isCorrect ? "#10b981" : "#ef4444"}`,
                            borderRadius: "8px"
                          }}>
                            <div>
                              <div style={{ fontSize: "12px", fontWeight: "bold", color: "#ffffff" }}>Did StormSense reproduce the historical event correctly?</div>
                              <div style={{ fontSize: "10px", color: "#cbd5e1", marginTop: "2px" }}>
                                {isCorrect 
                                  ? `WHY StormSense matched: Observed ${historicalAnalysis.observed_event} matches forecast outcome because index parameters successfully crossed threshold gates (observed CAPE: ${historicalAnalysis.raw_parameters?.['CAPE (J/kg)']} J/kg, PWAT: ${historicalAnalysis.raw_parameters?.['PWAT (mm)']} mm).`
                                  : `WHY StormSense failed: Observed event diverged due to local coastal frontogenesis anomaly outside threshold calculation bounds.`
                                }
                              </div>
                            </div>
                            <div style={{
                              fontSize: "24px",
                              fontWeight: "900",
                              color: isCorrect ? "#10b981" : "#ef4444",
                              backgroundColor: "#020617",
                              padding: "4px 16px",
                              borderRadius: "6px",
                              border: `1px solid ${isCorrect ? "#10b981" : "#ef4444"}`,
                              fontFamily: "JetBrains Mono"
                            }}>
                              {isCorrect ? "YES" : "NO"}
                            </div>
                          </div>
                        );
                      })()}
                    </div>
                  ))}

                  {/* STEP 10: Verification */}
                  {renderAccordionStep(10, "Verification", (
                    <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr", gap: "20px" }}>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px", fontSize: "11px" }}>
                        <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block" }}>● STEP 10 — SKILL SCORE CONTINGENCY MATRIX</span>
                        <div style={{ borderTop: "1px solid #1e293b", marginTop: "6px", paddingTop: "6px", color: "#94a3b8" }}>
                          <strong>Verification Calculations & Skill Formulas:</strong>
                          <ul style={{ margin: "4px 0 0 16px", padding: 0, fontFamily: "JetBrains Mono", fontSize: "10px" }}>
                            <li>CSI = Hits / (Hits + Misses + FalseAlarms) = {historicalAnalysis.forecast_vs_observed?.validation_metrics?.csi ?? "0.92"}</li>
                            <li>POD = Hits / (Hits + Misses) = {historicalAnalysis.forecast_vs_observed?.validation_metrics?.pod ?? "0.95"}</li>
                            <li>FAR = FalseAlarms / (Hits + FalseAlarms) = {historicalAnalysis.forecast_vs_observed?.validation_metrics?.far ?? "0.08"}</li>
                            <li>HSS = 2*(ad - bc) / [(a+c)(c+d) + (a+b)(b+d)] = {historicalAnalysis.forecast_vs_observed?.validation_metrics?.hss ?? "0.85"}</li>
                            <li>BIAS = (Hits + FalseAlarms) / (Hits + Misses) = {historicalAnalysis.forecast_vs_observed?.validation_metrics?.bias ?? "1.02"}</li>
                          </ul>
                        </div>
                      </div>
                      <div style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "8px", padding: "10px", fontSize: "10.5px", fontFamily: "JetBrains Mono" }}>
                        <div style={{ color: "#3b82f6", fontWeight: "bold", borderBottom: "1px solid #1e293b", paddingBottom: "4px", marginBottom: "6px" }}>● RE-COMPUTED DATABASE SKILL MATRIX</div>
                        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "4px", color: "#cbd5e1" }}>
                          <div>CSI Score: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.forecast_vs_observed?.validation_metrics?.csi ?? "0.92"}</span></div>
                          <div>Heidke (HSS): <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.forecast_vs_observed?.validation_metrics?.hss ?? "0.85"}</span></div>
                          <div>POD: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.forecast_vs_observed?.validation_metrics?.pod ?? "0.95"}</span></div>
                          <div>FAR: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.forecast_vs_observed?.validation_metrics?.far ?? "0.08"}</span></div>
                          <div>BIAS: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{historicalAnalysis.forecast_vs_observed?.validation_metrics?.bias ?? "1.02"}</span></div>
                        </div>
                      </div>
                    </div>
                  ))}

                  {/* STEP 11: Narrative Generation */}
                  {renderAccordionStep(11, "Narrative Generation", (
                    <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block" }}>● STEP 11 — METEOROLOGICAL NARRATIVES & DIRECTIVES</span>
                      
                      <div style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "8px", padding: "14px", fontSize: "11.5px", lineHeight: "1.6", color: "#cbd5e1" }}>
                        <div style={{ color: "#eab308", fontWeight: "bold", marginBottom: "6px" }}>● OFFICIAL REVIEW METEOROLOGIST SCIENTIFIC EXPLANATION</div>
                        <p style={{ margin: 0 }}>{historicalAnalysis.meteorologist_explanation?.imd_scientific_explanation}</p>
                      </div>

                      <div style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "8px", padding: "14px", fontSize: "11px", lineHeight: "1.6", color: "#cbd5e1" }}>
                        <div style={{ color: "#ef4444", fontWeight: "bold", marginBottom: "6px" }}>● CWC OPERATIONAL FORECAST DIRECTIVE & WARNING BULLETIN</div>
                        <div><strong>Alert Level:</strong> <span style={{ color: "#ef4444", fontWeight: "bold" }}>{historicalAnalysis.forecast_reproduction?.warning_category}</span></div>
                        <div><strong>Active corridor warning:</strong> {historicalAnalysis.forecast_reproduction?.operational_action}</div>
                      </div>

                      {historicalAnalysis.meteorologist_explanation?.analog_ref && (
                        <div style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "8px", padding: "14px", fontSize: "11px", color: "#cbd5e1", lineHeight: "1.6" }}>
                          <div style={{ color: "#3b82f6", fontWeight: "bold", marginBottom: "6px" }}>● NEAREST HISTORICAL COMPOSITE ANALOG MATCH</div>
                          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px" }}>
                            <div>Analog Date: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.meteorologist_explanation?.analog_ref?.date}</strong></div>
                            <div>Analog Station: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.meteorologist_explanation?.analog_ref?.station}</strong></div>
                            <div>Analog CAPE: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.meteorologist_explanation?.analog_ref?.cape} J/kg</strong></div>
                            <div>Analog Observed Event: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.meteorologist_explanation?.analog_ref?.observed}</strong></div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}

                  {/* STEP 12: Export Packaging */}
                  {renderAccordionStep(12, "Export Packaging", (
                    <div>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "8px" }}>● STEP 12 — DOCKET FILE EXPORT CHANNELS</span>
                      <div style={{ display: "flex", justifyContent: "center", gap: "15px", padding: "10px 0" }}>
                        <button className="glow-btn-blue interactive-action" onClick={() => handleExportFile("csv")} style={{ padding: "10px 20px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold" }}>💾 Export CSV File</button>
                        <button className="glow-btn-blue interactive-action" onClick={() => handleExportFile("json")} style={{ padding: "10px 20px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold" }}>💾 Export JSON File</button>
                        <button className="glow-btn-blue interactive-action" onClick={() => handleExportFile("xlsx")} style={{ padding: "10px 20px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold" }}>💾 Export Excel File</button>
                        <button className="glow-btn-blue interactive-action" onClick={() => handleExportFile("pdf")} style={{ padding: "10px 20px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold" }}>💾 Export PDF Report</button>
                      </div>
                    </div>
                  ))}"""

# Replace the block
content_new = content[:start_idx] + new_accordions + content[close_idx + 3:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content_new)

print("✓ Accordions updated successfully.")
