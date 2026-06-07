with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()

output = []
start = 5000
end = 5200
for idx in range(start, min(end, len(lines))):
    output.append(f"{idx+1}: {lines[idx]}")

with open('scratch/rh_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
