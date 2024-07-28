# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code


ENV PYTHONDOWNWRITEBYTECODE 1
ENV PYTHONNUNBUFFER 1

# update and  install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /price_alert/requirements.txt
RUN pip install -r /price_alert/requirements.txt

# copy project
COPY . .

# Expose the port server is running on
EXPOSE 8000
