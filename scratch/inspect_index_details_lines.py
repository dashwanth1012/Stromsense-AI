import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()

# Search for getIndexDetails
pos = content.find('const getIndexDetails =')
if pos != -1:
    line_idx = content.count('\n', 0, pos) + 1
    print("=== getIndexDetails start context ===")
    for idx in range(line_idx - 2, line_idx + 55):
        print(f"{idx+1}: {lines[idx]}")
else:
    print("getIndexDetails not found")
