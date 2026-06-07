import requests
from bs4 import BeautifulSoup
import re

# Wyoming Sounding URL
url = "https://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT:LIST&YEAR=2025&MONTH=05&FROM=1900&TO=1900&STNM=43150"

# Fetch sounding data
response = requests.get(url)

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Extract plain text
text = soup.get_text()

# Function to extract values
def extract_value(pattern):
    match = re.search(pattern, text)

    if match:
        return float(match.group(1))
    else:
        return None

# Extract atmospheric indices
cape = extract_value(r"Convective Available Potential Energy:\s+([-\d\.]+)")
li = extract_value(r"Lifted index:\s+([-\d\.]+)")
sweat = extract_value(r"SWEAT index:\s+([-\d\.]+)")
kindex = extract_value(r"K index:\s+([-\d\.]+)")
pwat = extract_value(r"Precipitable water.*?:\s+([-\d\.]+)")

# Risk analysis
risk = "LOW THUNDERSTORM RISK"

if cape and li and pwat:

    if cape > 2500 and li < -5 and pwat > 50:
        risk = "SEVERE THUNDERSTORM RISK"

    elif cape > 1500 and li < -3 and pwat > 40:
        risk = "HIGH THUNDERSTORM RISK"

    elif cape > 800:
        risk = "MODERATE THUNDERSTORM RISK"

# Print results
print("\n========= AUTOMATIC THUNDERSTORM ANALYSIS =========\n")

print(f"CAPE : {cape}")
print(f"Lifted Index : {li}")
print(f"SWEAT Index : {sweat}")
print(f"K Index : {kindex}")
print(f"PWAT : {pwat}")

print("\nForecast :", risk)