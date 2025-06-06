from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from prompt import MAIN_PROMPT
from sub_agents.compliance_agent import compliance_agent
from sub_agents.defendant_agent import defendant_agent
from sub_agents.judge_agent import judge_agent
from sub_agents.optimzer_agent import optimizer_agent
from sub_agents.prosecutor_agent import prosecutor_agent


def main():
    MODEL = "gemini-2.5-pro-preview-05-06"

    code_courtroom_coordinator = LlmAgent(
        name="code_courtroom_coordinator",
        model=MODEL,
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


if __name__ == "__main__":
    main()
