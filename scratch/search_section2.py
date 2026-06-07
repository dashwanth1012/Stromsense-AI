with open(r"c:\Users\USER\Thunderstorm analysis\frontend\src\components\modules\AnalyticsDeck.jsx", "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find("SECTION 2 & 3")
if pos != -1:
    print(f"Found at character {pos}")
    # print lines around this position
    lines = content[:pos].splitlines()
    start_line = len(lines)
    all_lines = content.splitlines()
    for idx in range(max(0, start_line - 5), min(len(all_lines), start_line + 30)):
        print(f"{idx+1}: {all_lines[idx]}")
else:
    print("Not found")
