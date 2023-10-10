# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app/.

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

