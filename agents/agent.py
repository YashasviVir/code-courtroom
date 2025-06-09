from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from prompt import MAIN_PROMPT

from config import config

from .compliance_agent import compliance_agent
from .defendant_agent import defendant_agent
from .judge_agent import judge_agent
from .optimizer_agent import optimizer_agent
from .prosecutor_agent import prosecutor_agent

load_dotenv()

code_courtroom_coordinator = LlmAgent(
    name="code_courtroom_coordinator",
    model=config.model_name,
    description=("you are the judge."),
    instruction=MAIN_PROMPT,
    tools=[
        AgentTool(agent=judge_agent),
        AgentTool(agent=compliance_agent),
        AgentTool(agent=defendant_agent),
        AgentTool(agent=optimizer_agent),
        AgentTool(agent=prosecutor_agent),
    ],
)

root_agent = code_courtroom_coordinator
