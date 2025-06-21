from google.adk import Agent

from config import config

from .prompt import DEFENDANT_PROMPT

defendant_agent = Agent(
    model=config.model_name,
    name="defendant_agent",
    description="You are the defendant in a courtroom setting. Your role is to respond to accusations, present your case, and defend yourself against the charges brought by the prosecution.",
    instruction=DEFENDANT_PROMPT,
    output_key="defendant_output",
)
