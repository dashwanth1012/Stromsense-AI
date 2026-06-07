import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\AnalyticsDeck.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Original lines count: {len(lines)}")
# Print lines around 1803
for idx in range(1800, min(len(lines), 1810)):
    print(f"{idx+1}: {repr(lines[idx])}")

# Let's replace lines from index 1802 (1-based line 1803) to 1806 (1-based line 1807)
# 1803: '            </div>\n'
# 1804: '          </div>\n'
# 1805: '                    </div>\n'
# 1806: '          </details>\n'
# 1807: '      )}\n'

# We want them to be:
# 1803: '            </div>\n' (closes right column)
# 1804: '          </div>\n' (closes display:grid)
# 1805: '          </details>\n' (closes details)
# 1806: '        </div>\n' (closes outer flex column)
# 1807: '      )}\n' (closes ternary)

lines[1804] = '          </details>\n'
lines[1805] = '        </div>\n'

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Modified lines written successfully.")
