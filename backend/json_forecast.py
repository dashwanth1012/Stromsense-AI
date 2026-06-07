import requests
from bs4 import BeautifulSoup
import re
import json

# Station list
stations = {
    "Visakhapatnam": "43150",
    "Chennai": "43279",
    "Kolkata": "42809",
    "Hyderabad": "43128",
    "Bhubaneswar": "42971"
}

# Store all forecasts
forecast_data = []

# Function to extract values
def extract_value(pattern, text):
    match = re.search(pattern, text)

    if match:
        return float(match.group(1))
    else:
        return None

# Loop through stations
for station_name, station_code in stations.items():

    url = f"https://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT:LIST&YEAR=2025&MONTH=05&FROM=1900&TO=1900&STNM={station_code}"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text()

    # Extract indices
    cape = extract_value(r"Convective Available Potential Energy:\s+([-\d\.]+)", text)

    li = extract_value(r"Lifted index:\s+([-\d\.]+)", text)

    sweat = extract_value(r"SWEAT index:\s+([-\d\.]+)", text)

    kindex = extract_value(r"K index:\s+([-\d\.]+)", text)

    pwat = extract_value(r"Precipitable water.*?:\s+([-\d\.]+)", text)

    # Risk logic
    risk = "LOW THUNDERSTORM RISK"

    if cape and li and pwat:

        if cape > 2500 and li < -5 and pwat > 50:
            risk = "SEVERE THUNDERSTORM RISK"

        elif cape > 1500 and li < -3 and pwat > 40:
            risk = "HIGH THUNDERSTORM RISK"

        elif cape > 800:
            risk = "MODERATE THUNDERSTORM RISK"

    # Create structured forecast
    station_forecast = {
        "station": station_name,
        "station_code": station_code,
        "cape": cape,
        "lifted_index": li,
        "sweat_index": sweat,
        "k_index": kindex,
        "pwat": pwat,
        "forecast": risk
    }

    # Add to list
    forecast_data.append(station_forecast)

# Print JSON nicely
print("\n========= JSON FORECAST DATA =========\n")

print(json.dumps(forecast_data, indent=4))