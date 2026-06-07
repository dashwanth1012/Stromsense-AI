import re

with open('c:/Users/USER/Thunderstorm analysis/frontend/src/components/modules/fallback_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

dates = re.findall(r'"date":\s*"([^"]+)"', text)
years = sorted(list(set(d.split('-')[0] for d in dates)))
print('Years in fallback_data:', years)
print('Total dates count:', len(dates))

stations = re.findall(r'"station":\s*"([^"]+)"', text)
print('Unique stations:', set(stations))
