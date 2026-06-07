with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'renderAccordionStep =' in line or 'renderAccordionStep = ' in line:
        print(f"Line {i+1}: {line.strip()}")
        # print 5 lines before and after
        for idx in range(max(0, i-5), min(i+10, len(lines))):
            print(f"{idx+1}: {lines[idx].rstrip()}")
