import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'HISTORICAL_WORKBENCH' in line or 'Historical Workbench' in line:
        print(f"Line {i+1}: {line.strip()}")
