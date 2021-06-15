import pandas as pd
import requests
from sign_request import sign_url

url = 'https://maps.googleapis.com/maps/api/streetview?'

location_type = 'address'  # 'coordinates' , 'address'

# input_file = 'athens.csv'
input_file = 'athens.csv'
save_dir = 'streetviews/test/'

n_addresses = 1

size = '640x640'  # max is 640x640
fov = '120'  # [0-120]: horizontal field of view
heading = '0'  # [0-360]: indicates the compass heading of the camera 0/360: North, 90: East, 180: South
radius = '50'  # [0-?]: radius in meters, to search for a panorama, centered on the given latitude and longitude.
pitch = '10'  # [-90, 90]: specifies the up or down angle of the camera relative to the Street View vehicle
source = 'default'  # 'default' Street View default view, 'outdoor' limits searches to outdoor collections
return_error_code = 'true'  # indicates whether the API should return an error code when no image is found


def main():
    df = pd.read_csv(input_file)

    for index, row in df.iterrows():
        location, filename = preprocess_location(index, row)
        construct_request(location, filename)
        if index + 1 >= n_addresses: break


def preprocess_location(index, item):
    if location_type == 'coordinates':
        lat_str = str(item['lat'])
        long_str = str(item['long'])
        location = lat_str + ',' + long_str
        loc_str = f'{lat_str}_{long_str}'.replace('.', '')
    else:
        location = f"{item['Address']}, {item['City']}, {item['Country']}".replace(' ', '')
        loc_str = item['Address'].replace('.', '_').replace(' ', '')

    filename = f'view_{index}_{loc_str}.jpg'

    return location, filename


def construct_request(location, filename):
    url_request = url + '&key=' + key + '&size=' + size + '&location=' + location + '&radius=' + radius + '&fov=' + fov\
                  + '&heading=' + heading + '&return_error_code' + return_error_code

    signed_url = sign_url(input_url=url_request, secret=secret)

    print('Sending: ', signed_url)
    ans = input('Yes? (y/n)')
    if ans == 'y':
        response = requests.get(signed_url)
        if response.ok:
            print('Success!')
            with open(save_dir + filename, 'wb') as file:
                file.write(response.content)
        else:
            print(response.content)

        response.close()


if __name__ == "__main__":
    with open('../../../DONT_PUBLISH_ME') as f:
        for i, line in enumerate(f):
            if i == 2:
                key = line.rstrip()
            if i == 4:
                secret = line.rstrip()
                break
    main()
