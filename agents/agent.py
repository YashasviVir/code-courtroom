from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from config import config

from .compliance_agent import compliance_agent
from .defendant_agent import defendant_agent
from .judge_agent import judge_agent
from .optimizer_agent import optimizer_agent
from .prompt import MAIN_PROMPT
from .prosecutor_agent import prosecutor_agent

code_courtroom_coordinator = LlmAgent(
    name="code_courtroom_coordinator",
    model=config.model_name,
    description=(
        "You are the coordinator of an AI code review courtroom. Your role is to manage the workflow between specialized agents that evaluate a developer's code based on correctness, compliance, performance, and intent. "
        "You ensure that each agent contributes their expertise and that the final decision reflects a balanced, structured judgment. "
        "You only act after receiving a user prompt containing code, developer intent, and constraints."
    ),
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
