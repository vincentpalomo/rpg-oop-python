# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /0.1.0

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code from 0.1.0 directory
COPY 0.1.0/ .

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]