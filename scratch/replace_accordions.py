import os

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Flowchart array starts around line 1980
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

content = content.replace(flowchart_target, flowchart_replacement)

# Accordion block starts around:
# {/* STEP 1: Data Ingestion */}
# and ends around export generation:
# {renderAccordionStep(12, "Export Generation", (
#   ...
# ))}

# Let's find the exact block and replace it.
# We'll use marker strings to find the start of STEP 1 and the end of STEP 12.
start_marker = '{/* STEP 1: Data Ingestion */}'
end_marker = '/* STEP 12: Export Generation */}' # wait, let's look at the end marker

# Let's find index of start_marker
start_idx = content.find(start_marker)
if start_idx == -1:
    print("Could not find start_marker!")
    exit(1)

# Let's find the end of Step 12 renderAccordionStep
# Let's search for "Export Generation" renderAccordionStep call
end_call_idx = content.find('{renderAccordionStep(12, "Export Generation", (')
if end_call_idx == -1:
    print("Could not find Step 12 call!")
    exit(1)

# Let's find the close of this step call.
# It should end with:
#                   ))}
#                 </div>
#               </div>
#             );
#           })()}
#         </div>
#       )}
#       </ErrorBoundary>
# 
#         <ErrorBoundary fallbackTitle="⚠ Forecast Lab Rendering Error">

close_target = """                  {renderAccordionStep(12, "Export Generation", (
                    <div style={{ display: "flex", justifyContent: "center", gap: "15px", padding: "10px 0" }}>
                      <button className="glow-btn-blue interactive-action" onClick={() => handleExportFile("csv")} style={{ padding: "10px 20px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold" }}>💾 Export CSV File</button>
                      <button className="glow-btn-blue interactive-action" onClick={() => handleExportFile("json")} style={{ padding: "10px 20px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold" }}>💾 Export JSON File</button>
                      <button className="glow-btn-blue interactive-action" onClick={() => handleExportFile("xlsx")} style={{ padding: "10px 20px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold" }}>💾 Export Excel File</button>
                      <button className="glow-btn-blue interactive-action" onClick={() => handleExportFile("pdf")} style={{ padding: "10px 20px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold" }}>💾 Export PDF Report</button>
                    </div>
                  ))}
                </div>"""

# Let's verify if close_target exists in content
if close_target not in content:
    # try standardizing whitespace/newlines
    print("close_target not found exactly. Let's do search.")
    # We can search for the end of Step 12. Let's print around end_call_idx
    print(content[end_call_idx:end_call_idx+800])
else:
    print("close_target found!")
