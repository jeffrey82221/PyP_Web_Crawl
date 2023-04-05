# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install
RUN apt-get update &&\
 apt-get install -y git

# Setup Git 
RUN git config pull.rebase false &&\
    git config --global user.name "jeffrey82221" &&\
    git config --global user.email "jeffrey82221@gmail.com"
    
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install -r requirements.txt