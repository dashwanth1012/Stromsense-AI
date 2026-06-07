from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from rsrw_archive import build_archive, write_archive


WORKBOOKS = [
    Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES Mar - June2023.xlsx"),
    Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES Mar - June2024.xlsx"),
    Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES PREMON2025up.xlsx"),
]

output_csv = ROOT / "backend" / "data" / "rsrw_historical_archive.csv"
output_xlsx = ROOT / "backend" / "data" / "rsrw_historical_archive.xlsx"

archive = build_archive(WORKBOOKS)
write_archive(archive, output_csv, output_xlsx)

fallback_path = ROOT / "frontend" / "src" / "components" / "modules" / "fallback_data.js"
fallback_records = archive.where(archive.notna(), None).to_dict(orient="records")
fallback_path.write_text(
    "export const fallbackHistoricalDates = "
    + json.dumps(fallback_records, indent=2, ensure_ascii=True)
    + ";\n",
    encoding="utf-8",
)

verified = archive[archive["observation_status"] == "VERIFIED"]
print(f"records={len(archive)}")
print(f"date_min={archive['date'].min()}")
print(f"date_max={archive['date'].max()}")
print(f"years={sorted(archive['date'].str[:4].unique().tolist())}")
print(f"verified_records={len(verified)}")
print(f"thunderstorm_records={int(verified['thunderstorm'].sum())}")
print(f"nwx_records={int(verified['nwx'].sum())}")
print(f"unverified_records={int((archive['observation_status'] != 'VERIFIED').sum())}")
