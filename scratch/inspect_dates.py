import re
with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()

# Search all occurrences of setHistoricalDates
matches = [m.start() for m in re.finditer(r'setHistoricalDates', content)]
print(f"Found {len(matches)} matches for setHistoricalDates:")
for m in matches:
    line_idx = content.count('\n', 0, m)
    print(f"Line {line_idx+1}: {lines[line_idx].strip()}")
    # show 5 lines before and after for the second match onwards, since first is state declaration
    if line_idx > 300:
        print("--- context ---")
        for idx in range(line_idx - 3, line_idx + 8):
            print(f"  {idx+1}: {lines[idx]}")
