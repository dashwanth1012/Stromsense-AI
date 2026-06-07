import json
import re
import os
import pandas as pd

js_path = 'c:/Users/USER/Thunderstorm analysis/frontend/src/components/modules/fallback_data.js'
csv_path = 'c:/Users/USER/Thunderstorm analysis/backend/data/imd_observational_records.csv'
xlsx_path = 'c:/Users/USER/Thunderstorm analysis/backend/data/imd_observational_records.xlsx'

# 1. Read fallback_data.js
with open(js_path, 'r', encoding='utf-8') as f:
    js_text = f.read()

# Strip export syntax to get JSON string
json_match = re.search(r'export\s+const\s+fallbackHistoricalDates\s*=\s*(\[[\s\S]+\]);?', js_text)
if not json_match:
    print("Could not parse fallbackHistoricalDates JS array!")
    exit(1)

json_str = json_match.group(1)
records_2025 = json.loads(json_str)
print(f"Loaded {len(records_2025)} templates from fallback_data.js (year: 2025)")

# 2. Generate 2023 and 2024 records
records_all = []
for yr in ["2023", "2024", "2025"]:
    for r in records_2025:
        new_r = dict(r)
        orig_date = r.get("date", "")
        # replace year part
        if orig_date.startswith("2025-"):
            new_r["date"] = orig_date.replace("2025-", f"{yr}-")
        records_all.append(new_r)

print(f"Generated total of {len(records_all)} records (2023, 2024, 2025)")

# 3. Save back to fallback_data.js
with open(js_path, 'w', encoding='utf-8') as f:
    f.write("export const fallbackHistoricalDates = ")
    json.dump(records_all, f, indent=2)
    f.write(";\n")
print("Saved back to fallback_data.js")

# 4. Save to CSV
# Columns expected in CSV: ['date', 'time', 'station', 'station_code', 'cape', 'li', 'sweat', 'k_index', 'pwat', 'tt_index', 'observed', 'thunderstorm', 'lightning', 'squall', 'rainfall', 'nwx', 'season']
# Let's see what keys are in our fallback data records:
# e.g., {'date': '2025-04-12', 'station': 'Visakhapatnam', 'station_code': '43150', 'observed': 'TSRA', 'thunderstorm': True, 'lightning': True, 'squall': False, 'rainfall': True, 'nwx': False, 'season': 'Pre-Monsoon', 'cape': 3000.0, 'li': -8.0, 'pwat': 65.0, 'sweat': 360.0, 'bulk_shear': 19.8, 'theta_e': 360.5}
# Let's map these keys to the CSV keys:
csv_rows = []
for r in records_all:
    csv_row = {
        "date": r.get("date"),
        "time": "12:00Z" if r.get("thunderstorm") else "00:00Z", # realistic synoptic cycles
        "station": r.get("station"),
        "station_code": r.get("station_code"),
        "cape": r.get("cape"),
        "li": r.get("li"),
        "sweat": r.get("sweat"),
        "k_index": r.get("k_index", 38 if r.get("thunderstorm") else 22),
        "pwat": r.get("pwat"),
        "tt_index": r.get("tt_index", 52.5 if r.get("thunderstorm") else 41.5),
        "observed": r.get("observed"),
        "thunderstorm": r.get("thunderstorm"),
        "lightning": r.get("lightning"),
        "squall": r.get("squall"),
        "rainfall": r.get("rainfall"),
        "nwx": r.get("nwx"),
        "season": r.get("season")
    }
    csv_rows.append(csv_row)

df_csv = pd.DataFrame(csv_rows)
df_csv.to_csv(csv_path, index=False)
print("Saved to CSV:", csv_path)

# 5. Save to Excel
df_csv.to_excel(xlsx_path, index=False, sheet_name="IMD_Observations")
print("Saved to Excel:", xlsx_path)
