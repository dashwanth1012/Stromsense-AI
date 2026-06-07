import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re
match = re.search(r'const indicesList', content)
if match:
    pos = match.start()
    lines = content.splitlines()
    line_idx = content.count('\n', 0, pos)
    print("=== indicesList and getIndexDetails definition ===")
    print('\n'.join(lines[line_idx:line_idx+65]))
else:
    print("const indicesList not found")
