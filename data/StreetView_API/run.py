from generate_loc import create_file
from fetch_loc import fetch_photos

def generate_file():
    print("Please input the bounding box coordinates, without any dots or commas and press Enter.")
    params = {}
    params['min_lat'] = int(input("\t 1st corner:"))
    params['max_lat'] = int(input("\t 2nd corner:"))
    params['min_lon'] = int(input("\t 3rd corner:"))
    params['max_lon'] = int(input("\t 4th corner:"))
    while True:
        print("Please input the number 1 for random method or 2 for even method.")
        ans = int(input('\t Method:'))
        if ans == 1:
            params['method'] = 'random'
            break
        elif ans == 2:
            params['method'] = 'even'
            break
        else:
            pass
    print("Please input the number of coordinates you want to generate. E.g 1,10,100")
    params['n_locs'] = int(input("\t Number of locations:"))
    file_path = create_file(params)
    print("File created: ", file_path)
    return file_path

def make_request(file_path):
    print("\n\n\t ~Now we will fetch the photos from Google Street View~\n")
    print("Please input the key:")
    key = input("\t Key:")
    print("Please input the secret:")
    secret = input("\t Secret:")

    params = {}
    print("\n\n\t ~Now we will set the parameters of the photos.~ \nIf you want to use default values just press Enter at each field.\n")
    print("Please input the number of photos to fetch. Values [1,?], default is 1")
    params['n_addresses'] = int(input("\t Number of photos:") or '1')
    print("Please input the size of images (Max 640x640). Values WIDTHxHEIGHT, e.g 320x640, default is 640x640")
    params['size'] = input("\t Size in pixels:") or '640x640'
    print("Please input the horizontal field of view (FOV). Values [0, 120], default is 120")
    params['fov'] = input("\t Field of View:") or '120'
    print("Please input the heading. It indicates the compass heading of the camera 0/360: North, 90: East, 180: South. Values [0, 360], default is 0.")
    params['heading'] = input("\t Heading:") or '0'
    print("Please input the radius in meters, to search for a panorama, centered on the given latitude and longitude. Values [0, ?], default is 50.")
    params['radius'] = input("\t Radius:") or '50'
    print("Please input the pitch. Specifies the up or down angle of the camera relative to the Street View vehicle. Values [-90,90], default is 10.")
    params['pitch'] = input("\t Pitch:") or '10'
    params['source'] = 'default'  # 'default' Street View default view, 'outdoor' limits searches to outdoor collections
    params['return_error_code'] = 'true'

    print("\nParameters are set:", params)
    print("\n\n\t ~Sending request!~ \n")
    fetch_photos(key, secret, file_path, params)

if __name__ == "__main__":
    print("\n\t ~Welcome to the Street View Photographer~")
    file_path = generate_file()
    make_request(file_path)
