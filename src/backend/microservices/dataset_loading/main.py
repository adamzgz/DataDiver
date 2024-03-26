from fastapi import FastAPI, File, UploadFile, Form
import pandas as pd
from dotenv import load_dotenv
import pyarrow as pa
import httpx
import load_dataset
import os

# Carga las variables de entorno

# Carga las variables de entorno del archivo .env
load_dotenv()

# Lanza la api 
app = FastAPI()


#Endpoint para subir un archivo, leerlo con pandas,
#convertirlo a una tabla de Apache Arrow y enviarlo a un servicio destino

@app.post("/upload-dataset/")

async def upload_dataset(file: UploadFile = File(...), destination: str = Form(...)):

    # Lee el archivo en un DataFrame de Pandas
    df = await load_dataset.load_data(file)

    # Convierte el DataFrame a una tabla de Apache Arrow
    table = pa.Table.from_pandas(df)

    # Serializa la tabla a un buffer
    buf = pa.ipc.serialize_table(table).to_pybytes()

    # Diccionario de URLs de los servicios destino, se modifican en el archivo .env
    destinations = {
        "data_cleaning": os.getenv("DATA_CLEANING_URL"),
        "EDA_analysis": os.getenv("EDA_ANALYSIS_URL"),
        "data_modeling": os.getenv("DATA_MODELING_URL"),
        "model_prediction": os.getenv("MODEL_PREDICTION_URL")
    }

    # Comprueba que el destino es correcto
    if destination not in destinations:
        return {"error": "Destino desconocido"}

    # Envía el buffer serializado al servicio que hizo la peticion
    response = httpx.post(destinations[destination], content=buf)

    return {"message": f"Dataset enviado a {destination}", "response": response.text}
