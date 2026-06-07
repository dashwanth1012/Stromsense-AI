import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Add backend directory to path
sys.path.append(os.path.abspath('backend'))

import analysis_engines as ae

def verify_stations():
    print("Loading database records...")
    db = ae.load_historical_observations()
    print(f"Total seeded records loaded: {len(db)}")
    
    # Group records by station
    by_station = {}
    for r in db:
        st = r.get("station")
        if st not in by_station:
            by_station[st] = []
        by_station[st].append(r)
        
    print("\n--- STATION RECORD COUNT SUMMARY ---")
    for st, recs in by_station.items():
        print(f"Station: {st:15} | Records Count: {len(recs)}")
        
    print("\n--- STATION PARAMETER DYNAMISM CHECK ---")
    for st, recs in by_station.items():
        capes = [r.get("cape") for r in recs if r.get("cape") is not None]
        pwats = [r.get("pwat") for r in recs if r.get("pwat") is not None]
        unique_capes = len(set(capes))
        unique_pwats = len(set(pwats))
        print(f"Station: {st:15} | Unique CAPE Values: {unique_capes:2} | Unique PWAT Values: {unique_pwats:2}")
        
    # Verify that no station has exactly the same CAPE series as another
    station_names = list(by_station.keys())
    print("\n--- CROSS-STATION SEPARATION CHECK ---")
    for i in range(len(station_names)):
        for j in range(i+1, len(station_names)):
            st1 = station_names[i]
            st2 = station_names[j]
            capes1 = [r.get("cape") for r in by_station[st1]]
            capes2 = [r.get("cape") for r in by_station[st2]]
            # Compare first 5 values if exists
            min_len = min(5, len(capes1), len(capes2))
            if min_len > 0 and capes1[:min_len] == capes2[:min_len]:
                print(f"⚠️ WARNING: {st1} and {st2} have identical initial CAPE values: {capes1[:min_len]}")
            else:
                print(f"✓ Dynamicity verified: {st1} vs {st2} (Unique telemetry separation)")

if __name__ == "__main__":
    verify_stations()
