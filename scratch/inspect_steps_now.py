import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()

# Search for renderAccordionStep(X, "Title"
import re
pattern = r'renderAccordionStep\(\s*(\d+)\s*,\s*\"([^\"]+)\"'
matches = list(re.finditer(pattern, content))

print(f"Found {len(matches)} steps in current file:")
for m in matches:
    step_num = m.group(1)
    title = m.group(2)
    line_num = content.count('\n', 0, m.start()) + 1
    print(f"Step {step_num}: {title} at line {line_num}")
