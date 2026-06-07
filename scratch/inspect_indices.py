with open('backend/analysis_engines.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re
match = re.search(r'def get_historical_step_trace', content)
if match:
    lines = content.splitlines()
    line_idx = content.count('\n', 0, match.start())
    print("=== get_historical_step_trace definition ===")
    print('\n'.join(lines[line_idx:line_idx+100]))
else:
    print("get_historical_step_trace not found")
