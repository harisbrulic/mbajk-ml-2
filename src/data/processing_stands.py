import json
import pandas as pd
import os
from datetime import datetime
import re

with open('data/raw/svezi_podatki.json', 'r') as file:
    data = json.load(file)

def process_data(item):
    timestamp = datetime.fromtimestamp(item["last_update"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    
    filename_safe = re.sub(r'[^\w\s-]', '', item["name"].replace(' ', '_')) + ".csv"
    
    bike_data = {
        "timestamp": [timestamp],
        "available_bikes": [item["available_bikes"]],
        "available_bike_stands": [item["available_bike_stands"]]
    }
    
    return filename_safe, bike_data

output_dir = 'data/processed'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for item in data:
    filename, bike_data = process_data(item)
    df = pd.DataFrame(bike_data)
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False)

print("Data saved successfully.")
