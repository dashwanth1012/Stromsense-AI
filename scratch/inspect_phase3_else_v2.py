import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\Phase3OpsModule.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("LINES 1165 to 1185:")
for idx in range(1164, 1185):
    if idx < len(lines):
        print(f"{idx+1}: {repr(lines[idx])}")
