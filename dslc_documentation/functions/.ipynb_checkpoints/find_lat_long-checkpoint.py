import json
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def find_lat_long(cities):
    geolocator = Nominatim(user_agent="city_geocoder", timeout=10)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    # unique location data frame
    city_data = pd.DataFrame(cities['Location'].unique(), columns=['Location']) 
    
    latitude = []
    longitude = []
    
    for city in city_data["Location"]:
        location = geocode(f"{city}, Australia")
        if location:
            lat, lon = location.latitude, location.longitude
        else:
            lat, lon = None, None

        latitude.append(lat)
        longitude.append(lon)
        
    latitude_df = pd.DataFrame(latitude, columns=['Latitude']) 
    longitude_df = pd.DataFrame(longitude, columns=['Longitude'])

    city_data_coordinates = pd.concat([city_data, latitude_df], axis=1)
    city_data_coordinates = pd.concat([city_data_coordinates, longitude_df], axis=1)
    
    return city_data_coordinates