import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/components/modules/ResearchHub.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(var in line for var in ['auditVerdict', 'reviewerId', 'reviewerComments', 'reviewerName', 'auditSigned', 'signTimestamp']):
        print(f"Line {i+1}: {line.strip()}")
