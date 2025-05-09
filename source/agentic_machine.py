import argparse
import json
import uuid
from datetime import datetime
from pathlib import Path

from any_agent import AgentConfig, AnyAgent
from any_agent.tools import search_web, visit_webpage
import requests

from source.the_machine.api.auth import sign_url
from source.the_machine.api.client import get_credentials


# Define the Street View agent
def init_street_view_agent(
    instructions: str = "You are a lonely machine that wanders the digital streets of the world. "
                        "Wherever you go, you take a picture.",
    framework: str = "openai",
    model: str = "gpt-4.1-nano",
    use_web: bool = False,
) -> AnyAgent:
    tools = [get_area_details_from_name, fetch_image_from_street_view]
    if use_web:
        tools += [search_web, visit_webpage]
    return AnyAgent.create(
        agent_framework=framework,
        agent_config=AgentConfig(
            model_id=model,
            instructions=instructions,
            tools=tools,
        ),
    )


# Define the tools for the agent
def get_area_details_from_name(area_name: str) -> list[dict]:
    """
    Get details of an area based on a place name using
    the [Nominatim API](https://nominatim.org/release-docs/develop/api/Search/).

    Args:
        area_name (str): The name of the area.

    Returns:
        dict: a list of dictionaries containing details about the area, including its latitude and longitude.

    Examples:
        {
            "addresstype": "town",
            "boundingbox": [
                "38.0076080",
                "38.0876080",
                "23.4948663",
                "23.5748663"
            ],
            "class": "place",
            "display_name": "Elefsina",
            "importance": 0.5708337975898039,
            "lat": "38.0476080",
            "licence": "Data \u00a9 OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
            "lon": "23.5348663",
            "name": "\u0395\u03bb\u03b5\u03c5\u03c3\u03af\u03bd\u03b1",
            "osm_id": 26490651,
            "osm_type": "node",
            "place_id": 49761935,
            "place_rank": 18,
            "type": "town"
        }
    """
    response = requests.get(
        f"https://nominatim.openstreetmap.org/search?q={area_name}&format=json",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    response_json = json.loads(response.content.decode())

    return response_json


def fetch_image_from_street_view(
    coordinates: str, size: str, fov: int, heading: int, radius: int
) -> str:
    """
    Given some coordinates in the format of XX.XXXXXX, YY.YYYYYY and other parameters fetch a photo
    from the Google Street View API.

    Args:
        coordinates (str): Latitude and longitude in the format 'lat,lng' for example '37.9838,23.7275'.
        size (str): Image size in the format 'WIDTHxHEIGHT'.
        fov (int): Field of view.
        heading (int): Compass heading of the camera.
        pitch (int): Camera pitch.
        radius (int): Search radius in meters.

    Returns:
        str: Path to the saved image file or error message
    """
    key, secret = get_credentials()

    output_path = Path("the_photos")
    output_path.mkdir(parents=True, exist_ok=True)

    base_url = "https://maps.googleapis.com/maps/api/streetview"
    url_request = (
        f"{base_url}?key={key}&size={size}"
        f"&location={coordinates}&radius={radius}&fov={fov}"
        f"&heading={heading}&return_error_code=true"
    )

    signed_url = sign_url(input_url=url_request, secret=secret)

    response = requests.get(signed_url)

    if response.status_code == 200:
        coordinates = coordinates.replace(",", "_").replace(".", "_")
        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        uid = str(uuid.uuid4())[:3]
        filename = f"streetview_{timestamp}_{coordinates}_{uid}.jpg"
        full_path = output_path / filename
        with open(full_path, "wb") as file:
            file.write(response.content)
        return str(full_path)  # Return the full path
    else:
        raise ValueError(
            f"Error when fetching image: {response.status_code} - {response.text}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Lonely Machine. V3 - Agent form.")
    parser.add_argument(
        "--prompt",
        type=str,
        default="Fetch me an image from Acropolis, Athens",
        help="Write your prompt here. The agent will try to fetch an image from the Google Street View API.",
    )

    args = parser.parse_args()

    r = get_area_details_from_name("elefsina")
    print(r)
    exit()

    agent = init_street_view_agent()
    agent_trace = agent.run(args.prompt)
    print(agent_trace.final_output)
