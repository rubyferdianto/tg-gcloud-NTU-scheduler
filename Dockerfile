# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose the port that the app runs on
EXPOSE 8080

# Run the Flask app with Gunicorn for production
<<<<<<< HEAD
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "0", "src.app:app"]
=======
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "0", "src.app:app"]
>>>>>>> b5456a5 (updated)
