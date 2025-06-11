from google.adk import Agent

from config import config

from .prompt import REWRITER_PROMPT

rewriter_agent = Agent(
    model=config.model_name,
    name="rewriter_agent",
    description="You are the rewriter of code in an AI enabled code courtroom setting. Your role is to oversee the judge's verdict and make required changes to the code if it is rejected or needs refactor.",
    instruction=REWRITER_PROMPT,
    output_key="rewriter_output",
)
