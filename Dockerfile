# Stage 1: Build
FROM python:3.8-slim AS builder

# Accept build arguments from docker-compose
ARG DJANGO_SECRET_KEY
ARG DATABASE_URL

# Set environment variables from build args
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
ENV DATABASE_URL=${DATABASE_URL}

# Prevents Python from writing pyc files & output buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Stage 2: Runtime
FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.8 /usr/local/lib/python3.8
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app source
COPY --from=builder /app /app

# Ensure entrypoint has execute permissions
RUN chmod +x /app/docker-entrypoint-app.sh && \
    ls -la /app/docker-entrypoint-app.sh

# Expose the port Fly.io will use
EXPOSE 8000

# Start the app
ENTRYPOINT ["/bin/bash", "-c", "bash /app/docker-entrypoint-app.sh"]
