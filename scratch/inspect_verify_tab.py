import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\ResearchHub.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("RESEARCH_VERIFY TAB DETAILS:")
for idx in range(3210, 3300):
    if idx < len(lines):
        print(f"{idx+1}: {lines[idx].strip()}")
