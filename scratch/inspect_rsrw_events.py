from pathlib import Path
import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

CASES = [
    (Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES Mar - June2023.xlsx"), "All Indices"),
    (Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES Mar - June2024.xlsx"), "Sheet1"),
    (Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES PREMON2025up.xlsx"), "Sheet1"),
    (Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES PREMON2025up.xlsx"), "notes"),
]


for path, sheet in CASES:
    frame = pd.read_excel(path, sheet_name=sheet, header=None)
    print(f"\n=== {path.name} / {sheet} {frame.shape} ===")
    for index, row in frame.iterrows():
        values = [value for value in row.tolist() if pd.notna(value) and str(value).strip()]
        if values and (path.name.endswith("2025up.xlsx") or index < 130):
            print(index, values[:18])
