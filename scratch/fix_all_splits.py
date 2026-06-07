import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'frontend/src/components/modules/ResearchHub.jsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Line 2469 split
t1 = 'historicalAnalysis.forecast_vs_observed?.forecast_event?.split(" ")[2] || "N/A"'
r1 = 'historicalAnalysis.forecast_vs_observed?.forecast_event?.split(" ")?.[2] || "N/A"'
content = content.replace(t1, r1)

# Fix Line 2852 & 2853 split
t2 = 'details.observed?.split(" ")[0]'
r2 = 'details.observed?.split(" ")?.[0]'
content = content.replace(t2, r2)

t3 = 'details.threshold?.split(" ")[0]'
r3 = 'details.threshold?.split(" ")?.[0]'
content = content.replace(t3, r3)

# Fix Line 2899 split
t4 = 'historicalAnalysis.forecast_reproduction?.forecast_outcome?.split(" ")[1] || "N/A"'
r4 = 'historicalAnalysis.forecast_reproduction?.forecast_outcome?.split(" ")?.[1] || "N/A"'
content = content.replace(t4, r4)

# Fix Line 4876 split (This was the main crash risk!)
t5 = 'historicalAnalysis.forecast_vs_observed?.forecast_event?.split(" ").slice(1).join(" ")'
r5 = 'historicalAnalysis.forecast_vs_observed?.forecast_event?.split(" ")?.slice(1)?.join(" ") || "N/A"'
content = content.replace(t5, r5)

# Also let's update the fallback message in activeTab === "REVIEWER_DASHBOARD"
t_fallback = """              <div className="panel-surface" style={{ padding: "40px", textAlign: "center", color: "#64748b", backgroundColor: "#0b0f19" }}>
                ⏳ Please select a case in the <strong>🕰️ Historical Analysis Center</strong> tab and click <strong>⚡ RUN PIPELINE ANALYSIS</strong> to activate this Reviewer Dashboard view.
              </div>"""

r_fallback = """              <div className="panel-surface" style={{ padding: "40px", textAlign: "center", color: "#64748b", backgroundColor: "#0b0f19" }}>
                ⏳ Please select and analyze a historical case first.
              </div>"""

content = content.replace(t_fallback, r_fallback)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ All split/slice operations protected with optional chaining.")
print("✓ Fallback UI text updated.")
