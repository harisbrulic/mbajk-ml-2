import requests
import json
import csv
import os
from datetime import datetime

current_datetime = datetime.now()

api_url_weather = "https://api.open-meteo.com/v1/forecast?latitude=46.5547&longitude=15.6466&current=temperature_2m,relative_humidity_2m,apparent_temperature,rain,visibility"
data_dir = "data/raw" 
csv_filename = f"{data_dir}/weather.csv"

response_weather = requests.get(api_url_weather)

if response_weather.status_code == 200:
    weather_data = response_weather.json()

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'temperature', 'relative_humidity', 'apparent_temperature', 'rain', 'visibility'] 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the CSV header

        record_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow({
            'date': record_time,
            'temperature': weather_data['current']['temperature_2m'],
            'relative_humidity': weather_data['current']['relative_humidity_2m'],
            'apparent_temperature': weather_data['current']['apparent_temperature'],
            'rain': weather_data['current']['rain'],
            'visibility': weather_data['current']['visibility']
        })
else:
    print(f"Error fetching weather data: {response_weather.status_code}")