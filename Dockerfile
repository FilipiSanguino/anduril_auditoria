# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the application will listen on
ENV PORT 8080
EXPOSE $PORT

# Run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "main:app"]
