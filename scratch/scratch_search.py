import os
import pandas as pd

paths = ['c:/Users/USER', 'c:/Users/USER/Downloads', 'c:/Users/USER/Desktop', 'c:/Users/USER/Documents', 'c:/Users/USER/Thunderstorm analysis']
found = []

for base in paths:
    if os.path.exists(base):
        for f in os.listdir(base):
            path = os.path.join(base, f)
            if os.path.isfile(path):
                f_lower = f.lower()
                if 'rsrw' in f_lower or 'premon' in f_lower or 'indices' in f_lower or '2023' in f_lower or '2024' in f_lower or '2025' in f_lower:
                    found.append(path)

print("Found files:")
for path in found:
    print(path)
