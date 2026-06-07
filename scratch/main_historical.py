with open('backend/main.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

lines = content.splitlines()

output = []
start = 2420
end = 2520
for idx in range(start, min(end, len(lines))):
    output.append(f"{idx+1}: {lines[idx]}")

with open('scratch/main_historical.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
