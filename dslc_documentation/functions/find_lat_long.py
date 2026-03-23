import os
import json
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="city_geocoder", timeout = 10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds = 5)

file_path = "D:\\Projects\\rain-in-Australia\\data\\Lat_lon_data.csv"

# If file exists, load it
if os.path.exists(file_path):
    existing_df = pd.read_csv(file_path)
else:
    existing_df = pd.DataFrame(columns=["Location", "Latitude", "Longitude"])
    
# unique location data frame
# load original data frame
rain_data = pd.read_csv("D:\\Projects\\rain-in-Australia\\data\\weatherAUS.csv")

# update location name
rain_data.replace('BadgerysCreek', 'Badgerys Creek', inplace = True)
rain_data.replace('CoffsHarbour', 'Coffs Harbour', inplace = True)
rain_data.replace('NorahHead', 'Norah Head', inplace = True)
rain_data.replace('NorfolkIsland', 'Norfolk Island', inplace = True)
rain_data.replace('SydneyAirport', 'Sydney Airport', inplace = True)
rain_data.replace('WaggaWagga', 'Wagga Wagga', inplace = True)
rain_data.replace('MountGinini', 'Mount Ginini', inplace = True)
rain_data.replace('MelbourneAirport', 'Melbourne Airport', inplace = True)
rain_data.replace('GoldCoast', 'Gold Coast', inplace = True)
rain_data.replace('MountGambier', 'Mount Gambier', inplace = True)
rain_data.replace('PearceRAAF', 'RAAF Base Pearce', inplace = True)
rain_data.replace('PerthAirport', 'Perth Airport', inplace = True)
rain_data.replace('SalmonGums', 'Salmon Gums', inplace = True)
rain_data.replace('AliceSprings', 'Alice Springs', inplace = True)
rain_data.replace('Richmond', 'Richmond RAAF', inplace = True)
rain_data.replace('Albury', 'Albury Airport', inplace = True)
rain_data.replace('Portland', 'Portland Airport', inplace = True)
rain_data.replace('Walpole', 'North Walpole', inplace = True)

# unique location data frame
city_data = pd.DataFrame(rain_data['Location'].unique(), columns=['Location']) 
 
for city in city_data["Location"]:
# Skip if already processed
    if city in existing_df["Location"].values:
        continue

    location = geocode(f"{city}, Australia")
    
    if location:
        lat, lon = location.latitude, location.longitude
    else:
        lat, lon = None, None

    new_row = pd.DataFrame([[city, lat, lon]], columns=["Location", "Latitude", "Longitude"])
    
    # Append and save immediately
    existing_df = pd.concat([existing_df, new_row], ignore_index=True)
    existing_df.to_csv(file_path, index=False)

    print(f"{i+1}/{len(city_data)}: {city} was added into the CSV file.")
