# Use an official Python base image
FROM python:3.12-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer for `uv`
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Install `uv` (already included in the installer, but keeping this just in case)
RUN pip install uv 

# Copy the requirements file first (optimizing build caching)
COPY requirements.txt /app/requirements.txt

# Install dependencies using `uv` inside the system environment
RUN uv pip install --system -r /app/requirements.txt

# Copy only necessary files into the container
COPY main2.py /app/main2.py
COPY . /app

# Create a directory for data
RUN mkdir -p /data

# Expose port 8000
EXPOSE 8000

# Command to start the app
CMD ["uv", "run", "main2.py"]





