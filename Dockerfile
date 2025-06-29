# Base image with Python
FROM python:3.11-slim

# Create working directory
WORKDIR /app

# Install dependencies
COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src/ .

ENV PORT=8080
EXPOSE $PORT

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "main:app"]

