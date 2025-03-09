FROM python:3.10-slim

# Install packages
COPY requirements/*.txt /req/
RUN pip install --no-cache-dir -r /req/requirements.txt && rm -rf /req

# Set working directory
WORKDIR /app