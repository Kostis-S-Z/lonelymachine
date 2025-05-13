# The Lonely Machine



> [The Lonely Machine](https://zoehatziyannaki.com/The-Lonely-Machine) is, a chthonic one, a cyborg, a critter of the Terrapolis, but above all an SF: a string figure, a sign of science fiction or fantasy, of speculative fabulation[1]which dares to stay with the trouble. It could be easily, a flaneur, one that strolls around the urban landscapes. But no, as this is no longer the case here and now, not in our times, the times we must think; the times of urgencies that need stories[2].The Lonely Machine is rather a wayfarer on an SF mode, who entangles, who tracks the lines of living and dying, who cultivates response-ability, who makes present to itself what it is doing, who lives in consequences or with consequence. It is not one that takes on reinterpreting the image of the city[3], like the flaneur, but the one who composts on a damaged planet of capitalist ruins.[4]
> 
> [1] Donna Haraway, Staying with the Trouble, (Duke University press, Durham and London, 2016), 10
[2] Haraway, 35
[3] Walter Benjamin, The Arcades Project, Harvard University Press, 2002
[4] Haraway, 36

_The Lonely Machine is an artistic research project led by [Zoe Hatziyannaki](https://zoehatziyannaki.com/), in collaboration with [Kostis S-Z](https://kostis-s-z.github.io/). For more information, click [here](https://zoehatziyannaki.com/The-Lonely-Machine)._ 

### Introduction to this space

This is the codebase of The Lonely Machine. It consits of all the code and instructions necessary to run the machine on your computer. It consists of multiple implementations and iterations of the machine since its first development in 2020. Initially, on the most explicit and human-curated method, a human would input exact coordinates and fine-tune parameters such as depth of field, camera orientation (x, y, z angles), pixel dimensions, and number of photos, and the machine would return the photo from that location. On the most abstract, bot-driven end, the user could set a bounding box on a map within which the bot would autonomously select and photograph locations, either randomly or in a structured, evenly distributed manner. Over time, this interface / communication has become increasingly human-friendly while at the same time increasing the machine's autonomy. In its latest version, the machine has the capacity for self-directed exploration and planning on the internet, based simply on a natural language human prompt of a few words. You can find a presentation of this project presented in 12/5/2025 [here](https://docs.google.com/presentation/d/1am2zM00JmAT31Lj1xEBnEJ3Jp8OZiQhpPh1kL5eIczo/edit?usp=sharing)

### History of the codebase

In its first iteration [v1 of 2020-2021], the user interacts with this software through an interactive dialog in the command line.

In its second iteration [v2 of 2023-2024], a Google Colab notebook is published that provides the user a more user-friendly, graphical interface.

In its third iteration [v3 of 2025], the lonely machine has been re-implemented as an [AI agent](https://huggingface.co/docs/smolagents/en/conceptual_guides/intro_agents). It can autonomously explore the world and take photos, without any human planning, simply by providing a prompt in natural language, e.g. "explore the southern suburbs of Athens" 


## Start here...

### Which version to pick?

- v2 is the most straightforward to get you started (no installation of any tools on your computer required!)
- v3 is the most beginner / user-friendly / autonomous version. But it requires an API key from a model provider, which is usually not free...
- v1 is the first version implemented, that requires very basic knowledge of how to use the command-line.

### Pre-requisites

- (all versions) You will need to get a [Street View API Key & Secret](https://developers.google.com/maps/documentation/streetview/get-api-key). Don't worry, it's free and relatively easy to acquire.
- (v1 & v3) [Git](https://github.com/git-guides/install-git) & [Python](https://realpython.com/installing-python/)
- (v3) You will need an API key from an agent provider, for example: [OpenAI](https://platform.openai.com/api-keys).
    - v3 of The Lonely Machine was built using [any-agent](https://github.com/mozilla-ai/any-agent), follow their documentation for more information.

## v3 - AI Agent

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

## v2 - Google Colab
[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kostis-S-Z/lonelymachine/blob/main/notebook.ipynb) 

## v1 - Command Line Interface (CLI)

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
