with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()

output = []
start = 4920
end = 5070
for idx in range(start, min(end, len(lines))):
    output.append(f"{idx+1}: {lines[idx]}")

with open('scratch/dashboard_view.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
