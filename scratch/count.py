import json
import re

with open('frontend/src/components/modules/fallback_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'export const fallbackHistoricalDates = (\[[\s\S]*?\]);', content)
if match:
    array_str = match.group(1)
    cleaned = array_str.replace('true', 'True').replace('false', 'False')
    data = eval(cleaned)
    print("Parsed records count:", len(data))
    
    ts_count = 0
    nwx_count = 0
    for item in data:
        observed = StringUpper = str(item.get('observed', '')).strip().upper()
        is_ts = observed in ["TS", "TSRA", "SEVERE TS", "SQ", "THUNDERSTORM", "THUNDERSTORM WITH RAIN"]
        if is_ts:
            ts_count += 1
        else:
            nwx_count += 1
            
    print("TS count:", ts_count)
    print("NWX count:", nwx_count)
    
    # Let's find unique dates and stations
    dates = set(item['date'] for item in data)
    stations = set(item['station'] for item in data)
    print("Unique dates:", len(dates))
    print("Unique stations:", len(stations))
else:
    print("No match found")
