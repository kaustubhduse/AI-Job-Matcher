# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# --- MODIFIED LINE ---
# Install git and the correct graphics library for OpenCV
RUN apt-get update && apt-get install -y git libgl1

# Copy only the requirements file first to leverage Docker's cache
COPY ./requirements.txt /code/requirements.txt

# Install the Python dependencies with a long timeout
RUN pip install --default-timeout=1200 --no-cache-dir --upgrade -r /code/requirements.txt

# Now, copy your application's source code into the container
COPY ./app /code/app

# Tell the container which command to run when it starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]