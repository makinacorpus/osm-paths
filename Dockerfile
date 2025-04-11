ARG BASE_IMAGE=python:3.12-bookworm

FROM ${BASE_IMAGE} AS base

# Set environment variables
ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV CACHE_DIR=/tmp/cache

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create the app directory
RUN mkdir /app

# Set the working directory inside the container
WORKDIR /app

# Install the application dependencies
COPY requirements.txt  /app/
COPY pyproject.toml  /app/
RUN uv pip install --system --no-cache-dir -r requirements.txt -U

# Copy the Django project to the container
RUN --mount=type=bind,src=./osm_paths,dst=/app/osm_paths uv pip install --system --no-cache-dir .

# Expose the Django port
EXPOSE 8000

# Run Django’s development server
CMD ["gunicorn", "osm_paths.wsgi:application", "--bind=0.0.0.0:8000"]