import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for setHistoricalAnalysis or historicalAnalysis structure
# Let's find lines around handleRunAnalysis
lines = text.split('\n')
for idx, line in enumerate(lines, 1):
    if 'historicalAnalysis' in line or 'setHistoricalAnalysis' in line:
        if 'setHistoricalAnalysis(' in line or 'const ' in line:
            print(f"{idx}: {line}")
