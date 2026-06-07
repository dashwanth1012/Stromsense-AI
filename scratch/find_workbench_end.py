with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()

output = []
for idx, line in enumerate(lines):
    if 'activeTab === "FORECAST_LAB"' in line:
        output.append(f"FORECAST_LAB starts at: {idx+1}")
        for j in range(max(0, idx - 25), idx + 5):
            output.append(f"{j+1}: {lines[j]}")
        break

with open('scratch/workbench_end_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
