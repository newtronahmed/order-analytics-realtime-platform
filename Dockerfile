# Dockerfile

# Use the official Python 3.12 image as a base
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install the uvicorn package
RUN pip install uvicorn[standard] fastapi

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]