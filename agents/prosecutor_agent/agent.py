from google.adk import Agent
from google.adk.tools import google_search

from config import config
from .prompt import PROSECUTOR_PROMPT

prosecutor_agent = Agent(
    model=config.model_name,
    name="prosecutor_agent",
    instruction=PROSECUTOR_PROMPT,
    output_key="prosecutor_output",
    tools=[google_search],
)