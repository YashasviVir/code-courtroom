from google.adk import Agent
from google.adk.tools import google_search

from config import config
from .prompt import OPTIMIZER_PROMPT

optimizer_agent = Agent(
    model=config.model_name,
    name="optimizer_agent",
    instruction=OPTIMIZER_PROMPT,
    output_key="optimizer_output",
    tools=[google_search],
)