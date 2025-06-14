import asyncio

import vertexai
from vertexai import agent_engines

from agents.agent import root_agent
from config import config

# import textwrap

# from google.adk.runners import InMemoryRunner
# from google.genai.types import Part, UserContent


async def main():
    vertexai.init(
        project=config.google_cloud_project,
        location=config.google_cloud_location,
        staging_bucket="gs://" + config.google_cloud_storage_bucket,
    )

    remote_app = agent_engines.create(
        display_name="Code Courtroom Agent",
        description="An agent that helps with code compliance in a courtroom setting.",
        agent_engine=root_agent,
        requirements=["google-cloud-aiplatform[adk,agent_engines]"],
    )

    print("Resource Name = ", remote_app.resource_name)
    print("Display Name = ", remote_app.display_name)


#     user_input = textwrap.dedent("""
# Double check this:
# Question:
# import time

# def process_data(data):
#     result = []
#     for i in range(len(data)):
#         if data[i] not in result:
#             result.append(data[i])
#         else:
#             continue
#     return result

# def get_user_input():
#     raw_input = input("Enter comma-separated values: ")
#     data = raw_input.split(",")
#     return data

# def main():
#     print("Welcome to DataCleaner 1.0")
#     user_data = get_user_input()


#     if len(user_data) > 0:
#         user_data = user_data[0]

#     cleaned = process_data(user_data)
#     print("Cleaned Data:", cleaned)

# main()
#     """).strip()

#     runner = InMemoryRunner(agent=root_agent)
#     session = await runner.session_service.create_session(
#         app_name=runner.app_name, user_id="test_user"
#     )
#     content = UserContent(parts=[Part(text=user_input)])
#     response = ""
#     async for event in runner.run_async(
#         user_id=session.user_id,
#         session_id=session.id,
#         new_message=content,
#     ):
#         print(event)
#         if event.content.parts and event.content.parts[0].text:
#             response = event.content.parts[0].text

#     print("Response:", response)


if __name__ == "__main__":
    asyncio.run(main())
