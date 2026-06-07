import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(1318, 1340):
    print(f"{idx+1}: {lines[idx].rstrip()}")
