import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\ResearchHub.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("FORECAST LAB RENDER MAIN PARTS:")
# print around line 2839 to 2900
for idx in range(2838, min(len(lines), 2900)):
    print(f"{idx+1}: {lines[idx].strip()}")
