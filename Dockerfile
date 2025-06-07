# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Update apt, upgrade packages, and install git
# Combine RUN commands for better caching and smaller image layers
RUN apt update && apt upgrade -y && apt install git -y

# Set the working directory inside the container.
# This is where your application code (from Git) will be copied by Coolify,
# and where your requirements.txt and start.sh should be.
WORKDIR /app

# Copy requirements.txt into the WORKDIR (/app)
# This allows Docker to cache the layer if requirements.txt doesn't change
COPY requirements.txt .

# Install Python dependencies
# Using --no-cache-dir to avoid storing pip cache in the image
RUN pip3 install --no-cache-dir -U pip && pip3 install --no-cache-dir -U -r requirements.txt

# Coolify will automatically copy the rest of your repository's files into /app
# after the Dockerfile is built. So you don't need `COPY . .` here typically.
# However, if start.sh is specifically needed during the build phase (e.g., if it's
# a setup script), you might add:
# COPY start.sh .
# RUN chmod +x start.sh

# But for a simple bot, usually the `CMD` is enough, and Coolify handles the copying.
# If start.sh is not copied by Coolify automatically or it's not made executable,
# you might need to ensure it has execute permissions.
# Often, it's safer to ensure it's executable:
# RUN chmod +x start.sh  # This assumes start.sh is copied by Coolify before CMD runs.

# Define the command to run your application when the container starts
# This will execute your start.sh script located at /app/start.sh
# Ensure your start.sh script is in the root of your Git repository.
CMD ["/bin/bash", "/app/start.sh"]
