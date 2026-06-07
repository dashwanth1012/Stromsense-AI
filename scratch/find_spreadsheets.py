import os

paths = [
    'c:/Users/USER/Downloads',
    'c:/Users/USER/Desktop',
    'c:/Users/USER/Documents',
    'c:/Users/USER/Thunderstorm analysis'
]

for base in paths:
    if os.path.exists(base):
        print(f"Scanning {base}...")
        for root, dirs, files in os.walk(base):
            # Skip node_modules etc
            if 'node_modules' in root or '.git' in root or 'venv' in root or '.next' in root:
                continue
            for file in files:
                f_lower = file.lower()
                if 'rsrw' in f_lower or 'premon' in f_lower or 'indices' in f_lower or 'thunderstorm' in f_lower:
                    print(os.path.join(root, file))
