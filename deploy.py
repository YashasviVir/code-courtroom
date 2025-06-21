import vertexai
from vertexai import agent_engines

from agents.agent import root_agent
from config import config

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