from google.adk import Agent

from config import config

from .prompt import COMPLIANCE_PROMPT

compliance_agent = Agent(
    model=config.model_name,
    name="compliance_agent",
    description="You are the compliance officer in a courtroom setting. Your role is to ensure that all legal proceedings adhere to the relevant laws and regulations, and to provide guidance on compliance issues that may arise during the trial.",
    instruction=COMPLIANCE_PROMPT,
    output_key="compliance_output",
)
