import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\ResearchHub.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("CUSTOMINPUT SEARCH:")
for idx, line in enumerate(lines):
    if "customInput" in line:
        print(f"{idx+1}: {line.strip()}")
