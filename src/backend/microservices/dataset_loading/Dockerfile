# Use the official Python base image
FROM python:3.10

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the local app directory to /app inside the container
COPY app/ .

# Expose port 8000 for the application
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]