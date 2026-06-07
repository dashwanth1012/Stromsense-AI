"""Normalize IMD RSRW index workbooks into the operational archive schema."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd


OBSERVATION_PATTERN = re.compile(r"^\s*(\d{6})/(\d{2})(\d{2})\s*$")

METRIC_LABELS = {
    "showalter index": "showalter",
    "lifted index": "li",
    "lift computed using virtual temperature": "li_virtual",
    "sweat index": "sweat",
    "k index": "k_index",
    "cross totals index": "cross_totals",
    "vertical totals index": "vertical_totals",
    "totals totals index": "tt_index",
    "convective available potential energy": "cape",
    "cape using virtual temperature": "cape_virtual",
    "convective inhibition": "cin",
    "cins using virtual temperature": "cin_virtual",
    "bulk richardson number": "brn",
    "bulk richardson number using capv": "brn_virtual",
    "precipitable water [mm] for entire sounding": "pwat",
}


def _clean_text(value) -> str:
    if pd.isna(value):
        return ""
    return " ".join(str(value).replace("\n", " ").split()).strip()


def _number(value, default=0.0) -> float:
    try:
        result = float(value)
        return default if pd.isna(result) else round(result, 2)
    except (TypeError, ValueError):
        return default


def _metric_key(value) -> str | None:
    label = _clean_text(value).lower().rstrip(":")
    for expected, key in METRIC_LABELS.items():
        if label == expected:
            return key
    return None


def _parse_observation_time(value) -> tuple[str, str] | None:
    match = OBSERVATION_PATTERN.match(_clean_text(value))
    if not match:
        return None
    date_token, hour, minute = match.groups()
    parsed = datetime.strptime(date_token, "%y%m%d")
    return parsed.strftime("%Y-%m-%d"), f"{hour}:{minute}Z"


def _season(date_text: str) -> str:
    month = int(date_text[5:7])
    if month in (3, 4, 5):
        return "Pre-Monsoon"
    if month in (6, 7, 8, 9):
        return "Monsoon"
    if month in (10, 11, 12):
        return "Post-Monsoon"
    return "Winter"


def _event_flags(raw_event: str, observation_verified: bool) -> dict:
    text = _clean_text(raw_event).upper()
    if not observation_verified:
        return {
            "observed": "UNVERIFIED",
            "thunderstorm": False,
            "lightning": False,
            "squall": False,
            "rainfall": False,
            "nwx": False,
        }

    has_ts = bool(re.search(r"\bTS(?::|RA|\b)|\bTRSA\b", text))
    has_lightning = has_ts or bool(re.search(r"\bLT(?::|\b)", text))
    has_squall = bool(re.search(r"\bSQ(?::|\b)", text))
    has_rain = bool(re.search(r"\b(?:RA|DZ|SHRA|TSRA|TRSA|RSRA)(?::|\b)", text))
    explicit_nwx = bool(re.search(r"\b(?:NWX|NIL|NO WEATHER)\b", text))

    if has_squall:
        observed = "SQ"
    elif has_ts and has_rain:
        observed = "TSRA"
    elif has_ts:
        observed = "TS"
    elif has_lightning:
        observed = "LT"
    elif has_rain:
        observed = "RA"
    else:
        observed = "NWX"

    return {
        "observed": observed,
        "thunderstorm": has_ts or has_squall,
        "lightning": has_lightning or has_squall,
        "squall": has_squall,
        "rainfall": has_rain,
        "nwx": explicit_nwx or observed == "NWX",
    }


def _event_lookup(frame: pd.DataFrame) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for _, row in frame.iterrows():
        values = list(row)
        observation_index = None
        observation_key = None
        for index, value in enumerate(values):
            parsed = _parse_observation_time(value)
            if parsed:
                observation_index = index
                observation_key = _clean_text(value)
                break
        if observation_index is None or observation_key is None:
            continue
        weather = " | ".join(
            token for token in (_clean_text(value) for value in values[:observation_index]) if token
        )
        lookup[observation_key] = weather
    return lookup


def _station_code(frame: pd.DataFrame, column: int) -> str:
    for row_index in range(min(8, len(frame.index))):
        label = _clean_text(frame.iat[row_index, 0]).lower()
        if "station number" not in label:
            continue
        value = frame.iat[row_index, column] if column < len(frame.columns) else None
        if pd.notna(value):
            return str(int(float(value)))
        match = re.search(r"(\d{5})", _clean_text(frame.iat[row_index, 0]))
        if match:
            return match.group(1)
    return "43150"


def _metric_rows(frame: pd.DataFrame) -> dict[str, int]:
    rows: dict[str, int] = {}
    for index in range(len(frame.index)):
        key = _metric_key(frame.iat[index, 0])
        if key is not None and key not in rows:
            rows[key] = index
    return rows


def parse_transposed_month(
    path: Path,
    sheet_name: str,
    events: dict[str, str],
    observation_verified: bool,
) -> list[dict]:
    frame = pd.read_excel(path, sheet_name=sheet_name, header=None)
    observation_row = next(
        (
            index
            for index in range(len(frame.index))
            if "observation time" in _clean_text(frame.iat[index, 0]).lower()
        ),
        None,
    )
    if observation_row is None:
        return []

    metric_rows = _metric_rows(frame)
    records = []
    for column in range(1, len(frame.columns)):
        observation_token = _clean_text(frame.iat[observation_row, column])
        parsed = _parse_observation_time(observation_token)
        if not parsed:
            continue
        date_text, time_text = parsed
        raw_event = events.get(observation_token, "")
        flags = _event_flags(raw_event, observation_verified)
        metrics = {
            key: _number(frame.iat[row_index, column])
            for key, row_index in metric_rows.items()
        }
        records.append(
            {
                "date": date_text,
                "time": time_text,
                "station": "Visakhapatnam",
                "station_code": _station_code(frame, column),
                **metrics,
                **flags,
                "season": _season(date_text),
                "raw_observed_event": raw_event or flags["observed"],
                "observation_status": "VERIFIED" if observation_verified else "NOT_SUPPLIED",
                "source_file": path.name,
                "source_sheet": sheet_name,
                "source_trace": f"{path.name}::{sheet_name}::{observation_token}",
            }
        )
    return records


def parse_paired_cycle_month(path: Path, sheet_name: str) -> list[dict]:
    frame = pd.read_excel(path, sheet_name=sheet_name, header=None)
    date_row = next(
        (
            index
            for index in range(len(frame.index))
            if _clean_text(frame.iat[index, 0]).lower() == "date"
        ),
        None,
    )
    observation_row = next(
        (
            index
            for index in range(len(frame.index))
            if "observation time" in _clean_text(frame.iat[index, 0]).lower()
        ),
        None,
    )
    if date_row is None or observation_row is None:
        return []

    metric_rows = _metric_rows(frame)
    records = []
    active_date = None
    for column in range(1, len(frame.columns)):
        raw_date = frame.iat[date_row, column]
        parsed_date = pd.to_datetime(raw_date, errors="coerce")
        if pd.notna(parsed_date):
            active_date = parsed_date.strftime("%Y-%m-%d")
        cycle = _clean_text(frame.iat[observation_row, column]).upper()
        if not active_date or not cycle:
            continue
        hour = "12" if cycle.startswith("12") else "00"
        observation_token = f"{active_date[2:4]}{active_date[5:7]}{active_date[8:10]}/{hour}00"
        metrics = {
            key: _number(frame.iat[row_index, column])
            for key, row_index in metric_rows.items()
        }
        records.append(
            {
                "date": active_date,
                "time": f"{hour}:00Z",
                "station": "Visakhapatnam",
                "station_code": _station_code(frame, column),
                **metrics,
                **_event_flags("", observation_verified=False),
                "season": _season(active_date),
                "raw_observed_event": "Observation event not supplied in source workbook",
                "observation_status": "NOT_SUPPLIED",
                "source_file": path.name,
                "source_sheet": sheet_name,
                "source_trace": f"{path.name}::{sheet_name}::{observation_token}",
            }
        )
    return records


def build_archive(workbooks: Iterable[Path]) -> pd.DataFrame:
    records: list[dict] = []
    for path in (Path(item) for item in workbooks):
        workbook = pd.ExcelFile(path)
        year_match = re.search(r"(2023|2024|2025)", path.name)
        year = year_match.group(1) if year_match else ""
        if year == "2023":
            events = _event_lookup(pd.read_excel(path, sheet_name="All Indices", header=None))
            monthly_sheets = [name for name in workbook.sheet_names if re.match(r"^(Mar|Apr|May|Jun)2023$", name)]
            for sheet_name in monthly_sheets:
                records.extend(parse_transposed_month(path, sheet_name, events, observation_verified=True))
        elif year == "2024":
            events = _event_lookup(pd.read_excel(path, sheet_name="Sheet1", header=None))
            monthly_sheets = [name for name in workbook.sheet_names if re.match(r"^(Mar|Apr|May|Jun)2024$", name)]
            for sheet_name in monthly_sheets:
                records.extend(parse_transposed_month(path, sheet_name, events, observation_verified=True))
        elif year == "2025":
            for sheet_name in ("May_2025", "June_2025"):
                if sheet_name in workbook.sheet_names:
                    records.extend(parse_paired_cycle_month(path, sheet_name))

    frame = pd.DataFrame(records)
    if frame.empty:
        return frame
    frame = frame.drop_duplicates(subset=["date", "time", "station_code"], keep="last")
    frame = frame.sort_values(["date", "time", "station_code"]).reset_index(drop=True)
    return frame


def write_archive(frame: pd.DataFrame, csv_path: Path, xlsx_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(csv_path, index=False, encoding="utf-8")
    frame.to_excel(xlsx_path, index=False, sheet_name="RSRW_Observations")
