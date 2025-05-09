import os

STREETVIEW_API_URL = "https://maps.googleapis.com/maps/api/streetview"


DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".streetview_photographer")
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "config.ini")

DEFAULT_LOCATION_TYPE = "coordinates"
DEFAULT_INPUT_FILE = "athens_random.csv"
DEFAULT_SAVE_DIR = os.path.join(os.getcwd(), "streetviews")

DEFAULT_API_PARAMS = {
    "n_addresses": 1,
    "size": "640x640",  # max is 640x640
    "fov": "120",  # [0-120]: horizontal field of view
    "heading": "0",  # [0-360]: compass heading of the camera
    "radius": "50",  # meters to search for a panorama
    "pitch": "10",  # [-90, 90]: up/down angle of the camera
    "source": "default",  # viewing mode: 'default' or 'outdoor'
    "return_error_code": "true",
}

# Default bounding box for Athens (can be over-written)
DEFAULT_LOCATION_PARAMS = {
    "min_lat": 37946894,
    "max_lat": 38092677,
    "min_lon": 23665374,
    "max_lon": 23926643,
    "method": "random",  # sample method: 'random' or 'even'
    "n_locs": 10,  # number of photos / locations to generate
}
