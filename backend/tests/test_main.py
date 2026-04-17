from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_upload_file():
    response = client.post("/upload/", files={"file": ("test.pdf", b"content")})
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully"}

def test_ask_question():
    response = client.post("/ask/", json={"question": "What is your name?"})
    assert response.status_code == 200
    assert "answer" in response.json()
