import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\ResearchHub.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("SEARCHING FOR FORMULA/EQUATION/CONTINGENCY REFS IN RESEARCH HUB:")
for idx, line in enumerate(lines):
    if idx > 3100:
        l_lower = line.lower()
        if "formula" in l_lower or "equation" in l_lower or "contingency" in l_lower or "euclidean" in l_lower:
            print(f"{idx+1}: {line.strip()}")
