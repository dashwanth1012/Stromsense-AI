import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'historicalAnalysis' in line and ('useState' in line or 'const' in line or 'let' in line or 'setHistoricalAnalysis' in line):
        print(f"Line {i+1}: {line.strip()}")
        # print surrounding 5 lines
        start = max(0, i - 5)
        end = min(len(lines), i + 15)
        print("--- CONTEXT ---")
        for j in range(start, end):
            print(f"{j+1}: {lines[j].rstrip()}")
        print("===============")
