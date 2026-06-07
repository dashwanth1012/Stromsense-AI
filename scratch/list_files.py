import os

for root, dirs, files in os.walk('c:/Users/USER/Thunderstorm analysis'):
    for file in files:
        if file.endswith(('.json', '.csv', '.js', '.jsx')):
            path = os.path.join(root, file)
            if 'node_modules' not in path and '.git' not in path and '.next' not in path:
                print(path)
