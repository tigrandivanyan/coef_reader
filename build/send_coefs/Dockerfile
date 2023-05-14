# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# Set the working directory to /app
WORKDIR /app

# Update the package manager and install Python 3.9, pip, and other dependencies
RUN apt-get update && \
    apt-get install -y python3.9 python3-pip python3-dev build-essential

WORKDIR /app
COPY requirements.txt requirements.txt
# Install the pytesseract Python package
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Start the application
CMD ["python3", "-u", "index.py"]
