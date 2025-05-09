import asyncio
from typing import Tuple, List

import gradio as gr
from any_agent import AgentTrace

from source.agentic_machine import init_street_view_agent


def _get_photo_paths_from_agent_trace(agent_trace: AgentTrace) -> List[str]:
    paths = []
    for tool_call in agent_trace.spans:
        if tool_call.name == "fetch_image_from_street_view":
            paths.append(tool_call.attributes["output.value"])

    return list(set(paths))  # make sure there are no duplicates


def query_agent(user_input: str, instructions: str, model: str, use_web: bool) -> Tuple[List[str] | None, str]:
    # Add an event loop for the agent to run in parallel with gradio
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)

    # Initialize the agent and run it with the user input
    agent = init_street_view_agent(instructions=instructions, model=model, use_web=use_web)
    agent_trace = agent.run(user_input)

    if "error" in agent_trace.final_output.lower():
        return None, agent_trace.final_output
    return _get_photo_paths_from_agent_trace(agent_trace), agent_trace.final_output


def gradio_app():
    with gr.Blocks() as app:
        gr.Markdown("## The Lonely Machine")
        gr.Markdown()
        with gr.Accordion("Configure the machine", open=False):
            with gr.Row():
                instructions = gr.Textbox(
                    label="Instructions",
                    value="You are a lonely machine that wanders the digital streets of the world.",
                )
            with gr.Row():
                model = gr.Dropdown(
                    label="Model",
                    choices=["gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "o3", "o4-mini"],
                    value="gpt-4.1",
                )
            with gr.Row():
                use_web = gr.Checkbox(label="Use Web", value=False)

        input_text = gr.Textbox(
            label="Where should I wander?",
            placeholder="A street, a neighborhood, a city, a country, a place...",
        )
        output_gallery = gr.Gallery(label="This is what I saw:")

        status = gr.Markdown(label="Response", value="")
        submit_button = gr.Button("Wander")
        submit_button.click(
            query_agent, inputs=[input_text, instructions, model, use_web], outputs=[output_gallery, status]
        )

    app.launch()


if __name__ == "__main__":
    gradio_app()
