# Base image
FROM python:3.12-slim

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev

# Set working directory
WORKDIR /apps

# Copy requirements and install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /apps

# Expose the FastAPI port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["python","-m","uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8000"]
