import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'class ErrorBoundary' in line:
        print(f"Line {i+1}: {line.strip()}")
        # print 30 lines
        for idx in range(i, min(i+40, len(lines))):
            print(f"{idx+1}: {lines[idx].rstrip()}")
