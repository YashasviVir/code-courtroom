from google.adk import Agent
from google.adk.tools import google_search

from config import config

from .prompt import PROSECUTOR_PROMPT

prosecutor_agent = Agent(
    model=config.model_name,
    name="prosecutor_agent",
    description="You are the prosecutor in a courtroom setting. Your role is to present the case against the defendant, gather evidence, and argue for a conviction based on the facts of the case.",
    instruction=PROSECUTOR_PROMPT,
    output_key="prosecutor_output",
    tools=[google_search],
)
