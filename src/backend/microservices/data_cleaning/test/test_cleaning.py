from fastapi.testclient import TestClient
from DataDiver.src.backend.microservices.data_cleaning.app.main import app # Importamos la aplicación FastAPI

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}