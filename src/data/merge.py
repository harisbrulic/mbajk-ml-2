import pandas as pd

# Učitavanje podataka
bike_data = pd.read_csv('data/processed/processed_bike_data.csv')
weather_data = pd.read_csv('data/processed/processed_weather_data.csv')

# Konverzija 'last_update' u biciklističkim podacima i 'date' u meteorološkim podacima u datetime
bike_data['last_update'] = pd.to_datetime(bike_data['last_update'])
weather_data['date'] = pd.to_datetime(weather_data['date'])

# Spajanje podataka na osnovu najbližeg vremena
combined_data = pd.merge_asof(bike_data.sort_values('last_update'), 
                               weather_data.sort_values('date'), 
                               left_on='last_update', 
                               right_on='date', 
                               direction='nearest')

# Čuvanje kombinovanog dataset-a
combined_data.to_csv('data/processed/combined_data.csv', index=False)
