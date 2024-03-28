# 1. Usa una imagen oficial de Python como imagen base
FROM python:3.10.13

# 2. Establece el directorio de trabajo en el contenedor
WORKDIR /app

# 3. Copia los requisitos de dependencias y los instala
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia el resto del código de la aplicación
COPY . .

# 5. Comando para ejecutar la aplicación usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]