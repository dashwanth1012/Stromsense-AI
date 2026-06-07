import os
import sys
import json
import pandas as pd

# Add backend to path
sys.path.insert(0, os.path.abspath("backend"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def to_markdown_custom(df):
    headers = list(df.columns)
    markdown_lines = []
    markdown_lines.append("| " + " | ".join(headers) + " |")
    markdown_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for idx, row in df.iterrows():
        vals = [str(row[h]).replace("\n", " ") for h in headers]
        markdown_lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(markdown_lines)

# Prepare content lists
output_sections = []

# 1. GENERATE DYNAMICITY PROOF (For 2025-05-10 across all 5 stations)
output_sections.append("=" * 80)
output_sections.append("SECTION 7: DYNAMICITY PROOF FOR 2025-05-10")
output_sections.append("=" * 80)

stations = ["Visakhapatnam", "Machilipatnam", "Chennai", "Kolkata", "Hyderabad"]
date = "2025-05-10"

dyn_rows = []
for station in stations:
    res = client.get(f"/cwc/historical-analysis?date={date}&station={station}")
    if res.status_code != 200:
        output_sections.append(f"Error fetching for {station}")
        continue
    data = res.json()
    raw_params = data.get("raw_parameters", {})
    prob_trace = data.get("probability_traceability", {})
    explanation = data.get("meteorologist_explanation", {})
    forecast_vs_obs = data.get("forecast_vs_observed", {})
    
    cape = raw_params.get("CAPE (J/kg)")
    li = raw_params.get("LI (K)") # Corrected key
    pwat = raw_params.get("PWAT (mm)")
    ts_prob = prob_trace.get("ts", {}).get("current")
    analog_date = explanation.get("analog_ref", {}).get("date")
    analog_sim = data.get("analog_similarity")
    outcome = forecast_vs_obs.get("forecast_event")
    
    triggers = ", ".join([t["name"] + f" ({t['weight']}%)" for t in data.get("trigger_contributions", [])[:2]])
    narrative_snippet = explanation.get("imd_scientific_explanation", "")[:60] + "..."
    
    dyn_rows.append({
        "Station": station,
        "CAPE": cape,
        "LI": li,
        "PWAT": pwat,
        "TS Prob": f"{ts_prob}%",
        "Triggers": triggers,
        "Outcome": outcome,
        "Analog": f"{analog_date} ({analog_sim}%)",
        "Narrative": narrative_snippet
    })

df_dyn = pd.DataFrame(dyn_rows)
output_sections.append(to_markdown_custom(df_dyn))

# 2. GENERATE CAPE AUDIT (For 5 distinct dates/stations)
output_sections.append("\n" + "=" * 80)
output_sections.append("SECTION 8: CAPE AUDIT")
output_sections.append("=" * 80)

cases = [
    {"date": "2025-04-12", "station": "Visakhapatnam"},
    {"date": "2025-05-10", "station": "Machilipatnam"},
    {"date": "2025-06-18", "station": "Chennai"},
    {"date": "2025-07-22", "station": "Kolkata"},
    {"date": "2025-08-12", "station": "Hyderabad"}
]

cape_rows = []
for c in cases:
    res = client.get(f"/cwc/historical-analysis?date={c['date']}&station={c['station']}")
    if res.status_code != 200:
        continue
    data = res.json()
    evolution = data.get("evolution", {})
    t1 = evolution.get("t_minus_1", {}).get("cape", 0)
    t0 = evolution.get("t_zero", {}).get("cape", 0)
    tp1 = evolution.get("t_plus_1", {}).get("cape", 0)
    
    # Calculate derived values (from frontend logic)
    delta = t0 - t1
    trend = "RISING" if t0 > t1 else "FALLING" if t0 < t1 else "STEADY"
    
    if t1 == t0 and t0 == tp1:
        if t0 == 0:
            reason_code = "INGESTION_FAILURE_FALLBACK"
        elif t0 == 1200:
            reason_code = "STALE_CACHE_DETECTION"
        else:
            reason_code = "STATIC_CACHE_LOCK"
    else:
        reason_code = "DYNAMIC_TELEMETRY_SYNC"
        
    cape_rows.append({
        "Date": c["date"],
        "Station": c["station"],
        "T-1 CAPE": t1,
        "T0 CAPE": t0,
        "T+1 CAPE": tp1,
        "Delta": delta,
        "Trend": trend,
        "Reason Code": reason_code
    })

df_cape = pd.DataFrame(cape_rows)
output_sections.append(to_markdown_custom(df_cape))

# 3. GENERATE PROBABILITY AUDIT (For same 5 cases)
output_sections.append("\n" + "=" * 80)
output_sections.append("SECTION 9: PROBABILITY AUDIT")
output_sections.append("=" * 80)

prob_rows = []
for c in cases:
    res = client.get(f"/cwc/historical-analysis?date={c['date']}&station={c['station']}")
    if res.status_code != 200:
        continue
    data = res.json()
    prob_trace = data.get("probability_traceability", {})
    ts = prob_trace.get("ts", {}).get("current")
    lightning = prob_trace.get("lightning", {}).get("current")
    heavy_rain = prob_trace.get("heavy_rain", {}).get("current")
    severe_ts = prob_trace.get("severe_ts", {}).get("current")
    squall = prob_trace.get("squall", {}).get("current")
    
    weights = data.get("trigger_contributions", [])
    weight_dict = {w["name"]: f"{w['weight']}%" for w in weights}
    
    prob_rows.append({
        "Date": c["date"],
        "Station": c["station"],
        "TS Prob": ts,
        "LT Prob": lightning,
        "HR Prob": heavy_rain,
        "STS Prob": severe_ts,
        "SQ Prob": squall,
        "Weights (CAPE/LI/PW/SW/BS/TE)": f"CAPE: {weight_dict.get('CAPE', '0%')} | LI: {weight_dict.get('LI', '0%')} | PWAT: {weight_dict.get('PWAT', '0%')} | SWEAT: {weight_dict.get('SWEAT', '0%')} | Shear: {weight_dict.get('Bulk Shear', '0%')} | Theta-E: {weight_dict.get('Theta-E', '0%')}"
    })

df_prob = pd.DataFrame(prob_rows)
output_sections.append(to_markdown_custom(df_prob))

# Write to file
out_path = r"C:\Users\USER\.gemini\antigravity\brain\3a369011-49b3-4032-bc60-3c0d94fe34dc\scratch\audit_output.txt"
with open(out_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(output_sections))

print("Audit data generated successfully inside python script!")
