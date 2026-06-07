import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('c:/Users/USER/Thunderstorm analysis/frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print("--- HISTORICAL_WORKBENCH RENDER MIDDLE (Lines 2712-2835) ---")
for idx in range(2711, min(2835, len(lines))):
    print(f"{idx+1}: {lines[idx]}")
