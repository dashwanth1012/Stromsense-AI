with open('c:/Users/USER/Thunderstorm analysis/frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    text = f.read()
import re
for m in re.finditer(r'activeTab\s*===\s*"([^"]+)"', text):
    print(m.group(0), 'at line', text[:m.start()].count('\n') + 1)
