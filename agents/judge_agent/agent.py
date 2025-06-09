from google.adk import Agent

from config import config

from .prompt import JUDGE_PROMPT

judge_agent = Agent(
    model=config.model_name,
    name="judge_agent",
    description="You are the judge in a courtroom setting. Your role is to oversee the proceedings, ensure fairness, and make rulings based on the law and evidence presented.",
    instruction=JUDGE_PROMPT,
    output_key="judge_output",
)
