# Code Courtroom

Code Courtroom is an AI-powered platform that simulates a courtroom environment for advanced code review. Leveraging the power of multiple specialized agents—Judge, Prosecutor, Defendant, Compliance, Optimizer, and Rewriter—the platform provides a collaborative and adversarial process to analyze, critique, and improve code submissions. Each agent is designed to fulfill a unique role, ensuring a comprehensive review that mimics real-world legal proceedings for code quality and compliance.

The backend is built with Python, orchestrating agent logic and business rules, while the frontend is a modern TypeScript/React application for seamless user interaction. The project uses [Google ADK](https://google.github.io/adk-docs/) for enhanced AI agent capabilities and integration, enabling robust communication and workflow automation between agents. With support for Astral UV and Bun, the development workflow is fast and efficient, and Docker ensures easy deployment across environments.

## Features
- **AI Agents:** Modular agents for different roles in code review and compliance.
- **Interactive Frontend:** User-friendly web interface built with React and Vite.
- **Backend API:** Python backend for agent orchestration and business logic.
- **Docker Support:** Easy deployment with Docker for both frontend and backend.

## Folder Structure
```
code-courtroom/
├── agents/           # Python modules for each AI agent
├── backend/          # Backend API and services (Python)
├── frontend/         # Frontend app (React + Vite)
├── config.py         # Configuration file
├── deploy.py         # Deployment script
├── Dockerfile        # Dockerfile for backend
├── requirements.txt  # Python dependencies
├── pyproject.toml    # Python project metadata
└── README.md         # Project documentation
```

## Getting Started

### Prerequisites
- Python 3.11+
- [Astral UV](https://docs.astral.sh/uv/) (for fast Python package management)
- [Bun](https://bun.sh/) (for frontend package management)
- Docker (optional, for containerized deployment)

### Backend Setup
1. Install Python dependencies:
   ```bash
   uv sync
   ```
2. from the `backend/` directory:
   ```bash
   uv run run.py
   ```

### Frontend Setup
1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install Node.js dependencies:
   ```bash
   bun install
   ```
3. Start the development server:
   ```bash
   bun run dev
   ```

### Docker Deployment
Build and run the full stack using Docker:
```bash
docker build -t code-courtroom-backend .
cd frontend
docker build -t code-courtroom-frontend .
```

## Usage
- Access the frontend at `http://localhost:5173` (default Vite port).
- The backend API runs on `http://localhost:8000` (or as configured).
- Interact with the agents through the web UI to submit code, receive feedback, and iterate.
