import os

search_dir = 'c:/Users/USER/Thunderstorm analysis/frontend/src'
for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith(('.js', '.jsx', '.css')):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            if 'analyze-historical-dataset' in text or 'analyze_historical_dataset' in text or 'upload-sounding' in text:
                print(f"Found in {path}")
