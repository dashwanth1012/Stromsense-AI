with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Search for the endpoint '/cwc/historical-analysis'
pos = content.find('/cwc/historical-analysis')
if pos != -1:
    print("Found historical-analysis at char:", pos)
    # Print the function definition and body (approx 150 lines)
    lines = content[pos:pos+5000].splitlines()
    for l in lines[:100]:
        print(l)
