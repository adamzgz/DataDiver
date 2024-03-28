from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import shutil
import os

# Lanza la api 
app = FastAPI()

#Endpoint para subir un archivo, leerlo con pandas,
#convertirlo a una tabla de Apache Arrow y enviarlo a un servicio destino

@app.post("/upload-dataset/")
async def upload_dataset(file: UploadFile = File(...)):
   
    # Definir la ruta de almacenamiento
    storage_path = "./files"
    file_location = f"{storage_path}/{file.filename}"
    
        # Cambio la logica a guardar el archivo simplemente, sin llegar a leerlo.
        # Dejo comentado el codigo anterior para referencia
        # df = await load_dataset.load_data(file)  # función para cargar datos

    if file.content_type == "text/csv" or file.content_type in ["application/vnd.ms-excel",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"] or file.content_type == "application/json":
        try:
        
            # Guardar archivo en el almacenamiento
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(file.file, file_object)

            # Aqui se debe añadir la logica para notificar al servicio de destino
            
            # Por ahora, solo devolvemos la ruta del archivo
            return {"location": file_location}
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise Exception("Formato de archivo no soportado.")





        



    


