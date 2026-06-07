import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\Phase3OpsModule.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find("reviewMode ?")
# Let's find the matching colon of the ternary starting at line 374.
# Since the reviewMode ? ( ternary can be very large, let's look for "): (" or "}: (" or similar.
# Or let's scan lines from 1000 onwards for lines that start with "} : (" or "} :".
lines = content.splitlines()
print("SCANNING FOR TERNARY COLON:")
for idx in range(1000, len(lines)):
    line = lines[idx]
    if line.strip().startswith("} :") or line.strip() == "} : (" or line.strip() == "} :":
        print(f"Line {idx+1}: {line}")
