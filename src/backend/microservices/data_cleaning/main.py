from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import pyarrow as pa
import pandas as pd
from typing import Optional
from data_cleaning_functions import data_cleaning

# Guardado del dataframe
# Pendiente de modificar a opciones mas robustas como una base de datos
dataframes = {}

# Autenticacion, pendiente de cambiar la logica
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Inicializacion de la API
app = FastAPI()


# Logica para recibir el Dataframe
@app.post("/receive-dataset/{user_id}")
async def receive_dataset(request: Request, user_id: str = Depends(oauth2_scheme)):
    buf = await request.body()
    table = pa.ipc.deserialize_table(buf)
    df = table.to_pandas()

    # Guardamos el DataFrame usando el user_id como clave
    dataframes[user_id] = df

    return {"mensaje": "DataFrame recibido y almacenado."}

@app.post("/clean-dataset/{user_id}")
async def clean_dataset(options: dict, user_id: str = Depends(oauth2_scheme)):
    if user_id not in dataframes:
        raise HTTPException(status_code=404, detail="DataFrame no encontrado, carga un dataframe antes")
    
    df = dataframes[user_id]

    # Aplica la función de limpieza según las opciones recibidas
    # Las opciones estan configuradas en data_cleaning_functions.py
    
    result = data_cleaning(df, options)

    # Actualiza el DataFrame limpio en la "base de datos"
    dataframes[user_id] = df

    # Pendiente de modificar el return segun sea necesario
    return {"mensaje": f"Proceso de {options} completado", "resultado": result}