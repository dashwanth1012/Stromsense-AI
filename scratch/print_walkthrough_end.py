with open(r'C:\Users\USER\.gemini\antigravity\brain\3a369011-49b3-4032-bc60-3c0d94fe34dc\walkthrough.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(len(lines) - 15, len(lines)):
    print(f"{idx+1}: {lines[idx].rstrip()}")
