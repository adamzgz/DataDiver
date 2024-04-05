from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import shutil
import os
import logging
from typing import List
from pydantic import BaseModel
import utils.dataset_utils as du
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional



# Inicializa el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lanza la api 
app = FastAPI()

# clase para el modelo de datos
class Dataset(BaseModel):
    data_id: str
    file_name: str


# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origins
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)


#Endpoint para subir un archivo y almacenarlo en el servidor (Falta implementar el LOGGING)

@app.post("/upload-dataset/{user_id}")
async def upload_dataset(
    user_id: str, 
    file: UploadFile = File(...), 
    overwrite: str = Form("false")
):
    overwrite_bool = overwrite.lower() == "true"

    logger.info(f"Valor de overwrite recibido: {overwrite}")

    logger.info(f"Subiendo archivo {file.filename} para el usuario {user_id}")
    # Ruta donde se almacenarán los archivos
    storage_path = f"/files/{user_id}"


    # Crear la carpeta si no existe
    logger.info(f"Creando carpeta de almacenamiento en {storage_path}")
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)

    # Ruta al archivo final
    file_location = f"{storage_path}/{file.filename}"

    # Verificar si el archivo ya existe

    logger.info(f"Verificando si el archivo ya existe")
    logger.info(f"El archivo es {file.filename}")

    existing_file = du.check_file_exists(user_id, file.filename)

    logger.info(f"El archivo ya existe: {existing_file}")
    logger.info(f"La opcion de sobreescribir es: {overwrite_bool}")
    # Si el archivo ya existe y no se ha confirmado la sobrescritura, devuelve un mensaje para confirmar
    if existing_file and not overwrite_bool:
        
        logger.info("El archivo ya existe. Se requiere confirmación para sobreescribir")
        raise HTTPException(status_code=351, detail="El archivo ya existe. ¿Desea sobreescribir?")


    # Si el archivo es un CSV, Excel o JSON, lo guardamos en el servidor
    logger.info(f"Verificando el formato del archivo")
    if file.content_type in ["text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/json"]:
        try:
            # Guardar el archivo en el servidor
            logger.info(f"Guardando el archivo en {file_location}")
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(file.file, file_object)
            logger.info("Archivo guardado correctamente")

            # Si estamos sobreescribiendo, actualizamos la entrada existente en lugar de crear una nueva
            logger.info("Comprobando si se está sobreescribiendo")
            if existing_file:
                logger.info("Actualizando la entrada existente en la base de datos")
                data_id = du.update_file_mapping(user_id, file.filename, file_location)

            # Si no estamos sobreescribiendo, creamos una nueva entrada
            else:
                logger.info("Creando una nueva entrada en la base de datos")
                data_id = du.generate_data_id()
                du.insert_file_mapping(user_id, data_id, file_location)

            message = "Archivo subido correctamente"

            # Devolver el ID del archivo y un mensaje de confirmación
            return {"data_id": data_id, "message": message}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {e}")
    else:
        # Devuelve un error mostrando el formato del archivo, es decir, su extension
        raise HTTPException(status_code=400, detail=f"Formato de archivo no soportado. el archivo es {file.content_type}")

    

@app.get("/list_datasets/{user_id}", response_model=List[Dataset])
async def list_datasets_for_user(user_id: str):

    # Obtener la lista de datasets del usuario
    logger.info(f"Obteniendo datasets para el usuario {user_id}")
    try:
        datasets = du.get_files_list(user_id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al lanzar la funcion de obtener los datasets: {e}")
    

    # Si no hay datasets, devolver un error 404
    if not datasets:
        raise HTTPException(status_code=404, detail="No se han encontrado datasets almacenados")
    
    # Si hay datasets, devolver una lista con los IDs y nombres de los archivos
    return [{"data_id": data_id, "file_name": file_path.split("/")[-1]} for data_id, file_path in datasets]







    


