import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

import main

rows = main.get_cwc_historical_dates("rsrw_historical_archive.xlsx")
print(rows[0]["date"], rows[0]["time"], rows[0]["source_trace"])
print(rows[1]["date"], rows[1]["time"], rows[1]["source_trace"])
