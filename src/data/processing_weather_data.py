import pandas as pd

RAW_DATA_FILEPATH = "data/raw/weather.csv"
PROCESSED_DATA_FILEPATH = "data/processed/processed_weather_data.csv"

df = pd.read_csv(RAW_DATA_FILEPATH)

df.to_csv(PROCESSED_DATA_FILEPATH, index=False) 