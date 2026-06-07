import os

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\AnalyticsDeck.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("SECTION 2 & 3 HEAD:")
for i in range(805, 830):
    if i < len(lines):
        print(f"{i+1}: {repr(lines[i])}")

print("\nSECTION 2 & 3 TAIL:")
for i in range(1015, 1040):
    if i < len(lines):
        print(f"{i+1}: {repr(lines[i])}")
