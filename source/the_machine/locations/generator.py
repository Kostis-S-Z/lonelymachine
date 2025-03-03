from typing import Tuple

import numpy as np
import pandas as pd
import os
from ..config import DEFAULT_LOCATION_PARAMS


def _evenly_generate(params: dict) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate evenly spaced latitude and longitude arrays based on the bounding box.

    Args:
        params (dict): Contains min/max latitude/longitude and n_locs.

    Returns:
        tuple: Arrays of latitudes and longitudes.
    """
    n_points = params["n_locs"] ** 0.5
    lat_range = params["max_lat"] - params["min_lat"]
    lon_range = params["max_lon"] - params["min_lon"]
    lat_step = int(lat_range // n_points)
    lon_step = int(lon_range // n_points)
    lats = np.arange(params["min_lat"], params["max_lat"], lat_step, dtype=int)
    lons = np.arange(params["min_lon"], params["max_lon"], lon_step, dtype=int)
    return lats, lons


def _randomly_generate(params: dict) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate random latitude and longitude arrays based on the bounding box.

    Args:
        params (dict): Contains min/max latitude/longitude and n_locs.

    Returns:
        tuple: Arrays of latitudes and longitudes.
    """
    n_points = int(params["n_locs"] ** 0.5)
    rng = np.random.default_rng(seed=42)
    lats = rng.integers(params["min_lat"], params["max_lat"], n_points)
    lons = rng.integers(params["min_lon"], params["max_lon"], n_points)
    return lats, lons


def _generate_coordinates(lats: np.ndarray, lons: np.ndarray):
    """
    Generate location coordinates along with placeholder address information.

    Args:
        lats (array-like): Array of latitude values.
        lons (array-like): Array of longitude values.

    Returns:
        dict: Dictionary with columns 'Address', 'City', 'Country', 'lat', 'long'.
    """
    locs = {"Address": [], "City": [], "Country": [], "lat": [], "long": []}
    for lat in lats:
        for lon in lons:
            lat_str = str(lat)
            lon_str = str(lon)
            # Insert decimal point as needed
            lat_fmt = lat_str[:2] + "." + lat_str[2:]
            lon_fmt = lon_str[:2] + "." + lon_str[2:]
            locs["Address"].append("-")
            locs["City"].append("-")
            locs["Country"].append("-")
            locs["lat"].append(lat_fmt)
            locs["long"].append(lon_fmt)
    return locs


def create_locations(params: dict = DEFAULT_LOCATION_PARAMS) -> str:
    """
    Create a CSV file with generated location coordinates.

    Args:
        params (dict, optional): Generation parameters; defaults to DEFAULT_LOCATION_PARAMS.

    Returns:
        str: The file path of the generated CSV.
    """
    methods = {"random": _randomly_generate(params), "even": _evenly_generate(params)}
    latitudes, longitudes = methods[params["method"]]

    print(latitudes, longitudes)
    print(
        f"Generated {len(latitudes)} latitudes, {len(longitudes)} longitudes. "
        f"Creating {len(latitudes) * len(longitudes)} points."
    )
    coordinates = _generate_coordinates(latitudes, longitudes)
    df = pd.DataFrame(
        coordinates, columns=["Address", "City", "Country", "lat", "long"]
    )
    filename = f"athens_{params['method']}.csv"
    df.to_csv(filename, index=False)
    print(f"CSV file created: {os.path.join(os.getcwd(), filename)}")
    return os.path.join(os.getcwd(), filename)
