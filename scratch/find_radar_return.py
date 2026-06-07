import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/RadarConsole.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

brackets = 0
in_component = False
for idx, line in enumerate(lines, 1):
    if 'export default function RadarConsole' in line:
        in_component = True
        print(f"Component starts at line {idx}")
    if in_component:
        # Count brackets to see top-level return
        # A simpler way is to search for lines that start with '  return (' or similar
        if line.strip().startswith('return ('):
            # Check indentation: if it is 2 spaces, it is probably the main return
            indent = len(line) - len(line.lstrip())
            print(f"Line {idx} (indent {indent}): {line.strip()}")
