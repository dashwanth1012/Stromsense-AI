import sys

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
# SKEW_T starts at line 1320. Let's inspect the REVIEWER_DASHBOARD block.
# Let's search for the line numbers we need:
# In our previous search, REVIEWER_DASHBOARD activeTab check started around line 4841 (now shifted slightly because of ErrorBoundary wrappers).
# Let's search for "activeTab === \"REVIEWER_DASHBOARD\""
start_idx = -1
for idx, line in enumerate(lines):
    if 'activeTab === "REVIEWER_DASHBOARD"' in line:
        start_idx = idx
        break

if start_idx != -1:
    print(f"Found at line {start_idx+1}")
    end_idx = min(start_idx + 300, len(lines))
    for i in range(max(0, start_idx - 10), end_idx):
        output_lines.append(f"{i+1}: {lines[i]}")
else:
    print("Not found")

out_path = r"C:\Users\USER\.gemini\antigravity\brain\3a369011-49b3-4032-bc60-3c0d94fe34dc\scratch\dashboard_jsx.txt"
with open(out_path, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)
print("Extracted to file!")
