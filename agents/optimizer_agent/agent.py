from google.adk import Agent
from google.adk.tools import google_search

from config import config

from .prompt import OPTIMIZER_PROMPT

optimizer_agent = Agent(
    model=config.model_name,
    name="optimizer_agent",
    description="You are the optimizer in a courtroom setting. Your role is to analyze the case details, identify areas for improvement, and suggest optimizations to enhance the efficiency and effectiveness of the legal proceedings.",
    instruction=OPTIMIZER_PROMPT,
    output_key="optimizer_output",
    tools=[google_search],
)
