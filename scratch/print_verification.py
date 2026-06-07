import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- START OF DUPLICATES ---")
for idx in range(2425, 2435):
    print(f"{idx+1}: {lines[idx].rstrip()}")

print("--- END OF DUPLICATES ---")
for idx in range(2538, 2546):
    print(f"{idx+1}: {lines[idx].rstrip()}")
