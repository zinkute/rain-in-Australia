def find_state(locations):
    
    import time
    import pandas as pd
    from geopy.geocoders import Nominatim
    
    # Initialize Nominatim
    geolocator = Nominatim(user_agent="geo_state_lookup")

    # List of location names
    location_names = locations

    # List to store results
    results = []

    for name in location_names:
        try:
            # Geocode to get coordinates
            location = geolocator.geocode(f"{name}, Australia")
            if location:
                # Reverse geocode to get detailed address
                location_details = geolocator.reverse((location.latitude, location.longitude), exactly_one=True)
                address = location_details.raw.get('address', {})
                state = address.get('state', 'Unknown')  # Safely get 'state'
            else:
                state = 'Not found'
        except Exception as e:
            state = f"Error: {e}"
    
        results.append({'Location': name, 'State': state})
    
        # Respect Nominatim's usage policy by sleeping between requests
        time.sleep(1)

    # Create DataFrame
    state_df = pd.DataFrame(results)

    return state_df