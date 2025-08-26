# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# --- FIX 1: Install git ---
# The od-parse library is installed from GitHub, so git is required.
RUN apt-get update && apt-get install -y git

# Copy only the requirements file first to leverage Docker's cache
COPY ./requirements.txt /code/requirements.txt

# --- FIX 2: Install Python packages with a long timeout ---
# This helps prevent failures when downloading large files like PyTorch on Render's servers.
RUN pip install --default-timeout=900 --no-cache-dir --upgrade -r /code/requirements.txt

# Now, copy the rest of your application code
COPY ./app /code/app

# Command to run the application when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]