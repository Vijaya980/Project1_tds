# Use official Python base image
FROM python:3.12.8-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    NODE_VERSION=18

# Install system dependencies & Node.js (for npm & Prettier)
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g prettier@3.4.2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install PyTorch without CUDA support. Should remove for production or machines which do have CUDA support.
ENV CUDA_HOME=""
ENV TORCH_CUDA_ARCH_LIST=""
ENV NVIDIA_VISIBLE_DEVICES=""

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Run the Python script (adjust as needed)
CMD ["python", "main.py"]