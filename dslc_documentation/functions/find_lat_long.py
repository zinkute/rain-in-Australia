# cities should have a list of correct city names
def find_lat_long(cities):
    
    import time
    
    # Create an empty list to gather latitude and longitude data
    latitude = []
    longitude = []

    # prepare Geolocator
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="city_geocoder", timeout=10)

    # loop through given cities
    for city in cities:
        location = geolocator.geocode(f"{city}, Australia")
        
        if location:
            latitude.append(location.latitude)
            longitude.append(location.longitude)
        else:
            latitude.append("No latitude found")
            longitude.append("No longitude found")
            
        time.sleep(1)
    
    return latitude, longitude
        