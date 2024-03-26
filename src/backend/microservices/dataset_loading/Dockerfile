# Usa una imagen oficial de Python como imagen base
FROM python:3.10.13

# Establece el directorio de trabajo en el contenedor
WORKDIR /code

# Copia los requisitos de dependencias y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de tu aplicación
COPY ./app /code/app

# Comando para ejecutar la aplicación usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]