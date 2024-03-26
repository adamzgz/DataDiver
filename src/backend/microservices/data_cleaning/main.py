from fastapi import FastAPI, Request
import pyarrow as pa
import pandas as pd

app = FastAPI()

@app.post("/receive-dataset/")
async def receive_dataset(request: Request):
    buf = await request.body()
    table = pa.ipc.deserialize_table(buf)
    df = table.to_pandas()

    # Devuelve mensaje de confirmación, falta añadir la logica para procesar el dataframe
    return {"mensaje": "DataFrame recibido y procesado."}
