FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies required for some python packages and PostgreSQL if needed in future
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI server directly, Base.metadata.create_all will generate schema
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
