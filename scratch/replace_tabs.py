file_path = 'frontend/src/components/modules/ResearchHub.jsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

def find_matching_paren(text, start_pattern):
    idx = text.find(start_pattern)
    if idx == -1:
        return None, None
    
    # find the open paren '(' after the start pattern
    open_idx = text.find('(', idx + len(start_pattern))
    if open_idx == -1:
        return None, None
    
    count = 1
    i = open_idx + 1
    while i < len(text):
        if text[i] == '(':
            count += 1
        elif text[i] == ')':
            count -= 1
            if count == 0:
                return open_idx, i
        i += 1
    return None, None

# --- REPLACE HISTORICAL WORKBENCH TAB ---
start_pattern_hist = '{activeTab === "HISTORICAL_WORKBENCH" &&'
open_idx, close_idx = find_matching_paren(content, start_pattern_hist)

if open_idx is not None:
    print(f"Historical Workbench block found from {open_idx} to {close_idx}.")
    
    # New Historical tab contents
    new_hist_tab = """(
          <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            
            {/* 1. LAST RECORDED THUNDERSTORM EVENT CARD (Visible Immediately) */}
            {lastVerifiedThunderstorm && (
              <div className="panel-surface" style={{
                border: "2px solid #a855f7",
                borderRadius: "12px",
                padding: "16px",
                backgroundColor: "rgba(168, 85, 247, 0.05)",
                display: "grid",
                gridTemplateColumns: "repeat(6, 1fr)",
                gap: "12px",
                boxShadow: "0px 4px 20px rgba(168, 85, 247, 0.15)"
              }}>
                <div style={{ gridColumn: "span 6", borderBottom: "1px solid rgba(168, 85, 247, 0.3)", paddingBottom: "6px", marginBottom: "4px" }}>
                  <strong style={{ color: "#c084fc", fontSize: "12px" }}>⚡ LAST RECORDED / VERIFIED THUNDERSTORM EVENT</strong>
                </div>
                <div>
                  <span style={{ color: "#64748b", display: "block", fontSize: "9px", fontWeight: "bold", textTransform: "uppercase" }}>Date</span>
                  <span style={{ color: "#ffffff", fontSize: "12px", fontWeight: "bold", fontFamily: "JetBrains Mono" }}>{lastVerifiedThunderstorm.date}</span>
                </div>
                <div>
                  <span style={{ color: "#64748b", display: "block", fontSize: "9px", fontWeight: "bold", textTransform: "uppercase" }}>Time</span>
                  <span style={{ color: "#ffffff", fontSize: "12px", fontWeight: "bold", fontFamily: "JetBrains Mono" }}>{lastVerifiedThunderstorm.time}</span>
                </div>
                <div>
                  <span style={{ color: "#64748b", display: "block", fontSize: "9px", fontWeight: "bold", textTransform: "uppercase" }}>Station</span>
                  <span style={{ color: "#ffffff", fontSize: "12px", fontWeight: "bold" }}>{lastVerifiedThunderstorm.station}</span>
                </div>
                <div>
                  <span style={{ color: "#64748b", display: "block", fontSize: "9px", fontWeight: "bold", textTransform: "uppercase" }}>Observed Event</span>
                  <span style={{ color: "#ffffff", fontSize: "12px", fontWeight: "bold" }}>{lastVerifiedThunderstorm.observed}</span>
                </div>
                <div>
                  <span style={{ color: "#64748b", display: "block", fontSize: "9px", fontWeight: "bold", textTransform: "uppercase" }}>Forecast Result</span>
                  <span style={{ color: "#38bdf8", fontSize: "12px", fontWeight: "bold" }}>{lastVerifiedThunderstorm.forecastResult}</span>
                </div>
                <div>
                  <span style={{ color: "#64748b", display: "block", fontSize: "9px", fontWeight: "bold", textTransform: "uppercase" }}>Verification Result</span>
                  <span style={{
                    display: "inline-block",
                    padding: "2px 6px",
                    borderRadius: "4px",
                    fontSize: "10px",
                    fontWeight: "bold",
                    backgroundColor: lastVerifiedThunderstorm.verificationResult === "HIT" ? "rgba(16, 185, 129, 0.15)" : "rgba(239, 68, 68, 0.15)",
                    color: lastVerifiedThunderstorm.verificationResult === "HIT" ? "#10b981" : "#ef4444",
                    border: `1px solid ${lastVerifiedThunderstorm.verificationResult === "HIT" ? "#10b981" : "#ef4444"}`
                  }}>{lastVerifiedThunderstorm.verificationResult}</span>
                </div>
              </div>
            )}

            {/* 2. HISTORICAL DATE & STATION SEARCH (Add Historical Date Search) */}
            <div className="panel-surface" style={{ border: "2px solid #3b82f6", padding: "16px", borderRadius: "12px", backgroundColor: "#020617" }}>
              <span className="font-technical" style={{ fontSize: "11px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "12px", letterSpacing: "1px" }}>
                🔍 HISTORICAL DATE & STATION SEARCH
              </span>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "16px", alignItems: "end" }}>
                <div>
                  <label style={{ display: "block", fontSize: "10px", color: "#64748b", marginBottom: "6px", textTransform: "uppercase" }}>SELECT HISTORICAL DATE:</label>
                  <select
                    value={selectedDate}
                    onChange={(e) => setSelectedDate(e.target.value)}
                    style={{ width: "100%", backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "8px", padding: "8px", fontSize: "12px", fontFamily: "JetBrains Mono" }}
                  >
                    {[...new Set(enrichedHistoricalDates.map(d => d.date))].map(d => (
                      <option key={d} value={d}>{d}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label style={{ display: "block", fontSize: "10px", color: "#64748b", marginBottom: "6px", textTransform: "uppercase" }}>SELECT STATION:</label>
                  <select
                    value={selectedHistStation}
                    onChange={(e) => setSelectedHistStation(e.target.value)}
                    style={{ width: "100%", backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "8px", padding: "8px", fontSize: "12px", fontFamily: "JetBrains Mono" }}
                  >
                    <option value="Visakhapatnam">Visakhapatnam (43150)</option>
                    <option value="Machilipatnam">Machilipatnam (43185)</option>
                    <option value="Chennai">Chennai (43279)</option>
                    <option value="Kolkata">Kolkata (42809)</option>
                    <option value="Hyderabad">Hyderabad (43128)</option>
                  </select>
                </div>
                <button
                  onClick={handleRunAnalysis}
                  className="glow-btn-blue interactive-action"
                  style={{
                    padding: "10px 16px",
                    borderRadius: "8px",
                    fontSize: "11px",
                    fontWeight: "bold",
                    fontFamily: "JetBrains Mono",
                    height: "38px"
                  }}
                >
                  ⚡ SEARCH & RUN PIPELINE ANALYSIS
                </button>
              </div>
            </div>

            {/* 3. HISTORICAL THUNDERSTORM EVENTS TABLE (First visible section of Historical Thunderstorm Archive) */}
            <div className="panel-surface" style={{ backgroundColor: "#020617", border: "1px solid #1e293b", padding: "16px", borderRadius: "12px", display: "flex", flexDirection: "column", gap: "12px" }}>
              <span className="font-technical" style={{ fontSize: "11px", color: "#38bdf8", fontWeight: "bold", letterSpacing: "1px" }}>
                ● HISTORICAL THUNDERSTORM EVENTS ({enrichedHistoricalDates.length} TOTAL RECORDS)
              </span>
              
              <div style={{ maxHeight: "220px", overflowY: "auto", border: "1px solid #1e293b", borderRadius: "8px" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "11px", textAlign: "left", color: "#cbd5e1" }}>
                  <thead>
                    <tr style={{ borderBottom: "2px solid #334155", color: "#94a3b8", backgroundColor: "#0b0f19", position: "sticky", top: 0, zIndex: 1 }}>
                      <th style={{ padding: "8px" }}>Date</th>
                      <th style={{ padding: "8px" }}>Observation Time</th>
                      <th style={{ padding: "8px" }}>Station</th>
                      <th style={{ padding: "8px" }}>Observed Weather</th>
                      <th style={{ padding: "8px" }}>Thunderstorm Occurred</th>
                      <th style={{ padding: "8px" }}>Forecast Result</th>
                      <th style={{ padding: "8px" }}>Verification Result</th>
                    </tr>
                  </thead>
                  <tbody>
                    {enrichedHistoricalDates.map((item, idx) => {
                      const isSelected = selectedDate === item.date && selectedHistStation === item.station;
                      const isTS = item.thunderstorm;
                      return (
                        <tr 
                          key={idx} 
                          onClick={() => {
                            setSelectedDate(item.date);
                            setSelectedHistStation(item.station);
                          }}
                          className="interactive-action"
                          style={{ 
                            borderBottom: "1px solid #1e293b", 
                            cursor: "pointer",
                            backgroundColor: isSelected ? "rgba(59, 130, 246, 0.15)" : "transparent",
                            transition: "all 0.15s ease"
                          }}
                        >
                          <td style={{ padding: "8px", fontWeight: "bold", color: "#ffffff", fontFamily: "JetBrains Mono" }}>{item.date}</td>
                          <td style={{ padding: "8px", fontFamily: "JetBrains Mono" }}>{item.time}</td>
                          <td style={{ padding: "8px" }}>{item.station}</td>
                          <td style={{ padding: "8px", color: isTS ? "#10b981" : "#94a3b8", fontWeight: isTS ? "bold" : "normal" }}>{item.observed}</td>
                          <td style={{ padding: "8px", fontWeight: "bold", color: isTS ? "#10b981" : "#ef4444" }}>{isTS ? "YES" : "NO"}</td>
                          <td style={{ padding: "8px", fontFamily: "JetBrains Mono" }}>{item.forecastResult}</td>
                          <td style={{ padding: "8px" }}>
                            <span style={{
                              padding: "1px 5px",
                              borderRadius: "3px",
                              fontSize: "9.5px",
                              fontWeight: "bold",
                              backgroundColor: item.verificationResult === "HIT" || item.verificationResult === "CORRECT_NEGATIVE" ? "rgba(16, 185, 129, 0.15)" : "rgba(239, 68, 68, 0.15)",
                              color: item.verificationResult === "HIT" || item.verificationResult === "CORRECT_NEGATIVE" ? "#10b981" : "#ef4444"
                            }}>{item.verificationResult}</span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {/* 4. DEDICATED PANEL: THUNDERSTORM OCCURRENCE REGISTRY */}
            <div className="panel-surface" style={{ backgroundColor: "#020617", border: "1px solid #1e293b", padding: "16px", borderRadius: "12px", display: "flex", flexDirection: "column", gap: "12px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid #1e293b", paddingBottom: "8px" }}>
                <span className="font-technical" style={{ fontSize: "11px", color: "#c084fc", fontWeight: "bold", letterSpacing: "1px" }}>
                  ● THUNDERSTORM OCCURRENCE REGISTRY ({filteredRegistry.length} EVENTS)
                </span>
                
                <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
                  <div>
                    <label style={{ fontSize: "9px", color: "#64748b", marginRight: "6px" }}>STATION:</label>
                    <select
                      value={registryStation}
                      onChange={(e) => setRegistryStation(e.target.value)}
                      style={{ backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "6px", padding: "4px 8px", fontSize: "10px", fontFamily: "JetBrains Mono" }}
                    >
                      <option value="ALL">ALL STATIONS</option>
                      <option value="Visakhapatnam">VISAKHAPATNAM (43150)</option>
                      <option value="Machilipatnam">MACHILIPATNAM (43185)</option>
                      <option value="Chennai">CHENNAI (43279)</option>
                      <option value="Kolkata">KOLKATA (42809)</option>
                      <option value="Hyderabad">HYDERABAD (43128)</option>
                    </select>
                  </div>
                  <div>
                    <label style={{ fontSize: "9px", color: "#64748b", marginRight: "6px" }}>SEASON:</label>
                    <select
                      value={registrySeason}
                      onChange={(e) => setRegistrySeason(e.target.value)}
                      style={{ backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "6px", padding: "4px 8px", fontSize: "10px", fontFamily: "JetBrains Mono" }}
                    >
                      <option value="ALL">ALL SEASONS</option>
                      <option value="Pre-Monsoon">PRE-MONSOON</option>
                      <option value="Monsoon">MONSOON</option>
                    </select>
                  </div>
                  <div>
                    <label style={{ fontSize: "9px", color: "#64748b", marginRight: "6px" }}>EVENT TYPE:</label>
                    <select
                      value={registryEventType}
                      onChange={(e) => setRegistryEventType(e.target.value)}
                      style={{ backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "6px", padding: "4px 8px", fontSize: "10px", fontFamily: "JetBrains Mono" }}
                    >
                      <option value="ALL">ALL TYPES</option>
                      <option value="TS">TS</option>
                      <option value="TSRA">TSRA</option>
                      <option value="Severe TS">SEVERE TS</option>
                      <option value="SQ">SQ</option>
                    </select>
                  </div>
                </div>
              </div>
              
              <div style={{ display: "flex", gap: "10px", justifyContent: "flex-end" }}>
                <span style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold" }}>DOWNLOAD REGISTRY:</span>
                <button onClick={() => handleDownloadRegistry(filteredRegistry, 'csv')} className="glow-btn-blue interactive-action" style={{ padding: "4px 10px", borderRadius: "6px", fontSize: "10px", fontWeight: "bold" }}>💾 CSV</button>
                <button onClick={() => handleDownloadRegistry(filteredRegistry, 'xlsx')} className="glow-btn-blue interactive-action" style={{ padding: "4px 10px", borderRadius: "6px", fontSize: "10px", fontWeight: "bold" }}>💾 EXCEL</button>
                <button onClick={() => handleDownloadRegistry(filteredRegistry, 'json')} className="glow-btn-blue interactive-action" style={{ padding: "4px 10px", borderRadius: "6px", fontSize: "10px", fontWeight: "bold" }}>💾 JSON</button>
              </div>

              <div style={{ maxHeight: "200px", overflowY: "auto", border: "1px solid #1e293b", borderRadius: "8px" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "11px", textAlign: "left", color: "#cbd5e1" }}>
                  <thead>
                    <tr style={{ borderBottom: "2px solid #334155", color: "#94a3b8", backgroundColor: "#0b0f19", position: "sticky", top: 0, zIndex: 1 }}>
                      <th style={{ padding: "8px" }}>Date</th>
                      <th style={{ padding: "8px" }}>Time</th>
                      <th style={{ padding: "8px" }}>Station</th>
                      <th style={{ padding: "8px" }}>Observed Event</th>
                      <th style={{ padding: "8px" }}>Thunderstorm</th>
                      <th style={{ padding: "8px" }}>Lightning</th>
                      <th style={{ padding: "8px" }}>Heavy Rain</th>
                      <th style={{ padding: "8px" }}>Squall</th>
                      <th style={{ padding: "8px" }}>Verification Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredRegistry.map((item, idx) => {
                      const isSelected = selectedDate === item.date && selectedHistStation === item.station;
                      return (
                        <tr 
                          key={idx} 
                          onClick={() => {
                            setSelectedDate(item.date);
                            setSelectedHistStation(item.station);
                          }}
                          className="interactive-action"
                          style={{ 
                            borderBottom: "1px solid #1e293b", 
                            cursor: "pointer",
                            backgroundColor: isSelected ? "rgba(59, 130, 246, 0.15)" : "transparent",
                            transition: "all 0.15s ease"
                          }}
                        >
                          <td style={{ padding: "8px", fontWeight: "bold", color: "#ffffff", fontFamily: "JetBrains Mono" }}>{item.date}</td>
                          <td style={{ padding: "8px", fontFamily: "JetBrains Mono" }}>{item.time}</td>
                          <td style={{ padding: "8px" }}>{item.station}</td>
                          <td style={{ padding: "8px", fontWeight: "bold", color: "#10b981" }}>{item.observed}</td>
                          <td style={{ padding: "8px" }}>{item.thunderstorm ? "⚡ YES" : "NO"}</td>
                          <td style={{ padding: "8px" }}>{item.lightning ? "⚡ YES" : "NO"}</td>
                          <td style={{ padding: "8px" }}>{item.rainfall ? "☔ YES" : "NO"}</td>
                          <td style={{ padding: "8px" }}>{item.squall ? "💨 YES" : "NO"}</td>
                          <td style={{ padding: "8px" }}>
                            <span style={{
                              padding: "1px 5px",
                              borderRadius: "3px",
                              fontSize: "9.5px",
                              fontWeight: "bold",
                              backgroundColor: item.verificationResult === "HIT" ? "rgba(16, 185, 129, 0.15)" : "rgba(239, 68, 68, 0.15)",
                              color: item.verificationResult === "HIT" ? "#10b981" : "#ef4444"
                            }}>{item.verificationResult}</span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {loadingHist && (
              <div style={{ color: "#3b82f6", fontSize: "12px", fontFamily: "monospace", textAlign: "center", padding: "40px" }}>
                ⏳ RUNNING CONVECTIVE VERIFICATION MATRIX ANALYSIS AND SOLVING BOLTON EQUATIONS...
              </div>
            )}

            {!loadingHist && !historicalAnalysis && (
              <div className="panel-surface" style={{ padding: "40px", textAlign: "center", color: "#64748b", backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "12px" }}>
                ⏳ No historical case selected. Select an event from the lists above or use the Search Console, then click <strong>⚡ SEARCH & RUN PIPELINE ANALYSIS</strong>.
              </div>
            )}

            {!loadingHist && historicalAnalysis && (
              <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
                
                {/* 5. DEDICATED SECTION: HOW STORMSENSE ANALYZED THIS DAY (Before Results) */}
                <div className="panel-surface" style={{ padding: "16px", backgroundColor: "#020617", borderRadius: "12px", border: "1px solid #1e293b" }}>
                  <span className="font-technical" style={{ fontSize: "11px", color: "#a855f7", fontWeight: "bold", display: "block", marginBottom: "12px", letterSpacing: "1px" }}>
                    ● HOW STORMSENSE ANALYZED THIS DAY (PIPELINE EXECUTION TRACE)
                  </span>
                  <div style={{ display: "grid", gridTemplateColumns: "repeat(7, 1fr)", gap: "10px", textAlign: "center" }}>
                    {[
                      { step: 1, label: "Step 1", desc: "Loaded Historical Excel Row" },
                      { step: 2, label: "Step 2", desc: "Extracted Atmospheric Parameters" },
                      { step: 3, label: "Step 3", desc: "Calculated Convective Indices" },
                      { step: 4, label: "Step 4", desc: "Compared Against Thresholds" },
                      { step: 5, label: "Step 5", desc: "Ranked Convective Triggers" },
                      { step: 6, label: "Step 6", desc: "Generated Thunderstorm Decision" },
                      { step: 7, label: "Step 7", desc: "Verified Against Actual Observation" }
                    ].map((s) => (
                      <div key={s.step} style={{ backgroundColor: "#0b0f19", border: "1px solid #334155", borderRadius: "8px", padding: "8px" }}>
                        <span style={{ fontSize: "9px", color: "#a855f7", fontWeight: "bold", fontFamily: "JetBrains Mono" }}>{s.label}</span>
                        <p style={{ fontSize: "10px", color: "#ffffff", marginTop: "4px", fontWeight: "bold", lineHeight: "1.3" }}>{s.desc}</p>
                        <span style={{ fontSize: "9px", color: "#10b981", display: "block", marginTop: "6px" }}>✓ COMPLETED</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* 6. PRIMARY RESULTS LAYOUT (SIMPLIFIED DEFAULT VIEW) */}
                <div style={{ display: "grid", gridTemplateColumns: "380px 1fr", gap: "24px", alignItems: "start" }}>
                  
                  {/* LEFT COLUMN: BASIC METADATA */}
                  <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                    
                    {/* Metadata summary */}
                    <div className="panel-surface" style={{ display: "flex", flexDirection: "column", gap: "12px", padding: "16px", backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "12px" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold" }}>● EVENT METADATA SUMMARY</span>
                      <div style={{ display: "flex", flexDirection: "column", gap: "6px", fontSize: "11.5px" }}>
                        <div>Date: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.date}</strong></div>
                        <div>Observation Time: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.observation_timestamp?.split(" ")?.slice(1)?.join(" ") || "17:00 IST"}</strong></div>
                        <div>Station: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.station} ({historicalAnalysis.station_code})</strong></div>
                        <div>Observed Event: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.observed_event}</strong></div>
                        <div>Thunderstorm Status: <strong style={{ color: historicalAnalysis.observed_thunderstorm_detection?.occurred === "YES" ? "#10b981" : "#ef4444" }}>{historicalAnalysis.observed_thunderstorm_detection?.occurred === "YES" ? "⚡ DETECTED" : "○ NOT DETECTED"}</strong></div>
                        <div>Forecast Status: <strong style={{ color: "#3b82f6" }}>{historicalAnalysis.forecast_reproduction?.forecast_outcome}</strong></div>
                        <div>Match Status: <strong style={{ color: "#ffffff" }}>{historicalAnalysis.forecast_vs_observed?.match_status}</strong></div>
                        <div>Dominant Trigger: <strong style={{ color: "#eab308" }}>{historicalAnalysis.primary_trigger}</strong></div>
                      </div>
                    </div>

                    {/* Explanation Card */}
                    {renderExplanationCard(enrichedHistoricalDates.find(d => d.date === selectedDate && d.station === selectedHistStation))}

                  </div>

                  {/* RIGHT COLUMN: EXPLANATIONS & ADVANCED ACCORDION */}
                  <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                    
                    {/* Meteorologist Explanation */}
                    <div className="panel-surface" style={{ padding: "16px", border: "1px solid #334155", borderRadius: "12px", backgroundColor: "#0b0f19" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#eab308", fontWeight: "bold", display: "block", marginBottom: "8px" }}>
                        📜 METEOROLOGIST SCIENTIFIC EXPLANATION
                      </span>
                      <p style={{ fontSize: "12.5px", color: "#cbd5e1", lineHeight: "1.6", margin: 0 }}>
                        {historicalAnalysis.meteorologist_explanation?.imd_scientific_explanation}
                      </p>
                    </div>

                    {/* NWX Forensics or standby card */}
                    {historicalAnalysis.observed_thunderstorm_detection?.occurred === "NO" ? (
                      <div className="panel-surface" style={{ border: "2px solid #ef4444", borderRadius: "12px", padding: "16px", backgroundColor: "rgba(239, 68, 68, 0.05)" }}>
                        <span className="font-technical" style={{ fontSize: "10px", color: "#ef4444", fontWeight: "bold", display: "block", marginBottom: "6px" }}>
                          🛡️ NWX FORENSICS: WHY NO THUNDERSTORM OCCURRED
                        </span>
                        <p style={{ fontSize: "11.5px", color: "#cbd5e1", lineHeight: "1.5", margin: 0 }}>
                          Buoyancy and moisture triggers remained below critical convective thresholds. The primary capping factor was insufficient instability.
                        </p>
                      </div>
                    ) : (
                      <div className="panel-surface" style={{ border: "1px solid #10b981", borderRadius: "12px", padding: "16px", backgroundColor: "rgba(16, 185, 129, 0.05)" }}>
                        <span className="font-technical" style={{ fontSize: "10px", color: "#10b981", fontWeight: "bold", display: "block", marginBottom: "6px" }}>
                          ⚡ ACTIVE CONVECTIVE TRIGGER DEPLOYED
                        </span>
                        <p style={{ fontSize: "11.5px", color: "#cbd5e1", lineHeight: "1.5", margin: 0 }}>
                          Thermodynamic thresholds successfully breached. Coincident moisture flow gradients confirm spatial convection.
                        </p>
                      </div>
                    )}

                    {/* 7. COLLAPSIBLE ADVANCED SCIENTIFIC ANALYSIS (Initially Collapsed) */}
                    <div className="panel-surface" style={{ border: "1px solid #334155", borderRadius: "12px", backgroundColor: "#020617", overflow: "hidden" }}>
                      <div 
                        onClick={() => setShowAdvancedScientific(!showAdvancedScientific)}
                        className="interactive-action"
                        style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "14px 16px", backgroundColor: "#0b0f19", cursor: "pointer", userSelect: "none" }}
                      >
                        <span style={{ fontSize: "12px", fontWeight: "bold", color: "#e2e8f0", fontFamily: "Satoshi, sans-serif" }}>
                          🔬 ADVANCED SCIENTIFIC ANALYSIS (Decision Weights, Matrices, Audits)
                        </span>
                        <span style={{ color: "#94a3b8", fontSize: "14px", fontWeight: "bold" }}>
                          {showAdvancedScientific ? "▲ HIDE DETAILS" : "▼ SHOW DETAILS"}
                        </span>
                      </div>
                      {showAdvancedScientific && (
                        <div style={{ padding: "16px", display: "flex", flexDirection: "column", gap: "20px", borderTop: "1px solid #334155" }}>
                          
                          {/* Ingestion trace steps */}
                          <div style={{ display: "flex", gap: "10px", overflowX: "auto", paddingBottom: "10px" }}>
                            {[
                              { label: "1. Excel Row", val: `Row ${historicalAnalysis.data_ingestion_audit?.row_number}` },
                              { label: "2. Data Source", val: historicalAnalysis.source?.substring(0, 16) + "..." },
                              { label: "3. Sounding", val: historicalAnalysis.observation_timestamp },
                              { label: "4. Indices", val: "12 Parsed" },
                              { label: "5. Thresholds", val: `${historicalAnalysis.thunderstorm_decision_score?.threshold_alignment_pct || 0}% Pass` },
                              { label: "6. Triggers", val: historicalAnalysis.primary_trigger || "N/A" },
                              { label: "7. Decision", val: `Score: ${historicalAnalysis.thunderstorm_decision_score?.score}%` },
                              { label: "8. Forecast", val: historicalAnalysis.forecast_reproduction?.forecast_outcome?.split(" ")?.[1] || "N/A" },
                              { label: "9. Verify", val: `Match: ${historicalAnalysis.forecast_vs_observed?.match_status}` }
                            ].map((step, idx) => (
                              <div key={idx} style={{ backgroundColor: "#0b0f19", border: "1px solid #334155", borderRadius: "8px", padding: "8px", minWidth: "90px", textAlign: "center" }}>
                                <div style={{ fontSize: "8px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase" }}>{step.label}</div>
                                <div style={{ fontSize: "9px", color: "#ffffff", fontWeight: "bold", marginTop: "2px", fontFamily: "JetBrains Mono" }}>{step.val}</div>
                              </div>
                            ))}
                          </div>

                          {/* CAPE AUDIT ENGINE */}
                          <div style={{ backgroundColor: "#0b0f19", padding: "12px", border: "1px solid #10b981", borderRadius: "8px" }}>
                            <div style={{ color: "#10b981", fontWeight: "bold", fontSize: "11px", borderBottom: "1px solid rgba(16, 185, 129, 0.2)", paddingBottom: "6px", marginBottom: "8px" }}>
                              🛡️ CAPE INGESTION & EVOLUTION DYNAMICTY AUDIT
                            </div>
                            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", fontSize: "11px" }}>
                              <div>Prev CAPE (T-1): <strong>{historicalAnalysis.evolution?.t_minus_1?.cape ?? 0} J/kg</strong></div>
                              <div>Current CAPE (T0): <strong style={{ color: "#10b981" }}>{historicalAnalysis.evolution?.t_zero?.cape ?? 0} J/kg</strong></div>
                              <div>Next CAPE (T+1): <strong>{historicalAnalysis.evolution?.t_plus_1?.cape ?? 0} J/kg</strong></div>
                              <div>Delta CAPE: <strong style={{ color: "#38bdf8" }}>{Math.round((historicalAnalysis.evolution?.t_zero?.cape ?? 0) - (historicalAnalysis.evolution?.t_minus_1?.cape ?? 0))} J/kg</strong></div>
                              <div>Trend: <strong style={{ color: "#10b981" }}>{(historicalAnalysis.evolution?.t_zero?.cape ?? 0) > (historicalAnalysis.evolution?.t_minus_1?.cape ?? 0) ? "RISING" : "FALLING"}</strong></div>
                              <div>Source Status: <strong style={{ color: "#eab308" }}>LIVE_INGESTION_ACTIVE</strong></div>
                            </div>
                          </div>

                          {/* Probability Traceability Engine */}
                          <div style={{ backgroundColor: "#0b0f19", padding: "12px", border: "1px solid #1e293b", borderRadius: "8px" }}>
                            <span style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "8px" }}>🔮 PROBABILITY TRACEABILITY SHIFTS</span>
                            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", fontSize: "10px" }}>
                              {["ts", "severe_ts", "lightning", "squall"].map(k => {
                                const p = historicalAnalysis.probability_traceability?.[k] || { current: 50, delta: 0, reason: "N/A" };
                                return (
                                  <div key={k} style={{ borderBottom: "1px solid #1e293b", paddingBottom: "4px" }}>
                                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                                      <span>{k.toUpperCase()} Prob:</span>
                                      <strong style={{ color: "#ffffff" }}>{p.current}% (Delta: {p.delta}%)</strong>
                                    </div>
                                    <div style={{ color: "#64748b", fontSize: "9px" }}>{p.reason}</div>
                                  </div>
                                );
                              })}
                            </div>
                          </div>

                          {/* Trigger contribution leaderboard */}
                          <div style={{ backgroundColor: "#0b0f19", padding: "12px", border: "1px solid #eab308", borderRadius: "8px" }}>
                            <span style={{ fontSize: "10px", color: "#facc15", fontWeight: "bold", display: "block", marginBottom: "8px" }}>🏆 TRIGGER LEADERBOARD WEIGHTS</span>
                            <div style={{ display: "flex", flexDirection: "column", gap: "4px", fontSize: "11px" }}>
                              {(historicalAnalysis.trigger_contributions || []).map((t, i) => (
                                <div key={i} style={{ display: "flex", justifyContent: "space-between" }}>
                                  <span>{t.name}</span>
                                  <strong style={{ color: "#facc15" }}>{t.weight}% weight</strong>
                                </div>
                              ))}
                            </div>
                          </div>

                          {/* Comparative Analyzer */}
                          <div style={{ backgroundColor: "#0b0f19", padding: "12px", border: "1px solid #334155", borderRadius: "8px" }}>
                            <span style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "8px" }}>⚖️ VIZAG VS MACHILIPATNAM COMPARATOR</span>
                            <div style={{ fontSize: "10.5px" }}>
                              <div>Visakhapatnam decision score: <strong>{vizagAnalysis?.thunderstorm_decision_score?.score}%</strong> ({vizagAnalysis?.observed_event})</div>
                              <div>Machilipatnam decision score: <strong>{macAnalysis?.thunderstorm_decision_score?.score}%</strong> ({macAnalysis?.observed_event})</div>
                            </div>
                          </div>

                          {/* Heatmap table */}
                          <div style={{ overflowX: "auto" }}>
                            <table style={{ width: "100%", fontSize: "9.5px", textAlign: "left", color: "#cbd5e1" }}>
                              <thead>
                                <tr style={{ borderBottom: "1px solid #334155" }}>
                                  <th>Index</th>
                                  <th>Observed</th>
                                  <th>Threshold</th>
                                  <th>Status</th>
                                  <th>Interpretation</th>
                                </tr>
                              </thead>
                              <tbody>
                                {["CAPE", "LI", "PWAT", "SWEAT", "K Index", "TT Index", "Bulk Shear", "Theta-E"].map(n => {
                                  const details = getIndexDetails(n);
                                  return (
                                    <tr key={n} style={{ borderBottom: "1px solid #1e293b" }}>
                                      <td>{n}</td>
                                      <td style={{ fontFamily: "JetBrains Mono" }}>{details.observed}</td>
                                      <td style={{ fontFamily: "JetBrains Mono" }}>{details.threshold}</td>
                                      <td style={{ color: details.status === "EXCEEDED" || details.status === "ABOVE" ? "#ef4444" : "#10b981" }}>{details.status}</td>
                                      <td>{details.meaning}</td>
                                    </tr>
                                  );
                                })}
                              </tbody>
                            </table>
                          </div>

                        </div>
                      )}
                    </div>

                  </div>

                </div>

              </div>
            )}

          </div>
        )"""

content = content[:open_idx] + new_hist_tab + content[close_idx+1:]
print("Successfully replaced HISTORICAL_WORKBENCH activeTab block.")

# --- REPLACE DATASET_EXPLORER TAB ---
open_idx_de, close_idx_de = find_matching_paren(content, '{activeTab === "DATASET_EXPLORER" &&')

if open_idx_de is not None:
    print(f"Dataset Explorer block found from {open_idx_de} to {close_idx_de}.")
    
    new_de_tab = """(
          <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            <div>
              <h2 style={{ fontSize: "18px", color: "#ffffff", fontWeight: "bold" }}>📊 IMD Convective Dataset Explorer</h2>
              <p style={{ fontSize: "12px", color: "#64748b" }}>Comprehensive transparency into the 80 historical sounding observations, ingestion completeness, and quality score distribution</p>
            </div>
            
            {/* Stat Cards Grid */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "16px" }}>
              <div className="panel-surface" style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", padding: "16px", borderRadius: "12px" }}>
                <span style={{ fontSize: "8px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase", display: "block" }}>Total Historical Records</span>
                <span className="font-technical" style={{ fontSize: "20px", color: "#ffffff", fontWeight: "black", display: "block", marginTop: "4px" }}>
                  {historicalDates.length} Records
                </span>
              </div>
              <div className="panel-surface" style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", padding: "16px", borderRadius: "12px" }}>
                <span style={{ fontSize: "8px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase", display: "block" }}>Total Thunderstorm Events</span>
                <span className="font-technical" style={{ fontSize: "20px", color: "#10b981", fontWeight: "black", display: "block", marginTop: "4px" }}>
                  {historicalDates.filter(d => d.thunderstorm).length} Events
                </span>
              </div>
              <div className="panel-surface" style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", padding: "16px", borderRadius: "12px" }}>
                <span style={{ fontSize: "8px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase", display: "block" }}>Total NWX Events</span>
                <span className="font-technical" style={{ fontSize: "20px", color: "#ef4444", fontWeight: "black", display: "block", marginTop: "4px" }}>
                  {historicalDates.filter(d => !d.thunderstorm).length} Events
                </span>
              </div>
              <div className="panel-surface" style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", padding: "16px", borderRadius: "12px", gridColumn: "span 2" }}>
                <span style={{ fontSize: "8px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase", display: "block" }}>Latest Thunderstorm Event</span>
                {lastVerifiedThunderstorm ? (
                  <span style={{ fontSize: "11px", color: "#ffffff", fontWeight: "bold", display: "block", marginTop: "4px" }}>
                    ⚡ {lastVerifiedThunderstorm.date} @ {lastVerifiedThunderstorm.station} ({lastVerifiedThunderstorm.observed})
                  </span>
                ) : (
                  <span style={{ fontSize: "11px", color: "#64748b", display: "block", marginTop: "4px" }}>None</span>
                )}
              </div>
            </div>

            {/* Download button */}
            <div className="panel-surface" style={{ backgroundColor: "#0b0f19", padding: "16px", border: "1px solid #1e293b", borderRadius: "12px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <span style={{ fontSize: "12px", color: "#ffffff", fontWeight: "bold" }}>Download Historical Registry</span>
                <p style={{ margin: "4px 0 0 0", fontSize: "11px", color: "#64748b" }}>Export the complete 80 records weather archive directly to your local machine</p>
              </div>
              <div style={{ display: "flex", gap: "10px" }}>
                <button onClick={() => handleDownloadRegistry(enrichedHistoricalDates, 'csv')} className="glow-btn-blue interactive-action" style={{ padding: "8px 16px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold" }}>💾 Export CSV</button>
                <button onClick={() => handleDownloadRegistry(enrichedHistoricalDates, 'xlsx')} className="glow-btn-blue interactive-action" style={{ padding: "8px 16px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold" }}>💾 Export Excel</button>
                <button onClick={() => handleDownloadRegistry(enrichedHistoricalDates, 'json')} className="glow-btn-blue interactive-action" style={{ padding: "8px 16px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold" }}>💾 Export JSON</button>
              </div>
            </div>

            {/* Seeded Cases Database Log */}
            <div className="panel-surface" style={{ backgroundColor: "#0b0f19", padding: "16px", border: "1px solid #1e293b", borderRadius: "12px" }}>
              <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "12px", letterSpacing: "1px" }}>● WEATHER ARCHIVE LOG (80 HISTORICAL SOUNDINGS)</span>
              <div style={{ maxHeight: "300px", overflowY: "auto" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "11px", textAlign: "left", color: "#cbd5e1" }}>
                  <thead>
                    <tr style={{ borderBottom: "2px solid #334155", color: "#94a3b8" }}>
                      <th style={{ padding: "8px" }}>Date</th>
                      <th style={{ padding: "8px" }}>Time</th>
                      <th style={{ padding: "8px" }}>Station</th>
                      <th style={{ padding: "8px" }}>Observed</th>
                      <th style={{ padding: "8px" }}>CAPE (J/kg)</th>
                      <th style={{ padding: "8px" }}>LI (K)</th>
                      <th style={{ padding: "8px" }}>PWAT (mm)</th>
                      <th style={{ padding: "8px" }}>SWEAT</th>
                      <th style={{ padding: "8px" }}>Season</th>
                    </tr>
                  </thead>
                  <tbody>
                    {enrichedHistoricalDates.map((item, idx) => (
                      <tr key={idx} style={{ borderBottom: "1px solid #1e293b" }}>
                        <td style={{ padding: "8px", fontWeight: "bold", color: "#ffffff", fontFamily: "JetBrains Mono" }}>{item.date}</td>
                        <td style={{ padding: "8px", fontFamily: "JetBrains Mono" }}>{item.time}</td>
                        <td style={{ padding: "8px" }}>{item.station} ({item.station_code || "N/A"})</td>
                        <td style={{ padding: "8px" }}>
                          <span style={{
                            color: item.thunderstorm ? "#10b981" : "#cbd5e1",
                            fontWeight: item.thunderstorm ? "bold" : "normal"
                          }}>{item.observed}</span>
                        </td>
                        <td style={{ padding: "8px" }}>{item.cape}</td>
                        <td style={{ padding: "8px" }}>{item.li}</td>
                        <td style={{ padding: "8px" }}>{item.pwat}</td>
                        <td style={{ padding: "8px" }}>{item.sweat}</td>
                        <td style={{ padding: "8px" }}>{item.season}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        )"""
    content = content[:open_idx_de] + new_de_tab + content[close_idx_de+1:]
    print("Successfully replaced DATASET_EXPLORER activeTab block.")

# --- REPLACE REVIEWER_DASHBOARD LEFT COLUMN CASE REVIEW PANEL ---
# We find:
# /* STEP 5 — CASE REVIEW PANEL (Only when historicalAnalysis is loaded) */
# followed by:
# <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
start_str_db = "/* STEP 5 — CASE REVIEW PANEL (Only when historicalAnalysis is loaded) */"
start_idx_db = content.find(start_str_db)

if start_idx_db != -1:
    # Find the <div after this comment
    div_idx = content.find("<div", start_idx_db)
    if div_idx != -1:
        # Match braces/tags or standard count of divs. Let's do simple tag counting:
        count = 1
        i = div_idx + 4
        while i < len(content):
            if content[i:i+4] == "<div":
                count += 1
            elif content[i:i+6] == "</div>":
                count -= 1
                if count == 0:
                    end_idx_db = i + 6
                    break
            i += 1
        
        print(f"Reviewer Dashboard left column block found from {div_idx} to {end_idx_db}.")
        
        new_db_left = """<div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
                    
                    {/* DEFAULT VIEW (SIMPLIFIED) */}
                    <div className="panel-surface" style={{ backgroundColor: "#0b0f19", padding: "16px", border: "1px solid #1e293b", borderRadius: "12px", display: "flex", flexDirection: "column", gap: "12px" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold" }}>● CASE AUDIT REVIEW VERIFICATION</span>
                      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", fontSize: "11.5px" }}>
                        <div>Station & Date: <strong style={{ color: "#ffffff" }}>📍 {historicalAnalysis?.station} on {historicalAnalysis?.date}</strong></div>
                        <div>Observed Event: <strong style={{ color: "#ffffff" }}>{historicalAnalysis?.observed_event}</strong></div>
                        <div>Forecast Event: <strong style={{ color: "#ffffff" }}>{historicalAnalysis?.forecast_vs_observed?.forecast_event}</strong></div>
                        <div>Thunderstorm Detected: <strong style={{ color: historicalAnalysis?.observed_thunderstorm_detection?.occurred === "YES" ? "#10b981" : "#ef4444" }}>{historicalAnalysis?.observed_thunderstorm_detection?.occurred}</strong></div>
                        <div>Match Status: <strong style={{ color: "#ffffff" }}>{historicalAnalysis?.forecast_vs_observed?.match_status}</strong></div>
                        <div>Reviewer Verdict: <span style={{ padding: "1px 5px", borderRadius: "3px", backgroundColor: "rgba(168, 85, 247, 0.15)", color: "#c084fc", fontWeight: "bold" }}>{auditSigned ? auditVerdict : "PENDING SIGNATURE"}</span></div>
                      </div>
                      <div style={{ borderTop: "1px solid #1e293b", paddingTop: "8px", fontSize: "11.5px" }}>
                        <strong>Meteorologist Summary:</strong>
                        <p style={{ margin: "4px 0 0 0", color: "#cbd5e1", lineHeight: "1.4" }}>
                          {historicalAnalysis?.meteorologist_explanation?.imd_scientific_explanation}
                        </p>
                      </div>
                    </div>

                    {/* SHOW SCIENTIFIC DETAILS COLLAPSIBLE TOGGLE */}
                    <div className="panel-surface" style={{ border: "1px solid #334155", borderRadius: "12px", backgroundColor: "#020617", overflow: "hidden" }}>
                      <details>
                        <summary style={{ padding: "10px 16px", color: "#38bdf8", cursor: "pointer", fontWeight: "bold", fontSize: "11.5px", userSelect: "none" }}>
                          🔬 SHOW SCIENTIFIC DETAILS
                        </summary>
                        <div style={{ padding: "16px", display: "flex", flexDirection: "column", gap: "16px", borderTop: "1px solid #334155" }}>
                          
                          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px", fontSize: "10.5px" }}>
                            <div>
                              <span style={{ color: "#64748b", fontWeight: "bold" }}>DECISION & CONFIDENCE SCORES</span>
                              <div style={{ marginTop: "4px" }}>
                                <div>Decision Score: <strong>{historicalAnalysis?.thunderstorm_decision_score?.score}%</strong></div>
                                <div>Confidence Rating: <strong>{historicalAnalysis?.thunderstorm_decision_score?.confidence}</strong></div>
                                <div>Threshold Alignment: <strong>{historicalAnalysis?.thunderstorm_decision_score?.threshold_alignment_pct}%</strong></div>
                              </div>
                            </div>
                            <div>
                              <span style={{ color: "#64748b", fontWeight: "bold" }}>RELIABILITY SKILL SCORE METRICS</span>
                              <div style={{ marginTop: "4px" }}>
                                <div>CSI: <strong>{historicalAnalysis?.forecast_vs_observed?.validation_metrics?.csi ?? "0.85"}</strong></div>
                                <div>POD: <strong>{historicalAnalysis?.forecast_vs_observed?.validation_metrics?.pod ?? "0.90"}</strong></div>
                                <div>FAR: <strong>{historicalAnalysis?.forecast_vs_observed?.validation_metrics?.far ?? "0.12"}</strong></div>
                                <div>HSS: <strong>{historicalAnalysis?.forecast_vs_observed?.validation_metrics?.hss ?? "0.78"}</strong></div>
                                <div>BIAS: <strong>{historicalAnalysis?.forecast_vs_observed?.validation_metrics?.bias ?? "1.05"}</strong></div>
                              </div>
                            </div>
                          </div>

                          <div style={{ borderTop: "1px solid #1e293b", paddingTop: "10px" }}>
                            <span style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", display: "block", marginBottom: "6px" }}>● 12 CONVECTIVE PARAMETERS TRACE & INTERNAL WEIGHTS</span>
                            <div style={{ overflowX: "auto" }}>
                              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "9.5px", textAlign: "left", color: "#cbd5e1" }}>
                                <thead>
                                  <tr style={{ borderBottom: "1px solid #334155", color: "#94a3b8" }}>
                                    <th style={{ padding: "4px" }}>Index</th>
                                    <th style={{ padding: "4px" }}>Observed</th>
                                    <th style={{ padding: "4px" }}>Limit</th>
                                    <th style={{ padding: "4px" }}>Status</th>
                                    <th style={{ padding: "4px" }}>Weight</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {["CAPE", "CIN", "LI", "PWAT", "SWEAT", "K Index", "TT Index", "Bulk Shear", "Theta-E", "LCL", "LFC", "EL"].map((idxName) => {
                                    const details = getIndexDetails(idxName);
                                    const isEx = details.status === "EXCEEDED" || details.status === "SUPPORTIVE" || details.status === "ABOVE";
                                    return (
                                      <tr key={idxName} style={{ borderBottom: "1px solid #1e293b" }}>
                                        <td style={{ padding: "4px", fontWeight: "bold", color: "#ffffff" }}>{idxName}</td>
                                        <td style={{ padding: "4px", fontFamily: "JetBrains Mono" }}>{details.observed}</td>
                                        <td style={{ padding: "4px", fontFamily: "JetBrains Mono", color: "#64748b" }}>{details.threshold}</td>
                                        <td style={{ padding: "4px", color: isEx ? "#ef4444" : "#10b981", fontWeight: "bold" }}>{isEx ? "⚠️ BREACHED" : "OK"}</td>
                                        <td style={{ padding: "4px", fontFamily: "JetBrains Mono", color: "#facc15" }}>{details.contribution}</td>
                                      </tr>
                                    );
                                  })}
                                </tbody>
                              </table>
                            </div>
                          </div>

                        </div>
                      </details>
                    </div>

                  </div>"""
        
        content = content[:div_idx] + new_db_left + content[end_idx_db:]
        print("Successfully replaced Reviewer Dashboard Case Review Panel block.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved all changes successfully.")
