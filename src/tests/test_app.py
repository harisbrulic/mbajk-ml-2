import pytest
from src.serve.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_predict_endpoint_missing_data_key(client):
    response = client.post('/mbajk/predict/', json={})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data is not None
    assert json_data["error"] == "Missing 'data' key in JSON"

def test_predict_endpoint_invalid_data_length(client):
    response = client.post('/mbajk/predict/', json={"data": [1] * 99})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data is not None
    assert json_data["error"] == "Data must contain exactly 100 values"

def test_predict_endpoint_non_numeric_data(client):
    response = client.post('/mbajk/predict/', json={"data": [1.0] * 99 + ["a"]})
    assert response.status_code == 400
    assert response.get_json()["error"] == "All values in data must be numbers"

