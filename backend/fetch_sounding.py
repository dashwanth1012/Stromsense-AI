"""Operational Wyoming sounding ingestion and cache management.

This module is intentionally side-effect free on import. The FastAPI layer calls
``get_cycle_sounding`` from the cycle-locked forecast workflow and from the
background cache refresher.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests
from bs4 import BeautifulSoup


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDINGS_DIR = os.path.join(BASE_DIR, "data", "soundings")
DEFAULT_TIMEOUT_SECONDS = 6
LIVE_ATTEMPT_COOLDOWN_MINUTES = 30


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _format_age(seconds: Optional[float]) -> str:
    if seconds is None:
        return "UNKNOWN"
    seconds = max(0, int(seconds))
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    if hours < 48:
        return f"{hours}h {minutes % 60}m"
    days = hours // 24
    return f"{days}d {hours % 24}h"


def _cycle_hour(cycle: str) -> int:
    return 0 if str(cycle).upper() == "00Z" else 12


def _cache_path(station_code: str, cycle: str) -> str:
    os.makedirs(SOUNDINGS_DIR, exist_ok=True)
    return os.path.join(SOUNDINGS_DIR, f"{station_code}_{cycle}.txt")


def _metadata_path(station_code: str, cycle: str) -> str:
    return os.path.join(SOUNDINGS_DIR, f"{station_code}_{cycle}.metadata.json")


def _read_metadata(station_code: str, cycle: str) -> dict:
    path = _metadata_path(station_code, cycle)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return {}


def _write_metadata(station_code: str, cycle: str, metadata: dict) -> None:
    os.makedirs(SOUNDINGS_DIR, exist_ok=True)
    tmp_path = _metadata_path(station_code, cycle) + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
    os.replace(tmp_path, _metadata_path(station_code, cycle))


def _cache_age_seconds(path: str) -> Optional[float]:
    if not os.path.exists(path):
        return None
    return (_utcnow().timestamp() - os.path.getmtime(path))


def build_wyoming_url(station_code: str, cycle: str, target_date: datetime) -> str:
    hour = _cycle_hour(cycle)
    from_to = f"{target_date.day:02d}{hour:02d}"
    return (
        "https://weather.uwyo.edu/cgi-bin/sounding?"
        f"region=seasia&TYPE=TEXT:LIST&YEAR={target_date.year}"
        f"&MONTH={target_date.month:02d}&FROM={from_to}&TO={from_to}&STNM={station_code}"
    )


def _extract_sounding_text(html: str) -> Optional[str]:
    soup = BeautifulSoup(html or "", "html.parser")
    pre_tag = soup.find("pre")
    text = pre_tag.get_text("\n") if pre_tag else soup.get_text("\n")
    if "PRES" in text and "HGHT" in text and ("Station" in text or "Observation time" in text):
        return text.strip() + "\n"
    return None


def _cycle_candidates(cycle: str, now_utc: Optional[datetime] = None) -> list[datetime]:
    now_utc = now_utc or _utcnow()
    hour = _cycle_hour(cycle)
    candidates = []
    for day_offset in range(3):
        candidate = now_utc - timedelta(days=day_offset)
        if day_offset == 0 and now_utc.hour < hour:
            continue
        candidates.append(candidate.replace(hour=hour, minute=0, second=0, microsecond=0))
    return candidates


def fetch_wyoming_sounding(
    station_code: str,
    cycle: str,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    now_utc: Optional[datetime] = None,
) -> dict:
    """Fetch the latest available Wyoming sounding text for a station/cycle."""
    now = now_utc or _utcnow()
    last_error = None
    for target in _cycle_candidates(cycle, now):
        url = build_wyoming_url(station_code, cycle, target)
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code != 200:
                last_error = f"HTTP {response.status_code}"
                continue
            raw_text = _extract_sounding_text(response.text)
            if not raw_text:
                last_error = "Wyoming response did not include a valid sounding table."
                continue
            return {
                "source_status": "LIVE",
                "source_type": "WYOMING_LIVE",
                "station": station_code,
                "cycle_time": target.strftime("%Y-%m-%d %H:%M UTC"),
                "last_update": _iso(now),
                "fetch_timestamp": _iso(now),
                "cache_age": "0s",
                "fetch_url": url,
                "raw_text": raw_text,
                "error": None,
            }
        except Exception as exc:
            last_error = str(exc)

    return {
        "source_status": "FAILED",
        "source_type": "WYOMING_LIVE",
        "station": station_code,
        "cycle_time": None,
        "last_update": _iso(now),
        "fetch_timestamp": _iso(now),
        "cache_age": "UNKNOWN",
        "fetch_url": None,
        "raw_text": None,
        "error": last_error or "No Wyoming sounding candidate returned data.",
    }


def compute_freshness_score(source_status: str, age_seconds: Optional[float], source_type: str = "") -> int:
    """Calculate data freshness score (0-100) based on source and age."""
    if source_status == "LIVE":
        return 100
    if source_status == "FALLBACK" or source_type in ("SEEDED_FALLBACK", "PROFILE_FALLBACK", "ISOLATED_PROFILE_FALLBACK"):
        return 10
    if age_seconds is None:
        return 10
    
    age_hours = age_seconds / 3600.0
    if age_hours > 72.0: # Older than 3 days
        return 5
        
    if age_hours <= 12.0:
        return max(20, round(90 * (1.0 - (age_hours / 12.0))))
    else:
        return max(5, round(20 * (1.0 - (age_hours / 24.0))))


def update_calculation_timestamp(station_code: str, cycle: str) -> None:
    """Updates the last successful thermodynamic calculation timestamp in cache metadata."""
    meta = _read_metadata(station_code, cycle)
    meta["last_successful_calculation"] = _iso(_utcnow())
    _write_metadata(station_code, cycle, meta)


def _read_cache(station_code: str, cycle: str) -> dict:
    path = _cache_path(station_code, cycle)
    metadata = _read_metadata(station_code, cycle)
    raw_text = None
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as handle:
            raw_text = handle.read()

    age_seconds = _cache_age_seconds(path)
    file_update = None
    if os.path.exists(path):
        file_update = _iso(datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc))

    age_hours = round(age_seconds / 3600.0, 2) if age_seconds is not None else None
    
    # Establish source status: LIVE (from this run), CACHE (recent cache file), or FALLBACK (old/seeded cache or missing)
    raw_status = metadata.get("source_status")
    source_type = metadata.get("source_type") or ("LOCAL_SOUNDING_CACHE" if raw_text else "NO_CACHE")
    
    if not raw_text:
        source_status = "FALLBACK"
    elif age_hours is not None and age_hours > 24.0:
        source_status = "FALLBACK"
    elif source_type in ("SEEDED_CACHE", "PROFILE_FALLBACK", "ISOLATED_PROFILE_FALLBACK"):
        source_status = "FALLBACK"
    else:
        source_status = "CACHE"
        
    freshness = compute_freshness_score(source_status, age_seconds, source_type)
    
    # Trace successful downloads
    last_success_dl = metadata.get("last_successful_download")
    if source_status == "LIVE" and not last_success_dl:
        last_success_dl = file_update or _iso(_utcnow())
    elif not last_success_dl and raw_text and source_status == "CACHE":
        last_success_dl = file_update

    return {
        "raw_text": raw_text,
        "metadata": {
            **metadata,
            "source_status": source_status,
            "source_type": source_type,
            "station": station_code,
            "cycle_time": metadata.get("cycle_time"),
            "last_update": metadata.get("last_update") or file_update,
            "fetch_timestamp": metadata.get("fetch_timestamp"),
            "cache_age": _format_age(age_seconds),
            "cache_age_hours": age_hours,
            "freshness_score": freshness,
            "last_successful_download": last_success_dl,
            "last_successful_calculation": metadata.get("last_successful_calculation"),
            "retry_count": metadata.get("retry_count", 0),
            "sounding_file": path,
            "error": metadata.get("error"),
        },
    }


def _refresh_due(cache_info: dict, max_cache_age_minutes: int) -> bool:
    metadata = cache_info.get("metadata", {})
    raw_text = cache_info.get("raw_text")
    if not raw_text:
        return True

    now = _utcnow()
    attempt = metadata.get("last_live_attempt") or metadata.get("fetch_timestamp")
    if attempt:
        try:
            parsed = datetime.fromisoformat(attempt.replace("Z", "+00:00"))
            if (now - parsed) < timedelta(minutes=LIVE_ATTEMPT_COOLDOWN_MINUTES):
                return False
        except Exception:
            pass

    age_seconds = _cache_age_seconds(metadata.get("sounding_file", ""))
    if age_seconds is None:
        return True
    if age_seconds > max_cache_age_minutes * 60:
        return True
    return metadata.get("source_type") in {None, "", "LOCAL_SOUNDING_CACHE", "SEEDED_CACHE"}


def write_cache(station_code: str, cycle: str, raw_text: str, metadata: dict) -> str:
    path = _cache_path(station_code, cycle)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(raw_text)
    
    meta = {
        **metadata,
        "source_status": "LIVE",
        "source_type": "WYOMING_LIVE",
        "station": station_code,
        "cache_age": "0s",
        "cache_age_hours": 0.0,
        "freshness_score": 100,
        "sounding_file": path,
        "last_live_attempt": _iso(_utcnow()),
        "last_successful_download": _iso(_utcnow()),
        "retry_count": 0,
    }
    _write_metadata(station_code, cycle, meta)
    return path


def get_cycle_sounding(
    station_code: str,
    cycle: str,
    prefer_live: bool = True,
    max_cache_age_minutes: int = 360,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict:
    """Return raw sounding text plus live/cache traceability metadata."""
    cycle = str(cycle).upper()
    cache_info = _read_cache(station_code, cycle)

    if prefer_live and _refresh_due(cache_info, max_cache_age_minutes):
        live = fetch_wyoming_sounding(station_code, cycle, timeout=timeout)
        if live.get("raw_text"):
            path = write_cache(station_code, cycle, live["raw_text"], live)
            # Re-read cache to get all computed freshness attributes
            return _read_cache(station_code, cycle)

        # Scrape failed, update retry attempt counts in existing cache metadata
        fallback = _read_cache(station_code, cycle)
        fallback_meta = fallback.get("metadata", {})
        retry_val = fallback_meta.get("retry_count", 0) + 1
        
        fallback_meta.update({
            "last_live_attempt": _iso(_utcnow()),
            "fetch_timestamp": live.get("fetch_timestamp"),
            "retry_count": retry_val,
            "error": live.get("error"),
        })
        _write_metadata(station_code, cycle, fallback_meta)
        fallback["metadata"] = fallback_meta
        return fallback

    return cache_info
