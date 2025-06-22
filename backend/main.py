# Import config from parent directory
import json
import sys

import vertexai
from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from vertexai import agent_engines

sys.path.append("..")
from config import config

# Initialize Vertex AI
vertexai.init(
    project=config.google_cloud_project,
    location=config.google_cloud_location,
    staging_bucket="gs://" + config.google_cloud_storage_bucket,
)

# Initialize FastAPI app
app = FastAPI(
    title="Code Courtroom Backend API",
    description="Backend API for the Code Courtroom system using deployed Vertex AI agents",
    version="1.0.0",
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    vertex_ai_connected: bool
    resource_id: str


async def get_remote_app():
    """Get the deployed remote app using server-side configuration"""
    try:
        # Use the resource ID from server configuration
        resource_path = f"projects/{config.google_cloud_project}/locations/{config.google_cloud_location}/reasoningEngines/{config.default_resource_id}"

        # Get the remote app
        remote_app = agent_engines.get(resource_path)
        return remote_app
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to remote app: {str(e)}"
        )


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Code Courtroom Backend API is running", "status": "healthy"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check with Vertex AI connection status"""
    try:
        # Test Vertex AI connection
        _test_agent = await get_remote_app()
        vertex_ai_connected = True
    except Exception as _e:
        vertex_ai_connected = False

    return HealthResponse(
        status="healthy",
        service="Code Courtroom Backend API",
        version="1.0.0",
        vertex_ai_connected=vertex_ai_connected,
        resource_id=config.default_resource_id,
    )


@app.get("/sessions/{user_id}")
async def get_user_sessions(user_id: str):
    """Get all sessions for a specific user"""
    try:
        remote_app = await get_remote_app()
        sessions = remote_app.list_sessions(user_id=user_id)
        return {"success": True, "user_id": user_id, "sessions": sessions}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving sessions: {str(e)}"
        )


class StreamQueryRequest(BaseModel):
    user_id: str
    message: str


@app.post("/stream_query")
async def stream_query(request: StreamQueryRequest = Body(...)):
    """
    Stream query results from Vertex AI agent for a user.
    Each event includes 'agent', 'role', and 'text' fields for easy client parsing.
    """
    try:
        remote_app = await get_remote_app()
        remote_session = remote_app.create_session(user_id=request.user_id)
        session_id = remote_session["id"]

        def event_stream():
            for event in remote_app.stream_query(
                user_id=request.user_id,
                session_id=session_id,
                message=request.message,
            ):
                agent = event.get("author", "unknown")
                content = event.get("content", {})
                # Extract the main text if available
                text = ""
                if isinstance(content, dict):
                    parts = content.get("parts", [])
                    if parts and isinstance(parts[0], dict):
                        text = parts[0].get("text", "")
                role = content.get("role", "")

                yield json.dumps({"agent": agent, "role": role, "text": text}) + "\n"

        return StreamingResponse(event_stream(), media_type="application/x-ndjson")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error streaming query: {str(e)}")
