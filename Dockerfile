FROM python:3.12-slim-bookworm
# Use an official Python base image


# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh
# Install uv
RUN pip install uv 
# Install dependencies using uv
RUN uv pip install fastapi uvicorn requests
RUN uv pip install -r requirements.txt


# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app
COPY main2.py /app
COPY requirements.txt .

RUN mkdir -p /data
# Copy files to the container
COPY . .
EXPOSE 8000
CMD ["uv", "run", "main2.py"]