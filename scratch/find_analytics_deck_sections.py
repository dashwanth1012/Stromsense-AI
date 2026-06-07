import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/AnalyticsDeck.jsx', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if any(term in line.lower() for term in ['calibration', 'roc', 'ml pipeline', 'reliability', 'diagram']):
            print(f"{idx}: {line.strip()}")
