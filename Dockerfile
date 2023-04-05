# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install
RUN apt-get update &&\
 apt-get install -y git

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install -r requirements.txt