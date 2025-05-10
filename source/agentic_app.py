import asyncio
from typing import Tuple, List

import gradio as gr
from any_agent import AgentTrace, AnyAgent

from source.agentic_machine import init_street_view_agent


default_instructions = (
    "You are a lonely machine that wanders the streets of the world. "
    "Wherever you go, you take a picture."
)
default_model = "gpt-4.1-mini"
default_use_web = False


def _get_photo_paths_from_agent_trace(agent_trace: AgentTrace) -> List[str]:
    paths = []
    for tool_call in agent_trace.spans:
        if tool_call.name == "fetch_image_from_street_view":
            paths.append(tool_call.attributes["output.value"])

    return list(set(paths))  # make sure there are no duplicates


def query_agent(
    agent: AnyAgent, user_input: str
) -> Tuple[AnyAgent | None, List[str] | None, str]:
    # Initialize agent for the first time
    if not agent:
        agent, _ = initialize_agent()

    agent_trace = agent.run(user_input)

    photo_paths = _get_photo_paths_from_agent_trace(agent_trace)

    print(f"Fetched these photos: {photo_paths}")

    return agent, photo_paths, agent_trace.final_output


def initialize_agent(
    agent: AnyAgent | None = None,
    instructions: str = default_instructions,
    model: str = default_model,
    use_web: bool = default_use_web,
):
    # If the agent was already initialized, reset it
    if agent:
        agent.exit()

    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    updated_agent = init_street_view_agent(
        instructions=instructions,
        model=model,
        use_web=use_web,
    )
    return updated_agent, "The Machine has been updated."


def gradio_app():
    with gr.Blocks() as app:
        gr.Markdown("## The Lonely Machine")

        agent = gr.State()

        with gr.Accordion("Configure the machine", open=False):
            with gr.Row():
                instructions = gr.Textbox(
                    label="Instructions",
                    value=default_instructions,
                )
            with gr.Row():
                model = gr.Dropdown(
                    label="Model",
                    choices=[
                        "gpt-4.1",
                        "gpt-4.1-mini",
                        "gpt-4.1-nano",
                        "o3",
                        "o4-mini",
                    ],
                    value=default_model,
                )
            with gr.Row():
                use_web = gr.Checkbox(label="Use Web", value=default_use_web)

            agent_status = gr.Markdown("")

            gr.Button("Save").click(
                initialize_agent,
                inputs=[agent, instructions, model, use_web],
                outputs=[agent, agent_status],
            )

        input_text = gr.Textbox(
            label="Where should I wander?",
            placeholder="A street, a neighborhood, a city, a country, a place...",
        )
        output_gallery = gr.Gallery(label="This is what I saw:")

        status = gr.Markdown(label="Response", value="")
        submit_button = gr.Button("Wander")
        submit_button.click(
            query_agent,
            inputs=[agent, input_text],
            outputs=[agent, output_gallery, status],
        )

    app.launch()


if __name__ == "__main__":
    gradio_app()
