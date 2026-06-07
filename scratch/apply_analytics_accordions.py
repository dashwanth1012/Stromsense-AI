import os

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\AnalyticsDeck.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# --- Part 1: Wrap Section 2 & 3 ---
# Find the exact boundaries
start_pattern = '      {/* SECTION 2 & 3: IMD THRESHOLD TUNING & CONTINGENCY MATRIX HUB */}\n      <div style={{ display: "grid", gridTemplateColumns: "1fr 1.2fr", gap: "24px" }}>'
end_pattern = '      {/* SECTION 4: HISTORICAL OBSERVATIONAL SOUNDING LOG TABLE */}'

start_idx = content.find(start_pattern)
end_idx = content.find(end_pattern)

if start_idx != -1 and end_idx != -1:
    print(f"Part 1 boundaries found: {start_idx} to {end_idx}")
    # Extract the grid block to wrap
    grid_block = content[start_idx + len(start_pattern):end_idx]
    # We want to keep the closing div of this grid which is at the very end of grid_block
    # Let's inspect the end of grid_block: it should end with `      </div>\n\n`
    # Let's wrap the block:
    wrapped_grid = """      {/* SECTION 2 & 3: IMD THRESHOLD TUNING & CONTINGENCY MATRIX HUB */}
      <details style={{ width: "100%", outline: "none", marginBottom: "16px" }}>
        <summary style={{
          cursor: "pointer",
          fontSize: "13px",
          fontWeight: "bold",
          color: "#a855f7",
          fontFamily: "JetBrains Mono",
          outline: "none",
          padding: "12px 20px",
          backgroundColor: "#0b0f19",
          border: "1px solid #334155",
          borderRadius: "12px",
          userSelect: "none"
        }}>
          🛠️ Advanced Diagnostics, Sensitivity Sliders & Contingency Matrix (Click to Expand)
        </summary>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1.2fr", gap: "24px", marginTop: "16px" }}>""" + grid_block + """      </details>\n\n"""
    
    # We can replace from start_idx to end_idx with wrapped_grid + end_pattern
    content = content[:start_idx] + wrapped_grid + content[end_idx:]
    print("Part 1: Section 2 & 3 successfully wrapped in details accordion.")
else:
    print("Error: Part 1 patterns not found!")

# --- Part 2: Update VALIDATION_LAB Tab ---
# Let's find:
#       ) : (
#              <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
#           
#           {/* Header Card */}
#           <div className="panel-surface" style={{ padding: "20px", border: "1px solid #334155" }}>
#             <h2 style={{ fontSize: "16px", color: "#ffffff", fontWeight: "bold" }}>Forecast Validation & AI/ML Calibration Lab</h2>
#             <p style={{ fontSize: "12px", color: "#64748b" }}>Pearson product-moment correlation analysis, convective threshold optimizer, and multi-model estimator calibration cockpit</p>
#             <div style={{ display: "flex", justifySelf: "stretch", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "20px" }}>
#               <div>

old_lab_header = """      ) : (
             <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
          
          {/* Header Card */}
          <div className="panel-surface" style={{ padding: "20px", border: "1px solid #334155" }}>
            <h2 style={{ fontSize: "16px", color: "#ffffff", fontWeight: "bold" }}>Forecast Validation & AI/ML Calibration Lab</h2>
            <p style={{ fontSize: "12px", color: "#64748b" }}>Pearson product-moment correlation analysis, convective threshold optimizer, and multi-model estimator calibration cockpit</p>
          </div>"""

# Let's check if there is slightly different spaces:
# The search showed:
# 1201:       ) : (
# 1202:              <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
# 1203:           
# 1204:           {/* Header Card */}
# 1205:           <div className="panel-surface" style={{ padding: "20px", border: "1px solid #334155" }}>
# 1206:             <h2 style={{ fontSize: "16px", color: "#ffffff", fontWeight: "bold" }}>Forecast Validation & AI/ML Calibration Lab</h2>
# 1207:             <p style={{ fontSize: "12px", color: "#64748b" }}>Pearson product-moment correlation analysis, convective threshold optimizer, and multi-model estimator calibration cockpit</p>
# 1208:           </div>

new_lab_header = """      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
          
          {/* Header Card with Date/Time/Source HUD */}
          <div className="panel-surface" style={{ padding: "20px", display: "flex", flexDirection: "column", gap: "12px", border: "1px solid #334155" }}>
            <div>
              <h2 style={{ fontSize: "16px", color: "#ffffff", fontWeight: "bold" }}>Forecast Validation & AI/ML Calibration Lab</h2>
              <p style={{ fontSize: "12px", color: "#64748b" }}>Pearson product-moment correlation analysis, convective threshold optimizer, and multi-model estimator calibration cockpit</p>
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
              <div>Data Source: <strong style={{ color: "#10b981" }}>IMD Radiosonde Archive & ML Pipeline Registry</strong></div>
            </div>
          </div>"""

# Let's do the replacement for the header first:
if old_lab_header in content:
    content = content.replace(old_lab_header, new_lab_header)
    print("Part 2: Validation lab header updated successfully.")
else:
    # Try with exact indentation from file view
    old_lab_header_alt = """      ) : (
             <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
          
          {/* Header Card */}
          <div className="panel-surface" style={{ padding: "20px", border: "1px solid #334155" }}>
            <h2 style={{ fontSize: "16px", color: "#ffffff", fontWeight: "bold" }}>Forecast Validation & AI/ML Calibration Lab</h2>
            <p style={{ fontSize: "12px", color: "#64748b" }}>Pearson product-moment correlation analysis, convective threshold optimizer, and multi-model estimator calibration cockpit</p>
          </div>"""
    content = content.replace(old_lab_header_alt, new_lab_header)
    print("Part 2: Validation lab header updated (alt).")

# Now we need to wrap the display:grid inside <details> in the validation lab section.
# The grid starts with:
#           <div style={{ display: "grid", gridTemplateColumns: "1.1fr 1.2fr", gap: "24px" }}>
# And ends with:
#             </div>
#           </div>
#         </div>
#       )}
#     </div>
#   );
# }

# Let's locate this grid block.
grid_start_pat = '          <div style={{ display: "grid", gridTemplateColumns: "1.1fr 1.2fr", gap: "24px" }}>'
# Let's find from end of file backwards
grid_start_idx = content.find(grid_start_pat, content.find("Forecast Validation & AI/ML Calibration Lab"))
end_tab_idx = content.find("      )}\n    </div>\n  );\n}", grid_start_idx)

if grid_start_idx != -1 and end_tab_idx != -1:
    print(f"Part 2 grid block found: {grid_start_idx} to {end_tab_idx}")
    grid_content = content[grid_start_idx + len(grid_start_pat):end_tab_idx]
    # We want to strip the outer div's matching closing tags. Let's find the closing tags at the end of grid_content.
    # The grid block starts with:
    # <div style={{ display: "grid", ... }}>
    #    ...
    # </div> (closes display:grid)
    # The grid block is inside a column div:
    # <div style={{ display: "flex", flexDirection: "column", ... }}>
    #   {/* Header Card */}
    #   ...
    #   <div style={{ display: "grid", ... }}> ... </div> (this closes grid_content)
    # </div> (this is closed right before `)}` at the end)
    # So grid_content ends with the closing div of display:grid.
    # Let's verify what the end of grid_content is by rfind:
    last_div_idx = grid_content.rfind("</div>")
    if last_div_idx != -1:
        grid_body = grid_content[:last_div_idx]
        wrapped_val_grid = """          <details style={{ width: "100%", outline: "none" }}>
            <summary style={{
              cursor: "pointer",
              fontSize: "13px",
              fontWeight: "bold",
              color: "#a855f7",
              fontFamily: "JetBrains Mono",
              outline: "none",
              padding: "12px 20px",
              backgroundColor: "#0b0f19",
              border: "1px solid #334155",
              borderRadius: "12px",
              userSelect: "none"
            }}>
              🛠️ Advanced Forecast Calibration, ML Pipeline Configurations & Log Console (Click to Expand)
            </summary>
            
            <div style={{ display: "grid", gridTemplateColumns: "1.1fr 1.2fr", gap: "24px", marginTop: "16px" }}>""" + grid_body + """            </div>
          </details>\n"""
        
        content = content[:grid_start_idx] + wrapped_val_grid + content[end_tab_idx:]
        print("Part 2: Validation lab grid successfully wrapped in details accordion.")
else:
    print("Error: Part 2 patterns not found!")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
