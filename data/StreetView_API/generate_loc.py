import numpy as np

# Bounding box coordinates from within athens
# https://boundingbox.klokantech.com/

min_lat = 37946894
max_lat = 38092677
min_lon = 23665374
max_lon = 23926643


lats = np.arange(min_lat, max_lat, 5000)
lons = np.arange(min_lon, max_lon, 3000)

i = 0
for lat in lats:
    for lon in lons:
        i += 1
        lat_i = str(lat)
        lon_i = str(lon)
        lat_i = lat_i[:2] + '.' + lat_i[2:]
        lon_i = lon_i[:2] + '.' + lon_i[2:]
        print(lat_i + ',' + lon_i)
        if i == 3:
            exit()
