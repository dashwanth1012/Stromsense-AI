with open('backend/main.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

lines = content.splitlines()
output = []
for idx in range(2710, min(2750, len(lines))):
    output.append(f"{idx+1}: {lines[idx]}")

with open('scratch/main_timestamp_view.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
