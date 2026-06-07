from pathlib import Path

import pandas as pd


CASES = [
    (Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES Mar - June2023.xlsx"), ["Mar2023", "Apr2023", "All Indices"]),
    (Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES Mar - June2024.xlsx"), ["Mar2024", "Apr2024", "Sheet1"]),
    (Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES PREMON2025up.xlsx"), ["May_2025", "June_2025", "forecast"]),
]


for path, sheets in CASES:
    print(f"\n=== {path.name} ===")
    for sheet in sheets:
        frame = pd.read_excel(path, sheet_name=sheet, header=None)
        print(f"\n--- {sheet} {frame.shape} ---")
        print(frame.iloc[:18, :12].to_string(index=True, header=True))
