# The Lonely Machine

As part of The Lonely Machine, a curious and auxiliary application has evolved over several iterations. This app provides users with an interface to communicate with a bot—an autonomous program capable of exploring and photographing streets around the world. This codebase consists of multiple implementations and iterations of the machine. Initially, on the most explicit and human-curated method, a human would input exact coordinates and fine-tune parameters such as depth of field, camera orientation (x, y, z angles), pixel dimensions, and number of photos, and the machine would return the photo from that location. On the most abstract, bot-driven end, the user could set a bounding box on a map within which the bot would autonomously select and photograph locations, either randomly or in a structured, evenly distributed manner. Over time, this interface / communication has become increasingly human-friendly while at the same time increasing the machine's autonomy. In its latest version, the machine has the capacity for self-directed exploration and planning on the internet, based simply on a natural language human prompt of a few words.

In its first iteration [v1 of 2020-2021], the user interacts with this software through an interactive dialog in the command line.

In its second iteration [v2 of 2023-2024], a Google Colab notebook is published that provides the user a more user-friendly, graphical interface.

In its third iteration [v3 of 2025], the lonely machine has been re-implemented as an [AI agent](https://huggingface.co/docs/smolagents/en/conceptual_guides/intro_agents). It can autonomously explore the world and take photos, without any human planning, simply by providing a prompt in natural language, e.g. "explore the southern suburbs of Athens" 


## Start here...

### v3 - AI Agent

1. In your terminal, clone the repository:
```
git clone https://github.com/Kostis-S-Z/lonelymachine.git
```

2. Change directory:
```
cd lonelymachine
```

3. Set your API key and secret as environment variables by running:
  ```sh
  export STREETVIEW_API_KEY=your_api_key
  export STREETVIEW_API_SECRET=your_api_secret
  export OPENAI_API_KEY=your_api_key  # only necessary for v3 - Agent
  ```
  Or copy `.env.sample` and rename it to `.env` and add them there.

  Or provide them when prompted in the interactive tools.

4. Create a virtual environment (optional but recommended):
```
python -m venv venv
```

   and then activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install the dependencies:
```
pip install -r requirements-agent.txt
```

6. Run the agent with a prompt of your choice, for example:
```
python -m source.agent --prompt "explore the southern suburbs of Athens"
```

7. The resulting photos will be saved under `source/the_photos/`. The filename is a timestamp, the coordinates of that photo and a 3-digit unique id.

### v2 - Google Colab
[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kostis-S-Z/lonelymachine/blob/main/notebook.ipynb) 

### v1 - Command Line Interface (CLI)

Follow steps 1-3 from v3 above to clone the repository and set up a virtual environment, and then:

4. Install the dependencies:
```
pip install -r requirements.txt
```

5. Execute the code:

<div style="text-align: center;">

| auto\_run (minimal human involvement) | interact\_run (human-in-the-loop)  |
|---------------------------------------|------------------------------------|
| `python -m source.auto_run`           | `python -m source.interact_run.py` |

</div>

6. (Optional) You can customize the default settings and parameters in the `source/the_machine/config.py` file. 
