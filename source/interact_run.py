import os
import sys
import getpass
from source.the_machine.locations.generator import create_locations
from source.the_machine.api.client import fetch_images


def prompt_for_int(prompt_message: str, default=None):
    """
    Prompt the user for an integer value with optional default.

    Args:
        prompt_message (str): The message to show for input.
        default (int, optional): The default value if Enter is pressed.

    Returns:
        int: The parsed integer.
    """
    while True:
        user_input = input(prompt_message).strip()
        if not user_input:
            if default is not None:
                return default
            continue
        try:
            return int(user_input.replace(".", "").replace(",", ""))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def generate_file():
    """
    Interactively prompt user to input bounding box and location generation parameters,
    then generate a CSV file with location coordinates.

    Returns:
        str: The file path of the generated CSV file.
    """
    print(
        "Please input the bounding box coordinates without dots or commas and press Enter."
    )
    params = {}
    params["min_lat"] = prompt_for_int("\tMinimum Latitude (South Limit): ")
    params["max_lat"] = prompt_for_int("\tMaximum Latitude (North Limit): ")
    params["min_lon"] = prompt_for_int("\tMinimum Longitude (West Limit): ")
    params["max_lon"] = prompt_for_int("\tMaximum Longitude (East Limit): ")

    # Select method for location generation.
    while True:
        method_input = (
            input(
                "Input method (1 for random, 2 for even; default is random): "
            ).strip()
            or "1"
        )
        if method_input in ["1", "2"]:
            params["method"] = "random" if method_input == "1" else "even"
            break
        else:
            print("Invalid selection. Please input 1 or 2.")

    # Number of locations to generate.
    params["n_locs"] = prompt_for_int("Number of locations (default 10): ", default=10)

    try:
        file_path = create_locations(params)
        print("CSV file created:", file_path)
        return file_path
    except Exception as e:
        print("Error generating CSV file:", e)
        sys.exit(1)


def make_request(file_path: str):
    """
    Interactively prompt user for API credentials and request parameters,
    then fetch Street View photos based on the CSV file.

    Args:
        file_path (str): The path to the CSV file with location data.
    """
    print("\n--- Fetch Street View Photos ---")
    api_key = input("Enter API key: ").strip()
    api_secret = getpass.getpass("Enter API secret (input hidden): ").strip()

    if not api_key or not api_secret:
        print("API credentials are required.")
        sys.exit(1)

    print("\nConfigure photo fetch parameters. Press Enter to use default values.")
    params = {}
    params["n_addresses"] = prompt_for_int(
        "\tNumber of photos to fetch (default 1): ", default=1
    )
    params["size"] = (
        input("\tImage size (WIDTHxHEIGHT, default 640x640): ").strip() or "640x640"
    )
    params["fov"] = input("\tField of view (default 120): ").strip() or "120"
    params["heading"] = input("\tHeading (default 0): ").strip() or "0"
    params["radius"] = input("\tRadius in meters (default 50): ").strip() or "50"
    params["pitch"] = input("\tPitch (default 10): ").strip() or "10"
    params["source"] = "default"
    params["return_error_code"] = "true"

    # Set temporary environment variables for credentials so fetch_images can access them.
    os.environ["STREETVIEW_API_KEY"] = api_key
    os.environ["STREETVIEW_API_SECRET"] = api_secret

    print("\nSending request with parameters:")
    for key, value in params.items():
        print(f"\t{key}: {value}")

    try:
        fetch_images(input_file=file_path, params=params)
    except Exception as e:
        print("An error occurred while fetching images:", e)
        sys.exit(1)


def main():
    print("Hi. This is the lonely machine. Shall we roam?")
    csv_file = generate_file()
    make_request(csv_file)
    print("Process completed.")


if __name__ == "__main__":
    main()
