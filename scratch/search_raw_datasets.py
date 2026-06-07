import os

for root, dirs, files in os.walk('c:/Users/USER'):
    # Avoid walking deep into unrelated system dirs
    if any(p in root for p in ['AppData\\Local\\Temp', 'AppData\\Local\\Microsoft', 'AppData\\Roaming', 'Pictures', 'Music', 'Videos', 'Contacts', 'Saved Games', 'Searches', 'Links']):
        continue
    for file in files:
        if 'RSRW' in file or '2023' in file or '2024' in file or '2025' in file or 'observational_records' in file:
            path = os.path.join(root, file)
            # Skip node_modules etc
            if 'node_modules' not in path and '.git' not in path and 'venv' not in path and '.next' not in path:
                print(path)
