# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Update apt, upgrade packages, and install git
RUN apt update && apt upgrade -y && apt install git -y

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and start.sh from your repository root
# into the /app directory inside the Docker image.
COPY requirements.txt .
COPY start.sh .

# Install Python dependencies
# Using --no-cache-dir to avoid storing pip cache in the image
RUN pip3 install --no-cache-dir -U pip && pip3 install --no-cache-dir -U -r requirements.txt

# Make the start.sh script executable
RUN chmod +x start.sh

# Define the command to run your application when the container starts
# This will execute your start.sh script located at /app/start.sh
CMD ["/bin/bash", "/app/start.sh"]
