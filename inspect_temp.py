with open("backend/analysis_engines.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "def _probability_from_row" in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print 40 lines
        for j in range(1, 40):
            print(f"Line {idx+1+j}: {lines[idx+j].strip()}")
        break
