import sys

# Set standard output encoding to utf-8
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if 'REVIEWER_DASHBOARD' in line:
            print(f'{idx}: {line.strip()}')
