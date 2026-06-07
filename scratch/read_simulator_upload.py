import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('c:/Users/USER/Thunderstorm analysis/frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print("--- FORECAST_LAB UPLOAD PART (Lines 3315-3385) ---")
for idx in range(3315, min(3385, len(lines))):
    print(f"{idx+1}: {lines[idx]}")
