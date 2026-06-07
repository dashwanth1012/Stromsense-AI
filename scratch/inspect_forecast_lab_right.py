import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\ResearchHub.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("FORECAST LAB RENDER RIGHT:")
# print around lines 3040 to 3120
for idx in range(3030, min(len(lines), 3120)):
    print(f"{idx+1}: {lines[idx].strip()}")
