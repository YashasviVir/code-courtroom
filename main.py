import textwrap

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import Part, UserContent

from config import config
from prompt import MAIN_PROMPT
from sub_agents.compliance_agent import compliance_agent
from sub_agents.defendant_agent import defendant_agent
from sub_agents.judge_agent import judge_agent
from sub_agents.optimizer_agent import optimizer_agent
from sub_agents.prosecutor_agent import prosecutor_agent


def main():
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
    run_agent(root_agent)


async def run_agent(root_agent):
    """Runs the agent on a simple input and expects a normal response."""
    user_input = textwrap.dedent(
        """
        Double check this:
        Question: who are you.
    """
    ).strip()

    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    content = UserContent(parts=[Part(text=user_input)])
    response = ""
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        print(event)
        if event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text

    print("Response:", response)


if __name__ == "__main__":
    main()
