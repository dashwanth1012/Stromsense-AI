# Real atmospheric values from sounding

cape = 2234
li = -4.83
sweat = 243
kindex = 33
pwat = 64

# Thunderstorm risk logic

if cape > 2500 and li < -5 and pwat > 50:
    risk = "SEVERE THUNDERSTORM RISK"

elif cape > 1500 and li < -3 and pwat > 40:
    risk = "HIGH THUNDERSTORM RISK"

elif cape > 800:
    risk = "MODERATE THUNDERSTORM RISK"

else:
    risk = "LOW THUNDERSTORM RISK"

# Print atmospheric analysis

print("\n========= THUNDERSTORM ANALYSIS =========\n")

print(f"CAPE : {cape} J/kg")
print(f"Lifted Index : {li}")
print(f"SWEAT Index : {sweat}")
print(f"K Index : {kindex}")
print(f"PWAT : {pwat} mm")

print("\nForecast :", risk)