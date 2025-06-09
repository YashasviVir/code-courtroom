import asyncio
import textwrap

from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

from agents.agent import root_agent


async def main():
    """Runs the agent on a simple input and expects a normal response."""
    user_input = textwrap.dedent(
        """
        Double check this:
        Question:
import time

def process_data(data):
    result = []
    for i in range(len(data)):
        if data[i] not in result:
            result.append(data[i])
        else:
            continue
    return result

def get_user_input():
    raw_input = input("Enter comma-separated values: ")
    data = raw_input.split(",")
    return data

def main():
    print("Welcome to DataCleaner 1.0")
    user_data = get_user_input()


    if len(user_data) > 0:
        user_data = user_data[0]

    cleaned = process_data(user_data)
    print("Cleaned Data:", cleaned)

main()
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
    asyncio.run(main())
