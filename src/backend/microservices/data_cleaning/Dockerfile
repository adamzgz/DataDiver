# 1. Usa una imagen oficial de Python como imagen base
FROM python:3.10.13

# 2. Establece el directorio de trabajo en el contenedor
WORKDIR /app

# 4. Copia el resto del código de la aplicación
COPY . .
RUN pip install --no-cache-dir -r requirements.txt



# 5. Comando para ejecutar la aplicación usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]