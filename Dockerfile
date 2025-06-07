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

# Set environment variables for PyTorch
ENV TORCH_CUDA_VERSION=cu118
ENV TORCH_NVCC_FLAGS="-Xfatbin -compress-all"

# Install dependencies using uv with specific platform
RUN uv pip install --system --platform manylinux_2_28_x86_64 -e .

# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["python", "main.py"] 