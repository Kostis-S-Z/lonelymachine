import argparse
from pathlib import Path

from any_agent import AgentConfig, AnyAgent
import requests

from source.the_machine.api.auth import sign_url
from source.the_machine.api.client import get_credentials


# Define the Street View agent
def init_street_view_agent(framework: str = "openai", model: str = "gpt-4.1-nano") -> AnyAgent:
    return AnyAgent.create(
        agent_framework=framework,
        agent_config=AgentConfig(
            model_id=model,
            instructions="You are an agent that fetches images from Google Street View API. The user will provide a "
                         "location and you will have to first find the coordinates of that location in the format "
                         "XX.XXXXXX, YY.YYYYYY (for example 38.059576,23.737887) and then fetch an image from the "
                         "Google Street View API. If the user asks for multiple photos from multiple place the you "
                         "will return more than one image, for each one of the places. "
                         "If the user asks for certain parameters, you will have to "
                         "use them. If the user does not provide any parameters you will have to use the default ones. "
                         "The default parameters are: size=640x640, fov=120, heading=0, pitch=10, radius=50."
                         "If there is an error in the request, you will return the error code and the error message"
                         "and explicitly say there was an error.",
            tools=[fetch_image_from_street_view],
        ),
    )


# Define the Tool for the agent
def fetch_image_from_street_view(location: str, size: str, fov: int, heading: int, pitch: int, radius: int) -> str:
    """
    Fetch an image from the Google Street View API.

    Args:
        location (str): Latitude and longitude in the format 'lat,lng'.
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
        f"&location={location}&radius={radius}&fov={fov}"
        f"&heading={heading}&return_error_code=true"
    )

    signed_url = sign_url(input_url=url_request, secret=secret)

    response = requests.get(signed_url)

    if response.status_code == 200:
        location = location.replace(",", "_").replace(".", "_")
        filename = f"streetview_{location}.jpg"
        full_path = output_path / filename
        with open(full_path, "wb") as file:
            file.write(response.content)
        return str(full_path)  # Return the full path
    else:
        return f"Error when fetching image: {response.status_code} - {response.text}"



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Lonely Machine. V3 - Agent form.")
    parser.add_argument(
        "--prompt",
        type=str,
        default="Fetch me an image from Acropolis, Athens",
        help="Write your prompt here. The agent will try to fetch an image from the Google Street View API.",
    )

    args = parser.parse_args()

    agent = init_street_view_agent()
    agent_trace = agent.run(args.prompt)
    print(agent_trace.final_output)