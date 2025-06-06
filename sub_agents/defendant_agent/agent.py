from google.adk import Agent
from google.adk.tools import google_search

from config import config
from .prompt import DEFENDANT_PROMPT

defendant_agent = Agent(
    model=config.model_name,
    name="defendant_agent",
    instruction=DEFENDANT_PROMPT,
    output_key="defendant_output",
    tools=[google_search],
)