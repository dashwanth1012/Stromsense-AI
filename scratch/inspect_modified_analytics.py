import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\AnalyticsDeck.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in modified file: {len(lines)}")
for i in range(max(0, len(lines) - 60), len(lines)):
    print(f"{i+1}: {lines[i]}", end="")
