from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_review_endpoint_positive():
    response = client.post("/review", json={"content": "This product was amazing and perfect!"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "positive"
    assert "readability_score" in data
    assert "suggestions" in data

def test_review_endpoint_negative():
    response = client.post("/review", json={"content": "This was terrible and frustrating."})
    assert response.status_code == 200
    assert response.json()["sentiment"] == "negative"

def test_review_endpoint_neutral():
    response = client.post("/review", json={"content": "It was a product."})
    assert response.status_code == 200
    assert response.json()["sentiment"] == "neutral"

def test_review_endpoint_empty():
    response = client.post("/review", json={"content": ""})
    assert response.status_code == 400
