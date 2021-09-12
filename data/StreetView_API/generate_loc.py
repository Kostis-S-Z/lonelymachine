import numpy as np
import pandas as pd
import os

# Bounding box coordinates from within athens
# https://boundingbox.klokantech.com/

params_def = {
    "min_lat": 37946894,
    "max_lat": 38092677,
    "min_lon": 23665374,
    "max_lon": 23926643,
    "method": 'random',  # random or even
    "n_locs": 1_000  # approximate for even
}


def create_file(params=params_def):
    methods = {'random': randomly_generate(params), 'even': evenly_generate(params)}
    latitudes, longitudes = methods[params['method']]
    print(f'Generated {len(latitudes)} latitudes, {len(longitudes)} longitudes. '
        f'Creating {len(latitudes)*len(longitudes)} points.')
    locations = generate_coordinates(latitudes, longitudes)
    locs_df = pd.DataFrame(locations, columns=['Address', 'City', 'Country', 'lat', 'long'])
    print(locs_df.shape)
    filename = f"athens_{params['method']}.csv"
    locs_df.to_csv(filename, index=False)
    return os.getcwd() + '/' + filename

def evenly_generate(params):
    n_points = params['n_locs'] ** 0.5
    lat_range = params['max_lat'] - params['min_lat']
    lon_range = params['max_lon'] - params['min_lon']
    lat_step_size = lat_range // n_points
    lon_step_size = lon_range // n_points

    lats = np.arange(params['min_lat'], params['max_lat'], lat_step_size)
    lons = np.arange(params['min_lon'], params['max_lon'], lon_step_size)

    return lats, lons


def randomly_generate(params):
    lats = np.random.uniform(params['min_lat'], params['max_lat'], int(params['n_locs'] ** 0.5))
    lons = np.random.uniform(params['min_lon'], params['max_lon'], int(params['n_locs'] ** 0.5))
    return lats, lons


def generate_coordinates(lats, lons):
    locs = {'Address': [], 'City': [], 'Country': [], 'lat': [], 'long': []}
    for lat in lats:
        for lon in lons:
            lat_i = str(lat)
            lon_i = str(lon)
            lat_i = lat_i[:2] + '.' + lat_i[2:]
            lon_i = lon_i[:2] + '.' + lon_i[2:]
            locs['Address'].append('-')
            locs['City'].append('-')
            locs['Country'].append('-')
            locs['lat'].append(lat_i)
            locs['long'].append(lon_i)
    return locs
