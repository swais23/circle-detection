FROM python:3.10-slim

# Install packages
COPY requirements/*.txt /req/
RUN cd /req && pip install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /src