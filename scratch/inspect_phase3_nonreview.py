import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\Phase3OpsModule.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for "reviewMode ?" or "reviewMode :"
pos = content.find("reviewMode ?")
if pos != -1:
    print(f"reviewMode ? found at char {pos}")
    # let's look for matching else block or ternary character :
    # Let's search for the close of the reviewMode block, which is activeReviewTab blocks, and look at the end.
    # We can search for activeSection or moduleId checks.
    # Let's search for the next 20 lines after the end of activeReviewTab blocks.
    # Let's write a python script to search for the else or colon of reviewMode ?
    lines = content.splitlines()
    for idx, line in enumerate(lines):
        if "reviewMode ?" in line:
            print(f"Line {idx+1}: {line}")
        if "reviewMode" in line and ":" in line:
            print(f"Line {idx+1}: {line}")
else:
    print("reviewMode ? not found")
