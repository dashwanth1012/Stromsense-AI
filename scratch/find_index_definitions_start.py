with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'const indexDefinitions = ' in line or 'indexDefinitions = {' in line:
        print(f"Line {i+1}: {line.strip()}")
        # print surrounding 10 lines
        for idx in range(max(0, i-5), min(i+15, len(lines))):
            print(f"{idx+1}: {lines[idx].rstrip()}")
