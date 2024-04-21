import requests
import json
import csv
import os

from datetime import datetime

current_datetime = datetime.now()

# API URL-ovi 
api_url_stations = "https://api.jcdecaux.com/vls/v1/stations?contract=maribor&apiKey=5e150537116dbc1786ce5bec6975a8603286526b"
api_url_weather = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,rain,visibility"

data_dir = "data/raw"  
processed_data_dir = "data/processed" 

# Dohvaćamo podatke o biciklističkim postajališčima
response_stations = requests.get(api_url_stations)

if response_stations.status_code == 200:
    stations_data = response_stations.json()

    # Iteriramo kroz svaku postaju
    for station in stations_data:
        latitude = station['position']['lat']
        longitude = station['position']['lng']

        weather_api_url = api_url_weather.format(latitude=latitude, longitude=longitude)
        response_weather = requests.get(weather_api_url)

        if response_weather.status_code == 200:
            weather_data = response_weather.json()

            # Čistimo ime
            station_name = station['name'].replace(' ', '_').replace('/', '_')

            # JSON datoteka (kao i prije)
            json_filename = f"{data_dir}/weather/{station_name}.json"
            with open(json_filename, 'w', encoding='utf-8') as file:
                output_data = {
                    'station_name': station['name'],
                    'weather': weather_data
                }
                json.dump(output_data, file, ensure_ascii=False, indent=4)

            # CSV datoteka - novi dio!
            normalized_station_name = station_name.lower()  # Niža slova za konzistentnost imena
            processed_data_file = os.path.join(processed_data_dir, f"{normalized_station_name}_processed_data.csv")

            header = ['date', 'bike_stands', 'available_bike_stands', 'temperature', 'relative_humidity', 'apparent_temperature', 'rain', 'visibility']

            # Otvaramo datoteku u 'a' (append) načinu rada
            with open(processed_data_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=header)

                if os.stat(processed_data_file).st_size == 0:
                    writer.writeheader()  # Zapisujemo zaglavlje ako je datoteka nova

                record_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow({
                    'date': record_time,
                    'bike_stands': station['bike_stands'],
                    'available_bike_stands': station['available_bike_stands'],
                    'temperature': weather_data['current']['temperature_2m'],
                    'relative_humidity': weather_data['current']['relative_humidity_2m'],
                    'apparent_temperature': weather_data['current']['apparent_temperature'],
                    'rain': weather_data['current']['rain'],
                    'visibility': weather_data['current']['visibility'],
                })
        else:
            print(f"Error for station {station['name']}: Weather API error - {response_weather.status_code}")
else:
    print("Error fetching bike station data.")