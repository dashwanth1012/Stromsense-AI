import csv

def analyze_csv():
    filepath = 'backend/data/imd_observational_records.csv'
    total_records = 0
    thunderstorms = 0
    nwx = 0
    events = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_records += 1
            obs = row.get('observed', '').strip().upper()
            is_ts = obs in ["TS", "TSRA", "SEVERE TS", "SQ", "THUNDERSTORM", "THUNDERSTORM WITH RAIN"]
            if is_ts:
                thunderstorms += 1
            else:
                nwx += 1
            events.append(row)
            
    print("CSV Total Records:", total_records)
    print("CSV Thunderstorms:", thunderstorms)
    print("CSV NWX:", nwx)
    if events:
        # Sort by date
        sorted_events = sorted(events, key=lambda x: x.get('date', ''))
        print("First Date in CSV:", sorted_events[0].get('date'))
        print("Last Date in CSV:", sorted_events[-1].get('date'))
        # Let's find latest thunderstorm
        ts_events = [e for e in sorted_events if e.get('observed', '').strip().upper() in ["TS", "TSRA", "SEVERE TS", "SQ", "THUNDERSTORM", "THUNDERSTORM WITH RAIN"]]
        if ts_events:
            print("Latest TS in CSV:", ts_events[-1].get('date'), ts_events[-1].get('station'), ts_events[-1].get('observed'))
        else:
            print("No TS events in CSV?")

analyze_csv()
