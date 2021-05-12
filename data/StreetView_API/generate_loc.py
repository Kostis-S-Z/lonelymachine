import numpy as np
import pandas as pd

# Bounding box coordinates from within athens
# https://boundingbox.klokantech.com/

min_lat = 37946894
max_lat = 38092677
min_lon = 23665374
max_lon = 23926643

method = 'random'  # random or even
n_locs = 10_000  # approximate for even


def evenly_generate():
    n_points = n_locs ** 0.5
    lat_range = max_lat - min_lat
    lon_range = max_lon - min_lon
    lat_step_size = lat_range // n_points
    lon_step_size = lon_range // n_points

    lats = np.arange(min_lat, max_lat, lat_step_size)
    lons = np.arange(min_lon, max_lon, lon_step_size)

    return lats, lons


def randomly_generate():
    lats = np.random.uniform(min_lat, max_lat, int(n_locs ** 0.5))
    lons = np.random.uniform(min_lon, max_lon, int(n_locs ** 0.5))
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


methods = {'random': randomly_generate(), 'even': evenly_generate()}
latitudes, longitudes = methods[method]
print(f'Generated {len(latitudes)} latitudes, {len(longitudes)} longitudes. '
      f'Creating {len(latitudes)*len(longitudes)} points.')
locations = generate_coordinates(latitudes, longitudes)
locs_df = pd.DataFrame(locations, columns=['Address', 'City', 'Country', 'lat', 'long'])
print(locs_df.shape)
locs_df.to_csv(f'athens_{method}.csv', index=False)
