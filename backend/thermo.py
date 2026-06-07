import math
import os
import re

def parse_sounding_indices(text: str) -> dict:
    """
    Parse University of Wyoming sounding footer indices (authoritative for operational cycle lock).
    """
    patterns = {
        "cape": r"Convective Available Potential Energy:\s*(-?\d+\.?\d*)",
        "cin": r"Convective Inhibition:\s*(-?\d+\.?\d*)",
        "lifted_index": r"Lifted index:\s*(-?\d+\.?\d*)",
        "sweat_index": r"SWEAT index:\s*(-?\d+\.?\d*)",
        "k_index": r"K index:\s*(-?\d+\.?\d*)",
        "pwat": r"Precipitable water \[mm\] for entire sounding:\s*(-?\d+\.?\d*)",
        "tt_index": r"Totals totals index:\s*(-?\d+\.?\d*)",
        "lcl": r"Pres \[hPa\] of the Lifted Condensation Level:\s*(-?\d+\.?\d*)",
        "lfc": r"Level of Free Convection:\s*(-?\d+\.?\d*)",
        "el": r"Equilibrum Level:\s*(-?\d+\.?\d*)",
    }
    indices = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                indices[key] = float(match.group(1))
            except ValueError:
                pass
    return indices


def parse_sounding_text(text):
    """
    Parses a raw University of Wyoming sounding text block and returns a list of dictionaries,
    each containing the parsed atmospheric columns.
    """
    lines = text.split('\n')
    data = []
    in_table = False
    
    for line in lines:
        if 'PRES' in line and 'HGHT' in line and 'TEMP' in line:
            in_table = True
            continue
        if in_table:
            if '---' in line:
                continue
            if 'Station number' in line or 'Station information' in line or 'Interested in' in line:
                in_table = False
                continue
            parts = line.split()
            if len(parts) >= 4:
                try:
                    # Minimum columns required are pressure, height, temperature, dewpoint
                    pres = float(parts[0])
                    hght = float(parts[1])
                    temp = float(parts[2])
                    dwpt = float(parts[3])
                    
                    relh = float(parts[4]) if len(parts) > 4 and parts[4] != "" else None
                    mixr = float(parts[5]) if len(parts) > 5 and parts[5] != "" else None
                    drct = float(parts[6]) if len(parts) > 6 and parts[6] != "" else None
                    sknt = float(parts[7]) if len(parts) > 7 and parts[7] != "" else None
                    thta = float(parts[8]) if len(parts) > 8 and parts[8] != "" else None
                    thte = float(parts[9]) if len(parts) > 9 and parts[9] != "" else None
                    thtv = float(parts[10]) if len(parts) > 10 and parts[10] != "" else None
                    
                    data.append({
                        "pres": pres, "hght": hght, "temp": temp, "dwpt": dwpt,
                        "relh": relh, "mixr": mixr, "drct": drct, "sknt": sknt,
                        "thta": thta, "thte": thte, "thtv": thtv
                    })
                except ValueError:
                    pass
    return data

def sat_vapor_pressure(temp_c):
    """Returns saturation vapor pressure in hPa using Bolton's formula"""
    return 6.112 * math.exp((17.67 * temp_c) / (temp_c + 243.5))

def mixing_ratio(pres_hpa, temp_c):
    """Returns mixing ratio in g/kg"""
    es = sat_vapor_pressure(temp_c)
    w = 0.622 * es / (pres_hpa - es)
    return w * 1000.0

def virtual_temperature(temp_c, w_g_kg):
    """Returns virtual temperature in Kelvin"""
    w_val = w_g_kg / 1000.0
    temp_k = temp_c + 273.15
    return temp_k * (1.0 + 0.61 * w_val)

def moist_lapse_rate(p_hpa, t_k):
    """
    Computes moist adiabatic lapse rate dT/dp in K/hPa
    """
    t_c = t_k - 273.15
    es = sat_vapor_pressure(t_c)
    ws = 0.622 * es / (p_hpa - es)
    
    # Constants
    Rd = 287.05
    Rv = 461.5
    Cp = 1005.7
    Lv = 2.501e6
    
    numerator = (Rd * t_k / (p_hpa * 100.0)) * (1.0 + (Lv * ws) / (Rd * t_k))
    denominator = Cp + (Lv**2 * ws * 0.622) / (Rv * t_k**2)
    
    # dT/dp (K/Pa) -> convert to K/hPa (multiply by 100.0)
    dT_dp = (numerator / denominator) * 100.0
    return dT_dp

def integrate_moist_adiabat(p_start, t_start_k, p_end, step_hpa=1.0):
    """
    Integrates parcel temperature along a moist adiabat from p_start to p_end
    """
    p = p_start
    t = t_start_k
    
    # Determine direction of step
    direction = -1.0 if p_end < p_start else 1.0
    dp = direction * step_hpa
    
    while (direction == -1.0 and p > p_end) or (direction == 1.0 and p < p_end):
        if (direction == -1.0 and p + dp < p_end) or (direction == 1.0 and p + dp > p_end):
            dp = p_end - p
        
        # Runge-Kutta 2nd Order integration
        k1 = moist_lapse_rate(p, t)
        k2 = moist_lapse_rate(p + dp, t + k1 * dp)
        t += 0.5 * (k1 + k2) * dp
        p += dp
        
    return t

def solve_thermodynamics(sounding_data):
    """
    Computes LCL, LFC, EL, CAPE, and CIN for a parsed sounding dataset.
    Uses parcel theory with virtual temperature correction.
    """
    if not sounding_data or len(sounding_data) < 2:
        return {"cape": 0, "cin": 0, "lcl": 900.0, "lfc": 800.0, "el": 150.0, "parcel_path": []}
    
    # Extract surface parcel coordinates
    sfc = sounding_data[0]
    p0 = sfc["pres"]
    t0 = sfc["temp"]
    td0 = sfc["dwpt"]
    
    t0_k = t0 + 273.15
    td0_k = td0 + 273.15
    
    # 1. Compute LCL Pressure and Temp (Bolton's formula)
    t_lcl_k = 1.0 / (1.0 / (td0_k - 56.0) + math.log(t0_k / td0_k) / 800.0) + 56.0
    p_lcl = p0 * ((t_lcl_k / t0_k) ** 3.5)
    t_lcl_c = t_lcl_k - 273.15
    
    # Mixing ratio of the parcel (remains constant before condensation)
    w_parcel_sfc = mixing_ratio(p0, td0)
    
    # 2. Trace parcel ascent path for all sounding pressure levels
    parcel_path = []
    lfc_pres = None
    el_pres = None
    
    # Perform calculation at each sounding layer
    for layer in sounding_data:
        p = layer["pres"]
        t_env = layer["temp"]
        td_env = layer["dwpt"]
        hght = layer["hght"]
        
        # Environmental mixing ratio and virtual temp
        w_env = mixing_ratio(p, td_env)
        t_ve_k = virtual_temperature(t_env, w_env)
        
        # Parcel temperature at pressure p
        if p >= p_lcl:
            # Dry adiabatic expansion
            t_p_k = t0_k * ((p / p0) ** 0.286)
            w_p = w_parcel_sfc
        else:
            # Moist adiabatic expansion starting from LCL
            t_p_k = integrate_moist_adiabat(p_lcl, t_lcl_k, p)
            w_p = mixing_ratio(p, t_p_k - 273.15)
            
        t_vp_k = virtual_temperature(t_p_k - 273.15, w_p)
        
        buoyancy = t_vp_k - t_ve_k
        
        parcel_path.append({
            "pres": p,
            "hght": hght,
            "t_env": t_env,
            "t_ve": t_ve_k - 273.15,
            "t_parcel": t_p_k - 273.15,
            "t_vp": t_vp_k - 273.15,
            "buoyancy": buoyancy
        })
        
    # Find LFC (first buoyant level above LCL) and EL (first neutral level above LFC)
    for layer in parcel_path:
        p = layer["pres"]
        buoy = layer["buoyancy"]
        if p < p_lcl and buoy > 0 and lfc_pres is None:
            lfc_pres = p
        if lfc_pres is not None and p < lfc_pres and buoy <= 0 and el_pres is None:
            el_pres = p

    if lfc_pres is None:
        lfc_pres = p_lcl
    if el_pres is None:
        el_pres = sounding_data[-1]["pres"]

    # Integrate positive buoyancy (CAPE) between LFC and EL; negative below LFC (CIN)
    cape = 0.0
    cin = 0.0
    g = 9.81

    for i in range(len(parcel_path) - 1):
        p1 = parcel_path[i]["pres"]
        p2 = parcel_path[i + 1]["pres"]
        h1 = parcel_path[i]["hght"]
        h2 = parcel_path[i + 1]["hght"]

        buoy1 = parcel_path[i]["buoyancy"]
        buoy2 = parcel_path[i + 1]["buoyancy"]

        t_ve1 = parcel_path[i]["t_ve"] + 273.15
        t_ve2 = parcel_path[i + 1]["t_ve"] + 273.15

        dz = h2 - h1
        if dz <= 0:
            continue

        b1 = g * buoy1 / t_ve1
        b2 = g * buoy2 / t_ve2
        b_avg = 0.5 * (b1 + b2)
        p_mid = 0.5 * (p1 + p2)

        if lfc_pres >= p_mid >= el_pres and b_avg > 0:
            cape += b_avg * dz
        elif p_mid >= lfc_pres and b_avg < 0:
            cin += b_avg * dz
                
    buoyant_layers = [p for p in parcel_path if p["buoyancy"] > 0]
    if buoyant_layers:
        instability_layer_depth = round(max(p["hght"] for p in buoyant_layers) - min(p["hght"] for p in buoyant_layers), 1)
    else:
        instability_layer_depth = 0.0

    max_buoyancy = max([p["buoyancy"] for p in parcel_path], default=0.0)
    min_buoyancy = min([p["buoyancy"] for p in parcel_path], default=0.0)

    if cape < 100 and instability_layer_depth < 1000:
        regime = "POST-CONVECTIVE STABILIZATION"
        summary = "Buoyancy is depleted; residual moisture may sustain stratiform rainfall."
    elif cape >= 2500:
        regime = "SEVERE CONVECTIVE INSTABILITY"
        summary = "Deep buoyant layer supports strong updrafts and organized convection."
    elif cape >= 1000:
        regime = "MODERATE INSTABILITY"
        summary = "Instability present; thunderstorms possible with triggering."
    else:
        regime = "WEAK INSTABILITY"
        summary = "Limited buoyant support for deep convection."

    return {
        "cape": round(max(0.0, cape), 1),
        "cin": round(cin, 1),
        "lcl": round(p_lcl, 1),
        "lfc": round(lfc_pres, 1),
        "el": round(el_pres, 1),
        "instability_layer_depth_m": instability_layer_depth,
        "max_virtual_buoyancy_k": round(max_buoyancy, 3),
        "min_virtual_buoyancy_k": round(min_buoyancy, 3),
        "thermodynamic_regime": regime,
        "parcel_trace_explainability": summary,
        "parcel_path": parcel_path
    }


def resolve_sounding_thermodynamics(text_data: str, profile_fallback: dict) -> dict:
    """
    Operational thermodynamic resolver:
    1) Parse authoritative Wyoming footer indices when present
    2) Compute parcel ascent CAPE/CIN/LCL/LFC/EL from profile columns
    3) Prefer parsed footer CAPE when computed CAPE is inconsistent (< 50 J/kg with footer > 0)
    """
    parsed_indices = parse_sounding_indices(text_data) if text_data else {}
    sounding_layers = parse_sounding_text(text_data) if text_data else []
    computed = solve_thermodynamics(sounding_layers) if sounding_layers else {}
    raw_cape = parsed_indices.get("cape")
    calculated_cape = computed.get("cape") if computed else None

    result = {
        "cape": profile_fallback.get("cape", 0.0),
        "cin": profile_fallback.get("cin", -50.0),
        "lifted_index": profile_fallback.get("lifted_index", 0.0),
        "sweat_index": profile_fallback.get("sweat_index", 200.0),
        "k_index": profile_fallback.get("k_index", 25.0),
        "pwat": profile_fallback.get("pwat", 45.0),
        "tt_index": profile_fallback.get("tt_index", 45.0),
        "lcl": profile_fallback.get("lcl", 900.0),
        "lfc": profile_fallback.get("lfc", 850.0),
        "el": profile_fallback.get("el", 150.0),
        "sounding_available": bool(sounding_layers),
        "indices_source": "profile_fallback",
        "raw_cape": raw_cape,
        "calculated_cape": calculated_cape,
        "cape_delta_raw_calculated": None,
        "instability_layer_depth_m": 0.0,
        "max_virtual_buoyancy_k": 0.0,
        "min_virtual_buoyancy_k": 0.0,
        "thermodynamic_regime": "UNKNOWN",
        "parcel_trace_explainability": "No thermodynamic profile available.",
    }

    if computed:
        for key in ("cape", "cin", "lcl", "lfc", "el"):
            if computed.get(key) is not None:
                result[key] = computed[key]
        for key in (
            "instability_layer_depth_m",
            "max_virtual_buoyancy_k",
            "min_virtual_buoyancy_k",
            "thermodynamic_regime",
            "parcel_trace_explainability",
        ):
            if key in computed:
                result[key] = computed[key]
        result["indices_source"] = "parcel_computation"

    for key in ("cape", "cin", "lifted_index", "sweat_index", "k_index", "pwat", "tt_index", "lcl", "lfc", "el"):
        if key in parsed_indices:
            result[key] = parsed_indices[key]
            result["indices_source"] = "wyoming_sounding_footer"

    footer_cape = parsed_indices.get("cape")
    if footer_cape is not None and footer_cape > 0 and result.get("cape", 0) < 50:
        result["cape"] = footer_cape

    if raw_cape is not None and calculated_cape is not None:
        result["cape_delta_raw_calculated"] = round(raw_cape - calculated_cape, 1)

    return result

def generate_mock_sounding_text(station_code, station_name, cycle, sfc_t, sfc_td):
    """
    Generates a high-fidelity University of Wyoming styled sounding text report
    with custom surface temperature and dewpoint, including indices at the bottom.
    """
    # Define vertical profiles template (pressure, height, temp_offset, dewpoint_offset, relh, mixr, drct, sknt)
    profile_layers = [
        (1000.0, 44,    0.0,   0.0,  90, 22.0,   90,  5),
        (925.0,  738,  -5.0,  -3.0,  88, 18.5,  110, 12),
        (850.0,  1477, -10.0,  -6.0,  80, 14.5,  120, 14),
        (700.0,  3139, -19.0, -18.0,  55,  7.8,  125, 18),
        (500.0,  5890, -35.0, -32.0,  80,  4.5,   95,  8),
        (400.0,  7630, -47.0, -42.0,  60,  2.2,  105,  6),
        (300.0,  9770, -62.0, -58.0,  55,  0.70, 210,  4),
        (200.0,  12560,-82.0, -82.0,  35,  0.08,  85,  8),
        (100.0,  16730,-102.0,-102.0, 60,  0.00,  90, 20)
    ]
    
    header = f"""University of Wyoming - Radiosonde Data
 
{station_code}  {station_name} Observations at {cycle} 26 May 2026
 
-----------------------------------------------------------------------------
   PRES   HGHT   TEMP   DWPT   RELH   MIXR   DRCT   SKNT   THTA   THTE   THTV
    hPa     m      C      C      %    g/kg    deg   knot     K      K      K 
-----------------------------------------------------------------------------
"""
    body = ""
    for pres, hght, t_off, td_off, relh, mix, drct, sknt in profile_layers:
        t = round(sfc_t + t_off, 1)
        td = round(sfc_td + td_off, 1)
        
        # Calculate theta, theta-e, theta-v realistically
        t_k = t + 273.15
        thta = round(t_k * ((1000.0 / pres) ** 0.286), 1)
        
        es = 6.112 * math.exp((17.67 * t) / (t + 243.5))
        w = 0.622 * es / (pres - es)
        thte = round(thta * math.exp((2.5e6 * w) / (1005.7 * t_k)), 1)
        thtv = round(thta * (1.0 + 0.61 * w), 1)
        
        body += f"{pres:6.1f} {hght:6d} {t:6.1f} {td:6.1f} {relh:6d} {mix:6.2f} {drct:6d} {sknt:6d} {thta:6.1f} {thte:6.1f} {thtv:6.1f}\n"
        
    # Map (station_code, cycle) to realistic indices for verification parsing
    mock_indices = {
        ("43150", "00Z"): {"li": -7.5, "sweat": 340.0, "k": 38.0, "pwat": 68.0, "cape": 2850.0, "cin": -45.0, "lcl": 850.0, "lfc": 810.0, "el": 120.0},
        ("43150", "12Z"): {"li": -8.8, "sweat": 380.0, "k": 41.0, "pwat": 72.0, "cape": 3200.0, "cin": -25.0, "lcl": 900.0, "lfc": 850.0, "el": 100.0},
        ("43185", "00Z"): {"li": -5.2, "sweat": 280.0, "k": 34.0, "pwat": 55.0, "cape": 2200.0, "cin": -60.0, "lcl": 880.0, "lfc": 830.0, "el": 150.0},
        ("43185", "12Z"): {"li": -6.8, "sweat": 320.0, "k": 37.0, "pwat": 61.0, "cape": 2600.0, "cin": -40.0, "lcl": 910.0, "lfc": 860.0, "el": 130.0},
        ("43279", "00Z"): {"li": -3.8, "sweat": 210.0, "k": 28.0, "pwat": 48.0, "cape": 1500.0, "cin": -80.0, "lcl": 900.0, "lfc": 820.0, "el": 180.0},
        ("43279", "12Z"): {"li": -4.5, "sweat": 240.0, "k": 31.0, "pwat": 52.0, "cape": 1750.0, "cin": -50.0, "lcl": 920.0, "lfc": 850.0, "el": 160.0},
        ("42809", "00Z"): {"li": -8.0, "sweat": 360.0, "k": 40.0, "pwat": 70.0, "cape": 2900.0, "cin": -35.0, "lcl": 870.0, "lfc": 840.0, "el": 110.0},
        ("42809", "12Z"): {"li": -9.2, "sweat": 410.0, "k": 44.0, "pwat": 76.0, "cape": 3400.0, "cin": -15.0, "lcl": 920.0, "lfc": 880.0, "el": 95.0},
        ("43128", "00Z"): {"li": -1.5, "sweat": 140.0, "k": 22.0, "pwat": 36.0, "cape": 800.0, "cin": -120.0, "lcl": 820.0, "lfc": 0.0, "el": 0.0},
        ("43128", "12Z"): {"li": -2.8, "sweat": 190.0, "k": 26.0, "pwat": 42.0, "cape": 1100.0, "cin": -90.0, "lcl": 850.0, "lfc": 780.0, "el": 220.0}
    }
    
    ind = mock_indices.get((station_code, cycle), {"li": -5.0, "sweat": 250.0, "k": 30.0, "pwat": 50.0, "cape": 2000.0, "cin": -50.0, "lcl": 900.0, "lfc": 800.0, "el": 150.0})
    
    footer = f"""-----------------------------------------------------------------------------
Station information and sounding indices
                             Station number: {station_code}
                            Observation time: 260526/{cycle.replace('Z', '00')}
                                Lifted index: {ind['li']:.2f}
                                 SWEAT index: {ind['sweat']:.2f}
                                     K index: {ind['k']:.2f}
       Convective Available Potential Energy: {ind['cape']:.2f}
              CAPE using virtual temperature: {ind['cape']:.2f}
                       Convective Inhibition: {ind['cin']:.2f}
              CINS using virtual temperature: {ind['cin']:.2f}
                            Equilibrum Level: {ind['el']:.2f}
                    Level of Free Convection: {ind['lfc']:.2f}
 Pres [hPa] of the Lifted Condensation Level: {ind['lcl']:.2f}
 Precipitable water [mm] for entire sounding: {ind['pwat']:.2f}
"""
    return header + body + footer

def seed_sounding_files():
    """Seeds radiosonde raw files in backend/data/soundings/ on startup"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    soundings_dir = os.path.join(base_dir, "data", "soundings")
    os.makedirs(soundings_dir, exist_ok=True)
    
    # Station parameter mappings to seed realistic soundings
    seed_configs = [
        ("43150", "Visakhapatnam", "00Z", 32.5, 25.2),
        ("43150", "Visakhapatnam", "12Z", 34.0, 26.5),
        ("43185", "Machilipatnam", "00Z", 31.0, 23.4),
        ("43185", "Machilipatnam", "12Z", 32.5, 24.5),
        ("43279", "Chennai",       "00Z", 30.2, 22.0),
        ("43279", "Chennai",       "12Z", 31.5, 23.2),
        ("42809", "Kolkata",       "00Z", 33.0, 26.8),
        ("42809", "Kolkata",       "12Z", 34.5, 27.5),
        ("43128", "Hyderabad",     "00Z", 29.0, 15.5),
        ("43128", "Hyderabad",     "12Z", 30.5, 17.2)
    ]
    
    for code, name, cycle, temp, dwpt in seed_configs:
        filepath = os.path.join(soundings_dir, f"{code}_{cycle}.txt")
        if not os.path.exists(filepath):
            txt = generate_mock_sounding_text(code, name, cycle, temp, dwpt)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(txt)
            print(f"✅ Sounding file seeded: {filepath}")

def fetch_live_wyoming_sounding(station_code: str, cycle: str) -> str:
    """
    Scrape live University of Wyoming sounding text block for active UTC cycle day/hour.
    Returns raw text if successful, else None.
    """
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime, timezone, timedelta

    now_utc = datetime.now(timezone.utc)
    target_hour = 0 if cycle == "00Z" else 12
    
    # Try fetching for today first, fallback to yesterday if cycle not yet available
    # weather.uwyo.edu takes a few minutes to publish, and 12Z won't be available during morning
    for day_offset in range(3):
        url_date = now_utc - timedelta(days=day_offset)
        
        # If querying 12Z but current UTC time is before 12Z, start with yesterday
        if day_offset == 0 and cycle == "12Z" and now_utc.hour < 12:
            continue
            
        year = url_date.year
        month_str = f"{url_date.month:02d}"
        day_str = f"{url_date.day:02d}"
        hour_str = f"{target_hour:02d}"
        
        from_to = f"{day_str}{hour_str}"
        url = f"https://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT:LIST&YEAR={year}&MONTH={month_str}&FROM={from_to}&TO={from_to}&STNM={station_code}"
        
        try:
            print(f"[INGEST] Requesting live Wyoming sounding: Station {station_code}, Date {year}-{month_str}-{day_str} {cycle}")
            response = requests.get(url, timeout=12)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                pre_tag = soup.find("pre")
                if pre_tag:
                    text_content = pre_tag.get_text()
                    if "PRES" in text_content and "HGHT" in text_content:
                        return text_content
                else:
                    text_content = soup.get_text()
                    if "PRES" in text_content and "HGHT" in text_content:
                        return text_content
        except Exception as e:
            print(f"[INGEST] Wyoming sounding fetch failed for {station_code} (offset {day_offset}): {e}")
            
    return None

# Run seeding on module import
seed_sounding_files()
