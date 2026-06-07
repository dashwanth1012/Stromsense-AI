import pandas as pd
import os

path = 'c:/Users/USER/Thunderstorm analysis/backend/data/imd_observational_records.xlsx'
if os.path.exists(path):
    try:
        xl = pd.ExcelFile(path)
        print("Sheet names:", xl.sheet_names)
        for name in xl.sheet_names:
            df = xl.parse(name)
            print(f"Sheet: {name}, Shape: {df.shape}")
            if 'date' in df.columns:
                print("Min Date:", df['date'].min())
                print("Max Date:", df['date'].max())
            elif 'Date' in df.columns:
                print("Min Date:", df['Date'].min())
                print("Max Date:", df['Date'].max())
    except Exception as e:
         print("Error:", e)
else:
    print("Does not exist")
