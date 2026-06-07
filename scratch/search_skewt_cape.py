import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\ResearchHub.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search within SKEW_T block (from line 1640 to 2085)
lines = content.splitlines()
print("SKEW_T BLOCK CAPE REFS:")
for idx in range(1639, 2084):
    line = lines[idx]
    if "cape" in line.lower() or "prob" in line.lower():
        print(f"{idx+1}: {line.strip()}")
