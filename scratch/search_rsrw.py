import os

search_str = 'RSRW'
for root, dirs, files in os.walk('c:/Users/USER/Thunderstorm analysis'):
    if 'node_modules' in root or '.git' in root or 'venv' in root or '.next' in root:
        continue
    for file in files:
        if file.endswith(('.js', '.jsx', '.py', '.json', '.md', '.txt', '.csv')):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                if search_str.lower() in text.lower():
                    print(f"Found in {path}")
            except Exception:
                pass
