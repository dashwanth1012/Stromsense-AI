import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\ResearchHub.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("RESEARCH HUB USEEFFECTS:")
for idx, line in enumerate(lines):
    if "useEffect" in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print next 10 lines
        for j in range(idx + 1, min(len(lines), idx + 15)):
            print(f"  {j+1}: {lines[j].strip()}")
