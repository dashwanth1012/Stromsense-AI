import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\ResearchHub.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Let's search for the headings of activeTab blocks
print("SEARCHING FOR TAB HEADINGS:")
for i, line in enumerate(lines):
    if "activeTab ===" in line and "&&" in line:
        print(f"\nTab block at line {i+1}: {line.strip()}")
        # print next 25 lines
        for j in range(i + 1, min(len(lines), i + 26)):
            print(f"{j+1}: {lines[j].strip()}")
