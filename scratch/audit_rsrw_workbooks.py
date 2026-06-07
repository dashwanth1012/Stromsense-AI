from pathlib import Path

import pandas as pd


FILES = [
    Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES Mar - June2023.xlsx"),
    Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES Mar - June2024.xlsx"),
    Path(r"C:\Users\USER\OneDrive\Desktop\RSRW INDICES PREMON2025up.xlsx"),
]


def normalized(value):
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


for path in FILES:
    workbook = pd.ExcelFile(path)
    print(f"FILE={path.name}")
    print(f"SHEETS={workbook.sheet_names}")
    total_rows = 0
    for sheet_name in workbook.sheet_names:
        frame = pd.read_excel(path, sheet_name=sheet_name)
        frame = frame.dropna(how="all")
        total_rows += len(frame)
        columns = [str(column) for column in frame.columns]
        normalized_columns = {normalized(column): column for column in columns}
        date_column = next((column for key, column in normalized_columns.items() if "date" in key), None)
        station_column = next((column for key, column in normalized_columns.items() if "station" in key or "stn" in key), None)
        event_column = next(
            (
                column
                for key, column in normalized_columns.items()
                if any(token in key for token in ("weather", "event", "observed", "phenomena", "ww"))
            ),
            None,
        )

        dates = pd.to_datetime(frame[date_column], errors="coerce") if date_column else pd.Series(dtype="datetime64[ns]")
        stations = (
            sorted({str(value).strip() for value in frame[station_column].dropna() if str(value).strip()})
            if station_column
            else []
        )
        events = frame[event_column].fillna("").astype(str).str.strip().str.upper() if event_column else pd.Series(dtype=str)
        thunderstorm_mask = events.str.contains(r"TS|THUNDER|SQUALL|LIGHTNING", regex=True)
        nwx_mask = events.str.contains(r"NWX|NIL|NO WEATHER|NO SIG|FAIR", regex=True)

        print(
            "SHEET="
            f"{sheet_name};ROWS={len(frame)};COLS={columns};"
            f"DATE_COL={date_column};STATION_COL={station_column};EVENT_COL={event_column};"
            f"DATE_MIN={dates.min() if not dates.empty else None};"
            f"DATE_MAX={dates.max() if not dates.empty else None};"
            f"STATIONS={stations};TS={int(thunderstorm_mask.sum())};NWX={int(nwx_mask.sum())}"
        )
    print(f"TOTAL_ROWS={total_rows}")
    print("---")
