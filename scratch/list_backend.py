import os

for root, dirs, files in os.walk('c:/Users/USER/Thunderstorm analysis/backend'):
    for file in files:
        path = os.path.join(root, file)
        if 'node_modules' not in path and '.git' not in path and 'venv' not in path and '__pycache__' not in path:
            print(path)
