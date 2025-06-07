# Use an official Python runtime
FROM python:3.8-slim-buster

# Install system dependencies
RUN apt update && apt install -y git && apt clean

# Set working directory
WORKDIR /Ultra-Forward-Bot

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the full bot code
COPY . .

# Ensure start.sh is executable
RUN chmod +x /Ultra-Forward-Bot/start.sh

# Run the startup script
CMD ["/bin/bash", "/Ultra-Forward-Bot/start.sh"]
