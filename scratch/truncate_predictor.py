import os

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\PredictorEngine.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

truncated_lines = lines[:1455]

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(truncated_lines)

print(f"Truncated file to {len(truncated_lines)} lines.")
