with open('c:/Users/USER/Thunderstorm analysis/frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print("--- HISTORICAL_WORKBENCH RENDER ---")
start = -1
for idx, line in enumerate(lines):
    if 'activeTab === "HISTORICAL_WORKBENCH"' in line:
        start = idx
        break
if start != -1:
    for i in range(start, start + 250):
        if i < len(lines):
            print(f"{i+1}: {lines[i]}")

print("\n--- REVIEWER_DASHBOARD RENDER ---")
start = -1
for idx, line in enumerate(lines):
    if 'activeTab === "REVIEWER_DASHBOARD"' in line:
        start = idx
        break
if start != -1:
    for i in range(start, start + 250):
        if i < len(lines):
            print(f"{i+1}: {lines[i]}")
