import json
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def find_lat_long(cities):
    geolocator = Nominatim(user_agent="city_geocoder", timeout=10)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    # load cache if exists
    try:
        with open("geocode_cache.json", "r") as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = {}

    latitude = []
    longitude = []

    for city in cities:
        if city in cache:
            lat, lon = cache[city]
        else:
            location = geocode(f"{city}, Australia")
            if location:
                lat, lon = location.latitude, location.longitude
            else:
                lat, lon = None, None

            cache[city] = (lat, lon)

        latitude.append(lat)
        longitude.append(lon)

    # save cache
    with open("geocode_cache.json", "w") as f:
        json.dump(cache, f)

    return latitude, longitude