from google.adk import Agent
from google.adk.tools import google_search

from config import config
from .prompt import COMPLIANCE_PROMPT

compliance_agent = Agent(
    model=config.model_name,
    name="compliance_agent",
    instruction=COMPLIANCE_PROMPT,
    output_key="compliance_output",
    tools=[google_search],
)