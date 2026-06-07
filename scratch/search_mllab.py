import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\AnalyticsDeck.jsx", "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find("Forecast Validation & AI/ML Calibration Lab")
if pos != -1:
    lines = content[:pos].splitlines()
    start_line = len(lines)
    all_lines = content.splitlines()
    for idx in range(max(0, start_line - 10), min(len(all_lines), start_line + 15)):
        print(f"{idx+1}: {all_lines[idx]}")
else:
    print("Not found")
