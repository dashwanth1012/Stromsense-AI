import re
with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

for target in ['activeTab === "DATASET_EXPLORER"', 'activeTab === "REVIEWER_DASHBOARD"']:
    idx = content.find(target)
    if idx != -1:
        line_num = content.count('\n', 0, idx) + 1
        print(f"Target {target} starts at line {line_num}")
    else:
        print(f"Target {target} not found")


