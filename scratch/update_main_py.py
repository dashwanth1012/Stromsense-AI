import os

path = 'backend/main.py'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

search1 = """@app.get("/cwc/historical-dates")
def get_cwc_historical_dates(file_name: str = None):
    db = analysis_engines.load_historical_observations(file_name=file_name)
    dates = []
    for r in db:
        is_storm = bool(r.get("thunderstorm"))
        dates.append({
            "date": r.get("date"),
            "station": r.get("station"),
            "station_code": r.get("station_code"),
            "observed": r.get("observed"),
            "thunderstorm": r.get("thunderstorm"),
            "lightning": r.get("lightning"),
            "squall": r.get("squall"),
            "rainfall": r.get("rainfall"),
            "nwx": r.get("nwx"),
            "season": r.get("season"),
            "cape": float(r.get("cape", 0.0)),
            "li": float(r.get("li", 0.0)),
            "pwat": float(r.get("pwat", 0.0)),
            "sweat": float(r.get("sweat", 0.0)),
            "bulk_shear": 19.8 if is_storm else 12.0,
            "theta_e": 360.5 if is_storm else 340.0,
        })
    dates.sort(key=lambda x: x["date"], reverse=True)
    return dates"""

replace1 = """@app.get("/cwc/historical-dates")
def get_cwc_historical_dates(file_name: str = None):
    db = analysis_engines.load_historical_observations(file_name=file_name)
    dates = []
    for r in db:
        is_storm = bool(r.get("thunderstorm"))
        db_time = str(r.get("time", ""))
        std_time = "05:00 IST" if ("00:00" in db_time or "00Z" in db_time) else "17:00 IST"
        dates.append({
            "date": r.get("date"),
            "time": std_time,
            "station": r.get("station"),
            "station_code": r.get("station_code"),
            "observed": r.get("observed"),
            "thunderstorm": r.get("thunderstorm"),
            "lightning": r.get("lightning"),
            "squall": r.get("squall"),
            "rainfall": r.get("rainfall"),
            "nwx": r.get("nwx"),
            "season": r.get("season"),
            "cape": float(r.get("cape", 0.0)),
            "li": float(r.get("li", 0.0)),
            "pwat": float(r.get("pwat", 0.0)),
            "sweat": float(r.get("sweat", 0.0)),
            "bulk_shear": 19.8 if is_storm else 12.0,
            "theta_e": 360.5 if is_storm else 340.0,
        })
    dates.sort(key=lambda x: x["date"], reverse=True)
    return dates"""

search2 = '"observation_timestamp": f"{date} {matching_row.get(\'time\')}",'
replace2 = '"observation_timestamp": f"{date} " + ("05:00 IST" if ("00:00" in str(matching_row.get(\'time\', \'\')) or "00Z" in str(matching_row.get(\'time\', \'\'))) else "17:00 IST"),'

if search1 in content:
    content = content.replace(search1, replace1)
    print("Search 1 replaced successfully.")
else:
    print("Search 1 NOT found!")

if search2 in content:
    content = content.replace(search2, replace2)
    print("Search 2 replaced successfully.")
else:
    print("Search 2 NOT found!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved main.py.")
