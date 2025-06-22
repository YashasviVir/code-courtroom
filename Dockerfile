# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (if using requirements.txt)
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# If using pyproject.toml/poetry, comment out above and use below instead:
# COPY pyproject.toml ./
# COPY uv.lock ./
# RUN pip install --upgrade pip && pip install uv
# RUN uv pip install --system --require-hashes uv.lock

# Copy project
COPY . .

# Expose port (Cloud Run will set $PORT)
EXPOSE 8080

# Start the app with uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
