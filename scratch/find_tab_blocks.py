with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()

# Search for tab renders
targets = [
    'activeTab === "SKEW_T"',
    'activeTab === "WYOMING_DATA"',
    'activeTab === "HISTORICAL_WORKBENCH"',
    'activeTab === "FORECAST_LAB"',
    'activeTab === "RESEARCH_VERIFY"',
    'activeTab === "INDEX_GLOSSARY"',
    'activeTab === "TERMINOLOGY"'
]

for target in targets:
    pos = content.find(target)
    if pos != -1:
        line_num = content.count('\n', 0, pos) + 1
        print(f"Target: {target} starts at line {line_num}")
    else:
        print(f"Target: {target} not found")
