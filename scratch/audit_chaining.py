import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(4840, 5072):
    line = lines[idx].strip()
    if 'historicalAnalysis' in line:
        print(f"Line {idx+1}: {line}")
