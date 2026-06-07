import sys
sys.path.append('backend')
import analysis_engines

db = analysis_engines.load_historical_observations()
print("Number of records in DB:", len(db))
if db:
    print("Keys of first record:", db[0].keys())
    # Count unique values of 'time' field in the DB
    times = {}
    for r in db:
        t = r.get('time')
        times[t] = times.get(t, 0) + 1
    print("Unique times in database:", times)
