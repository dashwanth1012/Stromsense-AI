import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()

# Search for activeTab === "FORECAST_LAB"
pos = content.find('activeTab === "FORECAST_LAB"')
if pos != -1:
    line_idx = content.count('\n', 0, pos) + 1
    print("=== FORECAST_LAB Start ===")
    for idx in range(line_idx - 2, line_idx + 18):
        print(f"{idx+1}: {lines[idx]}")
        
    # Let's search for next block RESEARCH_VERIFY start
    pos_rv = content.find('activeTab === "RESEARCH_VERIFY"', pos)
    if pos_rv != -1:
        line_idx_rv = content.count('\n', 0, pos_rv) + 1
        print("=== FORECAST_LAB Ends around line ===", line_idx_rv - 1)
        for idx in range(line_idx_rv - 6, line_idx_rv + 5):
            print(f"{idx+1}: {lines[idx]}")
else:
    print("FORECAST_LAB not found")
