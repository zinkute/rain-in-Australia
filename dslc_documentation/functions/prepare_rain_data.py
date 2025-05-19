def prepare_rain_data(
    wind_direction_transformation = True,
    location_transformation = True,
):
    import pandas as pd
    import numpy as np
    from find_lat_long import find_lat_long
    
    # load original data frame
    rain_data_clean = pd.read_csv("E:\\ML\\rain-in-Australia\\data\\weatherAUS.csv")

    # update location name
    rain_data_clean.replace('BadgerysCreek', 'Badgerys Creek', inplace = True)
    rain_data_clean.replace('CoffsHarbour', 'Coffs Harbour', inplace = True)
    rain_data_clean.replace('NorahHead', 'Norah Head', inplace = True)
    rain_data_clean.replace('NorfolkIsland', 'Norfolk Island', inplace = True)
    rain_data_clean.replace('SydneyAirport', 'Sydney Airport', inplace = True)
    rain_data_clean.replace('WaggaWagga', 'Wagga Wagga', inplace = True)
    rain_data_clean.replace('MountGinini', 'Mount Ginini', inplace = True)
    rain_data_clean.replace('MelbourneAirport', 'Melbourne Airport', inplace = True)
    rain_data_clean.replace('GoldCoast', 'Gold Coast', inplace = True)
    rain_data_clean.replace('MountGambier', 'Mount Gambier', inplace = True)
    rain_data_clean.replace('PearceRAAF', 'RAAF Base Pearce', inplace = True)
    rain_data_clean.replace('PerthAirport', 'Perth Airport', inplace = True)
    rain_data_clean.replace('SalmonGums', 'Salmon Gums', inplace = True)
    rain_data_clean.replace('AliceSprings', 'Alice Springs', inplace = True)

    # update data type
    rain_data_clean["Date"] = pd.to_datetime(rain_data_clean["Date"])
    rain_data_clean['RainToday'] = rain_data_clean['RainToday'].map({'No': False, 'Yes': True})
    rain_data_clean['RainTomorrow'] = rain_data_clean['RainTomorrow'].map({'No': False, 'Yes': True})
    # Then convert to nullable boolean dtype
    rain_data_clean['RainToday'] = rain_data_clean['RainToday'].astype('boolean')
    rain_data_clean['RainTomorrow'] = rain_data_clean['RainTomorrow'].astype('boolean')

    # calculate sin and cos transformation for wind direction:    
    # Map 16 compass directions to degrees (22.5° intervals)
    if wind_direction_transformation == True:
        direction_to_degrees_16 = {
            'N': 0,
            'NNE': 22.5,
            'NE': 45,
            'ENE': 67.5,
            'E': 90,
            'ESE': 112.5,
            'SE': 135,
            'SSE': 157.5,
            'S': 180,
            'SSW': 202.5,
            'SW': 225,
            'WSW': 247.5,
            'W': 270,
            'WNW': 292.5,
            'NW': 315,
            'NNW': 337.5
        }

        # Convert compass to degrees
        rain_data_clean['WindGustDir_deg'] = rain_data_clean['WindGustDir'].map(direction_to_degrees_16)
        rain_data_clean['WindDir9am_deg'] = rain_data_clean['WindDir9am'].map(direction_to_degrees_16)
        rain_data_clean['WindDir3pm_deg'] = rain_data_clean['WindDir3pm'].map(direction_to_degrees_16)

        # Convert degrees to radians
        rain_data_clean['WindGustDir_rad'] = np.radians(rain_data_clean['WindGustDir_deg'])
        rain_data_clean['WindDir9am_rad'] = np.radians(rain_data_clean['WindDir9am_deg'])
        rain_data_clean['WindDir3pm_rad'] = np.radians(rain_data_clean['WindDir3pm_deg'])

        # Compute sine and cosine components
        rain_data_clean['WindGustDir_x'] = np.cos(rain_data_clean['WindGustDir_rad'])  # x-axis component
        rain_data_clean['WindGustDir_y'] = np.sin(rain_data_clean['WindGustDir_rad'])  # y-axis component

        rain_data_clean['WindDir9am_x'] = np.cos(rain_data_clean['WindDir9am_rad'])  # x-axis component
        rain_data_clean['WindDir9am_y'] = np.sin(rain_data_clean['WindDir9am_rad'])  # y-axis component

        rain_data_clean['WindDir3pm_x'] = np.cos(rain_data_clean['WindDir3pm_rad'])  # x-axis component
        rain_data_clean['WindDir3pm_y'] = np.sin(rain_data_clean['WindDir3pm_rad'])  # y-axis component

        # drop intermediate columns
        rain_data_clean.drop(columns=['WindGustDir_deg', 'WindDir9am_deg', 'WindDir3pm_deg',
                            'WindGustDir_rad',  'WindDir9am_rad', 'WindDir3pm_rad', 
                           'WindDir3pm', 'WindGustDir', 'WindDir9am'], inplace=True)
        
    # add the rows with missing country-year combinations
    all_dates = pd.date_range(start = '2007-11-01', end = '2017-06-25')
    all_dates = pd.DataFrame(all_dates)

    location_date_combinations = pd.MultiIndex.from_product([all_dates[0], rain_data_clean['Location'].unique()],
                                                             names=["Date", "Location"])
    location_date_combinations_df = pd.DataFrame(index=location_date_combinations).reset_index()
    rain_data_clean = location_date_combinations_df.merge(rain_data_clean, on=["Date", "Location"], how="left")

    if location_transformation == True:
   
        # use custom function to find latitude and longitude for each weather station
        latitude, longitude = find_lat_long(rain_data_clean['Location'].unique())
        
        # Change location to latitude and longitude
        location_coordinates = zip(rain_data_clean['Location'].unique(), latitude, longitude)
        location_coordinates_df = pd.DataFrame(location_coordinates, columns = ['Location', 'Latitude', 'Longitude'])
        rain_data_clean = rain_data_clean.merge(location_coordinates_df, on = 'Location', how = 'left')
        rain_data_clean.drop(columns=['Location'], inplace = True)
    
    # delete incorrect values (change to NaN)
    # delete incorrect Wind Speed value
    rain_data_clean.loc[rain_data_clean['WindSpeed9am'] == 130, 'WindSpeed9am'] = np.nan
    # delete incorrect evaporation value
    rain_data_clean.loc[rain_data_clean['Evaporation'] == 145, 'Evaporation'] = np.nan

    return rain_data_clean