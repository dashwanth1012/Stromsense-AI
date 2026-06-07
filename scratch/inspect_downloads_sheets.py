import os
import pandas as pd

downloads_dir = 'c:/Users/USER/Downloads'
for f in os.listdir(downloads_dir):
    if f.endswith(('.xlsx', '.xls')):
        path = os.path.join(downloads_dir, f)
        if os.path.getsize(path) > 0:
            try:
                xl = pd.ExcelFile(path)
                print(f"File: {f}")
                print(f"  Sheets: {xl.sheet_names}")
                for sheet in xl.sheet_names[:5]: # print first 5 sheet stats
                    df = xl.parse(sheet)
                    print(f"    Sheet '{sheet}' - Shape: {df.shape}, Columns: {list(df.columns)[:5]}")
            except Exception as e:
                print(f"Error reading {f}: {e}")
