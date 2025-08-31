FROM python:3.12

# Configure python
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

# Update utilities and install clients
RUN apt-get update && \
    apt-get install -y redis-tools postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app

# Copy application code
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
