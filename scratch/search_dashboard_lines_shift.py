with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = -1
for i, line in enumerate(lines):
    if 'activeTab === "REVIEWER_DASHBOARD"' in line:
        start = i
        break

if start != -1:
    print(f"REVIEWER_DASHBOARD starts at: {start+1}")
    # find where it ends
    # We closed it with </ErrorBoundary> at some line
    for j in range(start, len(lines)):
         if 'activeTab === "INDEX_GLOSSARY"' in lines[j]:
              print(f"INDEX_GLOSSARY starts at: {j+1}")
              break
