import os

downloads_dir = 'c:/Users/USER/Downloads'
if os.path.exists(downloads_dir):
    for f in os.listdir(downloads_dir):
        if f.endswith(('.csv', '.xlsx', '.xls', '.txt', '.json')):
            path = os.path.join(downloads_dir, f)
            print(f"{path} - Size: {os.path.getsize(path)} bytes")
else:
    print("Downloads directory does not exist")
