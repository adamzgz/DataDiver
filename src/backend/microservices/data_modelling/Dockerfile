# 1. Usa una imagen oficial de Python como imagen base
FROM python:3.10

# 2. Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Copy the contents of the local app directory to /app inside the container
COPY app/ .

# Expose port 8003 for the application
EXPOSE 8003

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]