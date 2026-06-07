import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\ResearchHub.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for tabs or menus
print("TABS & MENUS:")
lines = content.splitlines()
for i, line in enumerate(lines):
    if "setActiveTab" in line or 'activeTab ===' in line or "export default" in line:
        print(f"{i+1}: {line}")
