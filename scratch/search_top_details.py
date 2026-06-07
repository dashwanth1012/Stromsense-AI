with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = -1
for i, line in enumerate(lines):
    if 'const getIndexDetails = (name) => {' in line and i < 1500:
        start = i
        break

if start != -1:
    print(f"Top-level getIndexDetails starts at line {start+1}")
    for idx in range(start, start + 75):
         print(f"{idx+1}: {lines[idx].rstrip()}")
