import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\Phase3OpsModule.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's count braces and parentheses starting from char pos of reviewMode ? at line 374
pos = content.find("reviewMode ? (")
if pos == -1:
    pos = content.find("reviewMode ?") # fallback
print(f"reviewMode ? starts at char {pos}")

# We start searching from pos + len("reviewMode ? (")
brace_count = 0
paren_count = 0
for idx in range(pos + 12, len(content)):
    char = content[idx]
    if char == '{':
        brace_count += 1
    elif char == '}':
        brace_count -= 1
    elif char == '(':
        paren_count += 1
    elif char == ')':
        paren_count -= 1
    elif char == ':' and brace_count == 0 and paren_count == 0:
        print(f"Found matching ':' at char {idx}")
        # print lines around it
        lines_before = content[:idx].splitlines()
        start_line = len(lines_before)
        all_lines = content.splitlines()
        for j in range(max(0, start_line - 5), min(len(all_lines), start_line + 20)):
            print(f"{j+1}: {all_lines[j]}")
        break
