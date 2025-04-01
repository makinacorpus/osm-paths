ARG BASE_IMAGE=python:3.12-bookworm

FROM ${BASE_IMAGE} AS base

# Create the app directory
RUN mkdir /app

# Set the working directory inside the container
WORKDIR /app

# Set environment variables
ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Upgrade pip
RUN pip install --upgrade pip

# Install the application dependencies
COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project to the container
COPY ../. /app/

# Expose the Django port
EXPOSE 8000

# Run Django’s development server
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
#gunicorn a la place de runserver