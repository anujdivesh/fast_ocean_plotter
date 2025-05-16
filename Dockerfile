FROM python:3.9-slim

# Install system dependencies + proj for geospatial
RUN apt-get update && apt-get install -y \
    build-essential \
    libgeos-dev \
    proj-bin \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies with exact versions
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create cache directory with proper permissions
RUN mkdir -p /app/static/plots && chmod 777 /app/static/plots

# Run with multiple workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "4", "main:app"]