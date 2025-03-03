import os
from pathlib import Path
import configparser
import pandas as pd
import requests
from ..config import (
    API_KEY_ENV,
    API_SECRET_ENV,
    DEFAULT_CONFIG_FILE,
    DEFAULT_SAVE_DIR,
    STREETVIEW_API_URL,
    DEFAULT_API_PARAMS,
)
from .auth import sign_url
from ..locations.processor import preprocess_location


def _get_credentials():
    """
    Retrieve API credentials from environment variables or a configuration file.

    Returns:
        tuple: (api_key, api_secret) if available, otherwise (None, None)
    """
    key = os.environ.get(API_KEY_ENV)
    secret = os.environ.get(API_SECRET_ENV)

    if key and secret:
        return key, secret

    if os.path.exists(DEFAULT_CONFIG_FILE):
        config = configparser.ConfigParser()
        config.read(DEFAULT_CONFIG_FILE)
        if "credentials" in config:
            return config["credentials"].get("key"), config["credentials"].get("secret")

    return None, None


def fetch_image_from_location(
    location: str, key: str, secret: str, params: dict, filename: str
):
    """
    Construct and send a request to the Street View API.

    Args:
        location (str): Formatted location string.
        filename (str): Name for the saved image file.
        key (str): Google API key.
        secret (str): Google API signing secret.
        params (dict): Parameters for the Street View API request.

    Returns:
        None: The image is saved to disk if the request is successful.
    """
    url_request = (
        f"{STREETVIEW_API_URL}?key={key}&size={params['size']}"
        f"&location={location}&radius={params['radius']}&fov={params['fov']}"
        f"&heading={params['heading']}&return_error_code={params['return_error_code']}"
    )
    if params.get("source") and params["source"] != "default":
        url_request += f"&source={params['source']}"
    if params.get("pitch"):
        url_request += f"&pitch={params['pitch']}"

    signed_url = sign_url(input_url=url_request, secret=secret)

    print("Sending request:", signed_url)
    ans = input("Yes? (y/n) ")
    if ans.lower() == "y":
        try:
            response = requests.get(signed_url)
            response.raise_for_status()
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Image saved: {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image: {e}")


def fetch_images(
    input_file: str, params: dict = DEFAULT_API_PARAMS, save_dir: str = DEFAULT_SAVE_DIR
):
    """
    Fetch Street View photos for locations specified in a CSV file.

    Args:
        input_file (str): Path to the CSV file containing location data.
        params (dict, optional): API parameters for the request; defaults to DEFAULT_API_PARAMS.
        save_dir (str): The directory where the fetched images will be saved.
    """
    key, secret = _get_credentials()
    if not key or not secret:
        print("Credentials not available. Set environment variables or update config.")
        return

    Path.mkdir(Path(save_dir), parents=True, exist_ok=True)

    df = pd.read_csv(input_file)

    for index, row in df.iterrows():
        location, filename = preprocess_location(index, row)
        fetch_image_from_location(
            location=location,
            key=key,
            secret=secret,
            params=params,
            filename=os.path.join(save_dir, filename),
        )
        if index + 1 >= params.get("n_addresses", 1):
            break
