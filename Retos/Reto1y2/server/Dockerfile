# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Environment variables
ARG ENV_SERVER

CMD ["python", "server.py", "ENV_SERVER"]