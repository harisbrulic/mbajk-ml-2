import pandas as pd
import datetime

RAW_DATA_FILEPATH = "data/raw/bike_stations.csv"
PROCESSED_DATA_FILEPATH = "data/processed/processed_bike_data.csv"

df = pd.read_csv(RAW_DATA_FILEPATH)

df['last_update'] = pd.to_datetime(df['last_update'])

df['occupancy_rate'] = (df['bike_stands'] - df['available_bike_stands']) / df['bike_stands'] * 100

df.to_csv(PROCESSED_DATA_FILEPATH, index=False) 