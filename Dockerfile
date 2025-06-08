# Use Python 3.12 as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Install PyTorch first
RUN pip install torch==2.6.0

# Install other dependencies using uv
RUN uv pip install --system -e .

# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["python", "main.py"] 