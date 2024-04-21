import requests
import json

from datetime import datetime

current_datetime = datetime.now()

api_url_stations = "https://api.jcdecaux.com/vls/v1/stations?contract=maribor&apiKey=5e150537116dbc1786ce5bec6975a8603286526b"

data_dir = "data/raw"

response_stations = requests.get(api_url_stations)

if response_stations.status_code == 200:
    stations_data = response_stations.json()

    for station in stations_data:

        station_name = station['name'].replace(' ', '_').replace('/', '_')

        json_filename = f"{data_dir}/weather/{station_name}.json"
        with open(json_filename, 'w', encoding='utf-8') as file:
            output_data = {
                'station_name': station['name'],
            }
            json.dump(output_data, file, ensure_ascii=False, indent=4)