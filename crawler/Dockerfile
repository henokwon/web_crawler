# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /crawler
WORKDIR /crawler

# Copy the current directory contents into the container at /crawler
COPY . /crawler

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
