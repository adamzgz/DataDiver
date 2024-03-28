# He modificado toda la logica de data_cleaning, ya que ahora se guardan los archivos en un contenedor compartido

# Importamos las librerias

from fastapi import FastAPI, HTTPException, Form
import pandas as pd
import os
import load_dataset as ld
import data_cleaning_functions as dcf

# Inicializo FastAPI
app = FastAPI()


# Endpoint operacion de limpieza

@app.post("/apply_cleaning")

# De momento recibe el nombre del archivo y la operacion a realizar, esto se cambiará para que reciba el id de usuario
# y a partir de ahi se obtenga el archivo

async def apply_cleaning_operation(file_name: str = Form(...), operation: str = Form(...)):

    # Definir la ruta de almacenamiento
    storage_path = "/files"
    file_location = f"{storage_path}/{file_name}"

    # Compruebo si el archivo existe
    if not os.path.exists(file_location):

        # Si no existe, lanzo un error 404
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    # Si existe, cargo el archivo y aplico la operacion de limpieza
    try:
        # Cargo el archivo usando la funcion de load_dataset
        df = ld.load_data(file_location)

        # Aplico la operacion de limpieza
        result = dcf.data_cleaning(df, operation)

        # Devuelvo el resultado
        return result
    
    # Si hay algun error, lo imprimo y lanzo un error 500
    except HTTPException as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))