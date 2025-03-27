# Use an official Python 3.11 slim image as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip to the latest version
RUN python -m pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY main.py .

# Cloud Run expects the application to listen on port 8080
EXPOSE 8080

# Run the application with uvicorn on container startup using exec form,
# allowing the port to be configured by the environment variable PORT (defaulting to 8080)
CMD exec uvicorn main:app --host 0.0.0.0 --port=${PORT: 8080}
