import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('c:/Users/USER/Thunderstorm analysis/frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print("--- REVIEWER_DASHBOARD TOP (Lines 4095-4200) ---")
for idx in range(4095, min(4200, len(lines))):
    print(f"{idx+1}: {lines[idx]}")
