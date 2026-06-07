with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Search for the key 'evolution ='
pos = content.find('evolution =')
if pos != -1:
    print("Found evolution = at char:", pos)
    print(content[pos-100:pos+1000])
else:
    print("Not found 'evolution ='")
