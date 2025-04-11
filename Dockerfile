ARG BASE_IMAGE=python:3.12-bookworm

FROM ${BASE_IMAGE} AS base

# Set environment variables
ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV CACHE_DIR=/tmp/cache
ENV DJANGO_SETTINGS_MODULE=osm_paths.settings

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create the app directory
RUN mkdir /app

# Set the working directory inside the container
WORKDIR /app

# Install the application dependencies
RUN --mount=type=bind,src=./requirements.txt,dst=/app/requirements.txt uv pip install --system --no-cache-dir -r requirements.txt -U
RUN --mount=type=bind,src=./osm_paths,dst=/app/osm_paths --mount=type=bind,src=./pyproject.toml,dst=/app/pyproject.toml uv pip install --system --no-cache-dir .

# Expose the Django port
EXPOSE 8000

# Run Django’s development server
CMD ["gunicorn", "osm_paths.wsgi:application", "--bind=0.0.0.0:8000"]