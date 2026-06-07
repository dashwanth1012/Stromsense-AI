import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for activeTab === "REVIEWER_DASHBOARD" block
pos = content.find('activeTab === "REVIEWER_DASHBOARD"')
if pos != -1:
    print("Found REVIEWER_DASHBOARD block at char:", pos)
    # Print 200 lines from pos
    lines = content[pos:pos+15000].splitlines()
    for idx, l in enumerate(lines[:350]):
        print(f"{idx+1}: {l}")
else:
    print("Not found")
