import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\ResearchHub.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for "setActiveTab" which is where tab selector is
pos = content.find("setActiveTab")
if pos != -1:
    lines = content[:pos].splitlines()
    start_line = len(lines)
    all_lines = content.splitlines()
    for idx in range(max(0, start_line - 15), min(len(all_lines), start_line + 45)):
        print(f"{idx+1}: {all_lines[idx]}")
