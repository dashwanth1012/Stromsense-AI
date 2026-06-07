import pandas as pd
import os

files = [
    'backend/data/imd_observational_records.csv',
    'backend/data/live_dataset.csv',
    'backend/ml/weather_training.csv',
    'data/live_dataset.csv'
]

for f in files:
    path = os.path.join('c:/Users/USER/Thunderstorm analysis', f)
    if os.path.exists(path):
        print(f"--- File: {f} ---")
        try:
            df = pd.read_csv(path)
            print("Columns:", list(df.columns))
            print("Shape:", df.shape)
            if 'date' in df.columns:
                df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')
                print("Min Date:", df['date_parsed'].min())
                print("Max Date:", df['date_parsed'].max())
                print("Year counts:\n", df['date_parsed'].dt.year.value_counts())
            elif 'Date' in df.columns:
                df['date_parsed'] = pd.to_datetime(df['Date'], errors='coerce')
                print("Min Date:", df['date_parsed'].min())
                print("Max Date:", df['date_parsed'].max())
                print("Year counts:\n", df['date_parsed'].dt.year.value_counts())
            else:
                print("No date column found!")
        except Exception as e:
            print("Error:", e)
