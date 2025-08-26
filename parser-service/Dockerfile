# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# --- NEW STEP: Install git ---
# First, update the package lists, then install git.
# The '-y' flag automatically confirms the installation.
RUN apt-get update && apt-get install -y git

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --default-timeout=900 --no-cache-dir --upgrade -r /code/requirements.txt
# Copy the application code into the container
COPY ./app /code/app

# Command to run the application
# Uvicorn is an ASGI server, for running FastAPI applications
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]