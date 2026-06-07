import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\ResearchHub.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("METRICS DECLARATION CONTINUATION:")
for idx in range(1540, 1572):
    if idx < len(lines):
        print(f"{idx+1}: {lines[idx].strip()}")
