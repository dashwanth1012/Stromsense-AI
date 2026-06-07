import json

log_path = r"C:\Users\USER\.gemini\antigravity\brain\3a369011-49b3-4032-bc60-3c0d94fe34dc\.system_generated\logs\transcript.jsonl"
with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'PHASE-5.3' in line:
            try:
                data = json.loads(line)
                content = data.get('content') or ''
                print(f"Line {idx}: type={data.get('type')}, len={len(content)}")
                if len(content) > 100:
                    # Write to a specific file
                    out_path = f"C:\\Users\\USER\\.gemini\\antigravity\\brain\\3a369011-49b3-4032-bc60-3c0d94fe34dc\\scratch\\user_input_{idx}.txt"
                    with open(out_path, 'w', encoding='utf-8') as out_f:
                        out_f.write(content)
                    print(f"  Saved to {out_path}")
            except Exception as e:
                print(f"Line {idx}: error {e}")
