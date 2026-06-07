import sys
sys.path.append('backend')
import analysis_engines

db = analysis_engines.load_historical_observations()
print(f"Total: {len(db)}")
for idx, r in enumerate(db):
    print(f"{idx+1}: date={r.get('date')}, station={r.get('station')}, observed={r.get('observed')}, time={r.get('time')}")
