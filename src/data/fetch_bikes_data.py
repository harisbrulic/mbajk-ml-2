import requests
import json
import csv
import datetime

api_url_stations = "https://api.jcdecaux.com/vls/v1/stations?contract=maribor&apiKey=5e150537116dbc1786ce5bec6975a8603286526b"
data_dir = "data/raw"
csv_filename = f"{data_dir}/bike_stations.csv"

response_stations = requests.get(api_url_stations)

if response_stations.status_code == 200:
    stations_data = response_stations.json()

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['number', 'name', 'last_update', 'bike_stands', 'available_bike_stands']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for station in stations_data:
            last_update_dt = datetime.datetime.fromtimestamp(station['last_update'] // 1000)
            last_update_str = last_update_dt.strftime('%Y-%m-%d %H:%M:%S')

            row = {
                'number': station['number'],
                'name': station['name'],
                'last_update': last_update_str,
                'bike_stands': station['bike_stands'],
                'available_bike_stands': station['available_bike_stands']
            }

            writer.writerow(row)
