# Start with your base image
FROM python:3.9-slim

# Install system dependencies including gcc, g++, build-essential, and pkg-config
RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    build-essential \
    pkg-config \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up a working directory
WORKDIR /app

# Copy your requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Define the command to run your application
CMD ["python", "app.py"]
