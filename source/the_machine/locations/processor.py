from ..config import DEFAULT_LOCATION_TYPE


def preprocess_location(index: int, item) -> tuple:
    """
    Process a location row into a formatted location string and image filename.

    Args:
        index (int): Row index.
        item (pandas.Series): A row with location data.

    Returns:
        tuple: (location, filename)
    """
    if DEFAULT_LOCATION_TYPE == "coordinates":
        lat_str = str(item["lat"])
        long_str = str(item["long"])
        location = f"{lat_str},{long_str}"
        loc_str = f"{lat_str}_{long_str}".replace(".", "")
    else:
        location = f"{item['Address']}, {item['City']}, {item['Country']}".replace(
            " ", ""
        )
        loc_str = item["Address"].replace(".", "_").replace(" ", "")
    filename = f"view_{index}_{loc_str}.jpg"
    return location, filename
