ARG BASE_IMAGE=python:3.12-bookworm

FROM ${BASE_IMAGE} AS base

# Set environment variables
ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create the app directory
RUN mkdir /app

# Set the working directory inside the container
WORKDIR /app

# Create a volume for Django command input and output
VOLUME /app/var

# Upgrade pip
RUN pip install --upgrade pip

# Install the application dependencies
COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project to the container
COPY . /app/

# Expose the Django port
EXPOSE 8000

# Run Django’s development server
CMD ["gunicorn", "osm-paths.wsgi:application", "--bind=0.0.0.0:8000"]