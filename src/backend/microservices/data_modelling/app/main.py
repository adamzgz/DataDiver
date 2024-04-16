from fastapi import FastAPI, HTTPException
import logging
from typing import List
import utils.dataset_utils as du
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict
from pydantic import BaseModel
import utils.load_dataset as ld
import utils.data_modelling_functions as dmf


# Inicializa el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lanza la api 
app = FastAPI()


class TrainRequest(BaseModel):
    user_id: int
    data_id: int
    model_type: str
    hyperparameters: Dict[str, any]
    target_variable: str
    features: List[str]
    test_size: float
    random_state: Optional[int] = None


@app.post("/train/")
async def train_model(request: TrainRequest):
    target_variable = request.target_variable
    features = request.features
    test_size = request.test_size
    random_state = request.random_state



    logger.info(f"Recibida petición para entrenar un modelo de tipo {request.model_type} con ID de usuario {request.user_id}")
    logger.info(f"Obteniendo dataset con ID: {request.data_id}")


    # Implementar lógica de autenticación y autorización
    # Recuperar la ruta al dataset
    try:
        logger.info(f"Buscando dataset en la base de datos con ID: {request.file_name}")
        file_location = du.get_file_path(request.file_name)
        logger.info(f"Dataset encontrado en la base de datos, ubicación: {file_location}")
        data_id = request.file_name
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    # Cargar y preprocesar el dataset

    # Paso 2: Carga el dataset
    try:
        logger.info(f"Cargando dataset con ID: {request.file_name}")
        df = await ld.load_data(file_location)
        logger.info(f"Dataset cargado con éxito, lanzando funciones de entrenamiento de modelos...")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Entrenar el modelo
    try:
        file_path, message = dmf.model_training(df, request.model_type, request.hyperparameters, file_location, target_variable, features, test_size, random_state)
        # La lógica de manejo de errores y respuesta se mantiene...
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Devolver una respuesta al cliente
    return {"message": "Modelo entrenado con éxito", "file_path": file_path, "accuracy_message": message}