from source.the_machine.locations.generator import create_locations
from source.the_machine.api.client import fetch_images


def main():
    """
    This script demonstrates how to generate a sample locations CSV file using
    the location generator and then fetch images using the API client.
    """
    # Generate a CSV file with sample location coordinates.
    csv_file = create_locations()
    print("Generated CSV file:", csv_file)

    # Fetch images based on the generated CSV file.
    # Note: Ensure API credentials are properly set.
    fetch_images(input_file=csv_file)


if __name__ == "__main__":
    main()
