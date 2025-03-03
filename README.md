# The Lonely Machine

As part of The Lonely Machine, a _curious_, auxiliary application was created. This app provides an interface to the user to communicate with a bot (i.e "an autonomous program on the internet that can interact with systems or users") that explores and _photographs_ streets around the world. This bot has various degrees of autonomy in regards to what and how it will capture the scene. On the most explicit and _human_-curated level, the user inputs the exact coordinates of the scene and can tune the scenography to their liking by adjusting various variables of the photograph, such as the depth of field or the angle of the camera in the x,y,z axis, as well as the pixel dimensions or the number of photos to capture. On the most abstract, _autonomous_ and (_ro_)_bot_-curated level, the user inputs the coordinates of a bounding box on a map from which within the bot is allowed to take photos, either in a random, exploratory fashion or in a structured, evenly distributed within the space manner.

In a bit more technical terms, this application is written in Python and combines common data science practices with the use of Google's Street View API to create a local dataset of PNG images and a CSV spreadsheet to register the coordinates of the photos. 

In its first iteration of the application, the user interacts with this software through an interactive dialog in the command line.

In its second iteration, a Google Colab notebook is published that provides the user a more user-friendly, graphical interface.

TL;DR this bot can:
- Generate CSV files with location coordinates.
- Fetch Street View images based on provided locations.
- Be used as an interactive CLI tool (`interact.py`).
- Be used as an interactive notebook for Google Colab.


## Start here...

[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kostis-S-Z/lonelymachine/blob/main/notebook.ipynb) 

## Or here...

1. In your terminal, clone the repository:
```
git clone https://github.com/Kostis-S-Z/lonelymachine.git
```

2. Change directory:
```
cd lonelymachine
```

3. Install the dependencies:
```
pip install -r requirements.txt
```

4. Execute the code:

<div style="text-align: center;">

| auto\_run (minimal human involvement) | interact\_run (human-in-the-loop)  |
|---------------------------------------|------------------------------------|
| `python -m source.auto_run`           | `python -m source.interact_run.py` |

</div>

### Configuration

- Set your API key and secret as environment variables by running:
  ```sh
  export STREETVIEW_API_KEY=your_api_key
  export STREETVIEW_API_SECRET=your_api_secret
  ```
  Or provide them when prompted in the interactive tools.

- Customize default settings and parameters in the `source/the_machine/config.py` file.