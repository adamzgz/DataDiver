from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
import shutil
import os

# Lanza la api 
app = FastAPI()

# Configuración simple de seguridad basada en token, solo para desarrollo

API_KEY = "tokencitotokencito"
API_KEY_NAME = "api_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Función para verificar el token de acceso
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return True
    else:
        raise HTTPException(status_code=403, detail="Token de acceso inválido")
    


#Endpoint para subir un archivo y almacenarlo en el servidor

@app.post("/upload-dataset/")
async def upload_dataset(file: UploadFile = File(...)):
   
    # Definir la ruta de almacenamiento
    storage_path = "./files"
    file_location = f"{storage_path}/{file.filename}"
    
    # Verificar que el archivo sea un CSV o un Excel o un JSON
    if file.content_type in ["text/csv",
                            "application/vnd.ms-excel",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            "application/json"]:
        try:
        
            # Guardar archivo en el almacenamiento
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(file.file, file_object)


           # Lugar para la lógica de notificación al servicio de destino
            
            # Por ahora, solo devolvemos la ruta del archivo
            return {"location": file_location}
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Formato de archivo no soportado.")






        



    


