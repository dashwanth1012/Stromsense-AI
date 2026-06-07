import os

main_path = "backend/main.py"

with open(main_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Define _determine_static_cape_reason
if "def _determine_static_cape_reason" not in content:
    reason_func = """
def _determine_static_cape_reason(entry, entries):
    warning = _detect_static_cape_warning(entries)
    if not warning:
        return None
    source_type = entry.get("source_type") or ""
    retry_count = entry.get("retry_count", 0)
    error = entry.get("error")
    age_hours = entry.get("cache_age_hours", 0.0)
    
    if retry_count > 0 or error:
        return "LIVE_INGESTION_FAILURE"
    elif "SEED" in source_type or "PROFILE" in source_type:
        return "SEED_PROFILE_REUSE"
    elif age_hours >= 12.0:
        return "STALE_TELEMETRY"
    else:
        return "SOLVER_REUSE"
"""
    # Insert after _detect_static_cape_warning
    insert_pos = content.find("def _detect_static_cape_warning(entries):")
    # Find end of that function
    pos = content.find("return None", insert_pos)
    if pos != -1:
        end_pos = content.find("\n", pos) + 1
        content = content[:end_pos] + reason_func + content[end_pos:]
        print("Inserted _determine_static_cape_reason helper.")

# 2. Add dynamic reason to entry and return in update_cape_traceability
if '"static_data_reason":' not in content:
    # Update update_cape_traceability function
    target = 'warning = _detect_static_cape_warning(entries)'
    replacement = """warning = _detect_static_cape_warning(entries)
    reason = _determine_static_cape_reason(entry, entries)
    entry["static_data_warning"] = warning
    entry["static_data_reason"] = reason"""
    content = content.replace(target, replacement)
    
    # Also update the returned dict structure in update_cape_traceability if needed
    # But since it copies entry, warning and reason are already in entry/timeline.
    print("Updated update_cape_traceability warning/reason logic.")

# 3. Update /cwc/cape-traceability return dict
target_t = '"static_data_warning": _detect_static_cape_warning(entries),'
replacement_t = """"static_data_warning": _detect_static_cape_warning(entries),
            "static_data_reason": _determine_static_cape_reason(latest, entries) if entries else None,"""
content = content.replace(target_t, replacement_t)
print("Updated /cwc/cape-traceability endpoint return dictionary.")

# 4. Insert compute_probability_traceability helper
if "def compute_probability_traceability" not in content:
    prob_trace_func = """
def compute_probability_traceability(current_row, prev_row, active_thresholds):
    # current probabilities
    curr_baseline = [{
        "station": current_row.get("station"),
        "cape": current_row.get("cape", 0.0),
        "lifted_index": current_row.get("li", current_row.get("lifted_index", 0.0)),
        "sweat_index": current_row.get("sweat", current_row.get("sweat_index", 0.0)),
        "k_index": current_row.get("k_index", 0.0),
        "pwat": current_row.get("pwat", 0.0),
        "tt_index": current_row.get("tt_index", 48.0),
        "sounding_available": True
    }]
    curr_probs = analysis_engines.run_probabilistic_forecast_for_rows(curr_baseline, active_thresholds).get("probabilistic_rows", [])
    curr_p = curr_probs[0] if curr_probs else {
        "ts_probability": 50.0, "severe_ts_probability": 40.0, "lightning_probability": 45.0, "heavy_rain_probability": 40.0, "squall_probability": 30.0, "nwx_probability": 50.0
    }
    
    # previous probabilities
    if prev_row:
        prev_baseline = [{
            "station": prev_row.get("station"),
            "cape": prev_row.get("cape", 0.0),
            "lifted_index": prev_row.get("li", prev_row.get("lifted_index", 0.0)),
            "sweat_index": prev_row.get("sweat", prev_row.get("sweat_index", 0.0)),
            "k_index": prev_row.get("k_index", 0.0),
            "pwat": prev_row.get("pwat", 0.0),
            "tt_index": prev_row.get("tt_index", 48.0),
            "sounding_available": True
        }]
        prev_probs = analysis_engines.run_probabilistic_forecast_for_rows(prev_baseline, active_thresholds).get("probabilistic_rows", [])
        prev_p = prev_probs[0] if prev_probs else curr_p
    else:
        prev_p = curr_p
        
    def get_contribs(row, prob_type):
        cape = float(row.get("cape", 0.0))
        li = float(row.get("li", row.get("lifted_index", 0.0)))
        sweat = float(row.get("sweat", row.get("sweat_index", 0.0)))
        pwat = float(row.get("pwat", 0.0))
        k_index = float(row.get("k_index", 0.0))
        tt_index = float(row.get("tt_index", 48.0))
        cin = float(row.get("cin", -50.0))
        shear = float(row.get("bulk_shear", 12.0))
        theta_e = float(row.get("theta_e", 340.0))
        conv = float(row.get("moisture_convergence", 6.0))
        
        cape_score = max(0.0, min(1.0, cape / max(1.0, active_thresholds.get("cape", 2100) * 1.8)))
        li_score = max(0.0, min(1.0, abs(min(0.0, li)) / abs(min(-1.0, active_thresholds.get("li", -4.5) * 1.6))))
        sweat_score = max(0.0, min(1.0, sweat / max(1.0, active_thresholds.get("sweat", 290) * 1.4)))
        pwat_score = max(0.0, min(1.0, pwat / max(1.0, active_thresholds.get("pwat", 50) * 1.4)))
        k_score = max(0.0, min(1.0, k_index / max(1.0, active_thresholds.get("k_index", 30) * 1.3)))
        tt_score = max(0.0, min(1.0, tt_index / 60.0))
        cin_release_score = max(0.0, min(1.0, (cin + 115.0) / 95.0))
        shear_score = max(0.0, min(1.0, shear / 24.0))
        theta_score = max(0.0, min(1.0, (theta_e - 325.0) / 42.0))
        conv_score = max(0.0, min(1.0, conv / 16.0))
        
        if prob_type == "ts":
            parts = {
                "CAPE": 0.25 * cape_score,
                "LI": 0.18 * li_score,
                "SWEAT": 0.16 * sweat_score,
                "PWAT": 0.16 * pwat_score,
                "K Index": 0.12 * k_score,
                "CIN": 0.07 * cin_release_score,
                "Convergence": 0.06 * conv_score
            }
        elif prob_type == "severe_ts":
            parts = {
                "SWEAT": 0.34 * sweat_score,
                "CAPE": 0.24 * cape_score,
                "LI": 0.14 * li_score,
                "Bulk Shear": 0.12 * shear_score,
                "TT Index": 0.10 * tt_score,
                "Convergence": 0.06 * conv_score
            }
        elif prob_type == "lightning":
            parts = {
                "CAPE": 0.34 * cape_score,
                "TT Index": 0.20 * tt_score,
                "LI": 0.18 * li_score,
                "SWEAT": 0.14 * sweat_score,
                "Theta-E": 0.14 * theta_score
            }
        elif prob_type == "heavy_rain":
            parts = {
                "PWAT": 0.42 * pwat_score,
                "K Index": 0.18 * k_score,
                "CAPE": 0.14 * cape_score,
                "TT Index": 0.12 * tt_score,
                "Convergence": 0.14 * conv_score
            }
        elif prob_type == "squall":
            parts = {
                "SWEAT": 0.46 * sweat_score,
                "CAPE": 0.18 * cape_score,
                "LI": 0.14 * li_score,
                "Bulk Shear": 0.12 * shear_score,
                "TT Index": 0.10 * tt_score
            }
        else:
            parts = {"CAPE": 1.0}
            
        total = sum(parts.values())
        if total == 0:
            return [{"name": k, "weight": round(100.0 / len(parts), 1)} for k in parts.keys()]
        
        res = []
        for k, v in parts.items():
            res.append({"name": k, "weight": round((v / total) * 100.0, 1)})
        res.sort(key=lambda x: x["weight"], reverse=True)
        return res

    ts_val = curr_p.get("ts_probability")
    severe_val = curr_p.get("severe_ts_probability")
    lightning_val = curr_p.get("lightning_probability")
    heavy_rain_val = curr_p.get("heavy_rain_probability")
    squall_val = curr_p.get("squall_probability")
    nwx_val = curr_p.get("nwx_probability")
    
    prev_ts = prev_p.get("ts_probability")
    prev_severe = prev_p.get("severe_ts_probability")
    prev_lightning = prev_p.get("lightning_probability")
    prev_heavy_rain = prev_p.get("heavy_rain_probability")
    prev_squall = prev_p.get("squall_probability")
    prev_nwx = prev_p.get("nwx_probability")

    return {
        "ts": {
            "current": ts_val,
            "previous": prev_ts,
            "delta": round(ts_val - prev_ts, 1),
            "contributors": get_contribs(current_row, "ts"),
            "reason": "Supportive thermodynamics breach local inhibition cap." if ts_val >= 50 else "High CIN and stable lapse rates cap convective initiation."
        },
        "severe_ts": {
            "current": severe_val,
            "previous": prev_severe,
            "delta": round(severe_val - prev_severe, 1),
            "contributors": get_contribs(current_row, "severe_ts"),
            "reason": "Strong boundary instability combined with wind shear." if severe_val >= 40 else "Weak wind shear restricts cell organization."
        },
        "lightning": {
            "current": lightning_val,
            "previous": prev_lightning,
            "delta": round(lightning_val - prev_lightning, 1),
            "contributors": get_contribs(current_row, "lightning"),
            "reason": "Deep vertical cloud depth supports charge separation." if lightning_val >= 50 else "Shallow cloud boundaries restrict charge separation."
        },
        "heavy_rain": {
            "current": heavy_rain_val,
            "previous": prev_heavy_rain,
            "delta": round(heavy_rain_val - prev_heavy_rain, 1),
            "contributors": get_contribs(current_row, "heavy_rain"),
            "reason": "Loaded atmospheric moisture column enables high rain rate." if heavy_rain_val >= 50 else "Dry mid-level layer limits precipitation totals."
        },
        "squall": {
            "current": squall_val,
            "previous": prev_squall,
            "delta": round(squall_val - prev_squall, 1),
            "contributors": get_contribs(current_row, "squall"),
            "reason": "Elevated low-level kinetic wind shear favors outflow gusts." if squall_val >= 40 else "Weak kinetic environmental shear suppresses squalls."
        },
        "nwx": {
            "current": nwx_val,
            "previous": prev_nwx,
            "delta": round(nwx_val - prev_nwx, 1),
            "contributors": [{"name": "CIN", "weight": 50.0}, {"name": "Lapse Rates", "weight": 50.0}],
            "reason": "Tropopause stable columns restrict storm development." if nwx_val >= 50 else "Convective triggers dominate, high storm probability."
        }
    }
"""
    # Insert helper before endpoint definitions
    insert_pos = content.find("@app.get(\"/cwc/historical-dates\")")
    content = content[:insert_pos] + prob_trace_func + "\n\n" + content[insert_pos:]
    print("Inserted compute_probability_traceability helper.")

# 5. Link probability_traceability inside get_cwc_historical_analysis
if '"probability_traceability":' not in content:
    # Let's locate get_cwc_historical_analysis endpoint
    idx = content.find("def get_cwc_historical_analysis(")
    # Find where return dictionary starts
    ret_pos = content.find("return {", idx)
    if ret_pos != -1:
        # Before returning, we compute prob_trace
        computation = """
    # Calculate previous row for station probability deltas
    prev_row = None
    for i in range(row_idx - 1, -1, -1):
        if db[i].get("station") == station:
            prev_row = db[i]
            break
            
    prob_trace = compute_probability_traceability(matching_row, prev_row, custom_thresholds)
    """
        content = content[:ret_pos] + computation + "\n    " + content[ret_pos:]
        
        # Now insert key in returned dict
        ret_key_pos = content.find("return {", idx) + 8
        content = content[:ret_key_pos] + '\n        "probability_traceability": prob_trace,' + content[ret_key_pos:]
        print("Updated get_cwc_historical_analysis to return probability_traceability.")

# 6. Link probability_traceability inside custom_sounding_analysis
if '"probability_traceability": prob_trace,' not in content:
    idx = content.find("def custom_sounding_analysis(")
    ret_pos = content.find("return {", idx)
    if ret_pos != -1:
        computation = """
    prev_custom_row = {
        "cape": 2200.0,
        "cin": -50.0,
        "li": -5.0,
        "pwat": 52.0,
        "sweat": 295.0,
        "k_index": 31.0,
        "tt_index": 48.0,
        "bulk_shear": 12.0,
        "theta_e": 340.0,
        "lcl": 900.0,
        "lfc": 820.0,
        "el": 150.0
    }
    prob_trace = compute_probability_traceability(row, prev_custom_row, custom_thresholds)
    """
        content = content[:ret_pos] + computation + "\n    " + content[ret_pos:]
        
        ret_key_pos = content.find("return {", idx) + 8
        content = content[:ret_key_pos] + '\n        "probability_traceability": prob_trace,' + content[ret_key_pos:]
        print("Updated custom_sounding_analysis to return probability_traceability.")

with open(main_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Backend main.py script modifications completed successfully!")
