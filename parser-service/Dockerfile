# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /code

# Install git, which is needed to install libraries from GitHub
RUN apt-get update && apt-get install -y git

# Copy only the requirements file first. This helps Docker cache
# the installed packages, making future builds much faster.
COPY ./requirements.txt /code/requirements.txt

# Install the Python dependencies with a long timeout
# This prevents errors when downloading large files like PyTorch.
RUN pip install --default-timeout=900 --no-cache-dir --upgrade -r /code/requirements.txt

# Now, copy your application's source code into the container
COPY ./app /code/app

# Tell the container which command to run when it starts.
# This starts the Uvicorn server for your FastAPI application.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]