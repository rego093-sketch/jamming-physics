# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1         PYTHONUNBUFFERED=1

WORKDIR /app

# (Optional) native build tools; wheels should cover NumPy/SciPy, but keep this for safety.
RUN apt-get update && apt-get install -y --no-install-recommends         build-essential         && rm -rf /var/lib/apt/lists/*

# Install Python deps from the archive
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the whole archive contents into the image
COPY . /app

# Make sure our script is executable
RUN chmod +x scripts/run_all.sh

# PYTHONPATH so scripts can import code/dns2d.py as 'dns2d'
ENV PYTHONPATH=/app/code

# One-click end-to-end demo + assertions
CMD ["bash", "scripts/run_all.sh"]
