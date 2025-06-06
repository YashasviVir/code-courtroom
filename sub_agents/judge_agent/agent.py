from google.adk import Agent
from google.adk.tools import google_search

from config import config
from .prompt import JUDGE_PROMPT

judge_agent = Agent(
    model=config.model_name,
    name="judge_agent",
    instruction=JUDGE_PROMPT,
    output_key="judge_output",
    tools=[google_search],
)