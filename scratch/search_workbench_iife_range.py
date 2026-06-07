with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'const indexDefinitions = {' in line and i > 2000:
        print(f"Duplicate indexDefinitions starts at: {i+1}")
    if 'const getIndexDetails = (name) => {' in line and i > 2000:
        print(f"Duplicate getIndexDetails starts at: {i+1}")
    if 'const makeDecisionNarrative = () => {' in line and i > 2000:
        print(f"Following function makeDecisionNarrative starts at: {i+1}")
