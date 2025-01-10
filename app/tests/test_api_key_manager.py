from fastapi.testclient import TestClient
import pytest
import logging

from app.main import app

client = TestClient(app)

data_test = {
    'api_key_reference_id': '676e0123a06008d4833c1c2e'
}


def test_create_api_key_reference():
    response = client.post(
        '/api/v1/api-key-manager',
        json={
                "name": "url-shortener",
                "description": "A simple API to shorten URLs. The service accepts URLs and generates a shorter link.",
                "created_at": "2024-12-21T12:00:00Z",
                "updated_at": "2024-12-21T12:00:00Z"
            }
        )
    
    assert response.status_code == 201, f"The status code is wrong, the expected is '201', the response is '{response.status_code}'"
    assert response.json()['ok'] == True
    assert response.json()['message'] == 'API reference created successfully.'

def test_update_api_key_reference():
    response = client.patch(
        f'/api/v1/api-key-manager/{data_test.get("api_key_reference_id")}',
        json={
            "name": "url-shortener-test-passed",
            "description": "A simple descripcion TEST PASSED"
        }
    )

    assert response.status_code == 200, f"The status code is wrong, the expected is '200', the response is '{response.status_code}'"
    assert response.json() == {'ok': True, 'message': 'API reference updated successfully.'}

def test_update_api_key_reference_not_found():
    response = client.patch(
        f'/api/v1/api-key-manager/376aed53bc00226a2435371b',
        json={
            "name": "url-shortener-test-passed",
            "description": "A simple descripcion TEST PASSED"
        }
    )

    assert response.status_code == 404
    assert response.json() == {'ok': False, 'message': 'API reference not found.'}


def test_delete_api_key_reference_not_found():
    response = client.delete(
        f'/api/v1/api-key-manager/376aed53bc00226a2435371b',
    )

    assert response.status_code == 404
    assert response.json() == {'ok': False, 'message': 'API reference not found.'}

def test_generate_api_key():
    response = client.patch(
        f'/api/v1/api-key-manager/generate-key/{data_test.get("api_key_reference_id")}',
        json={"expiration_date": "2024-12-21"}
    )

    assert response.status_code == 200
    assert response.json()['ok'] == True
    assert response.json()['message'] == 'API key generated succesfully in api reference.'

def test_delete_api_key_not_found():
    response = client.delete(
    f'/api/v1/api-key-manager/{data_test.get("api_key_reference_id")}/delete-key/17bs1f18-7432-4d73-af00-115w9ae317cc',
    )

    assert response.status_code == 404
    assert response.json() == {'ok': False, 'message': 'API key not found in api reference.'}

def test_delete_api_key_reference_id_not_found():
    response = client.delete(
        f'/api/v1/api-key-manager/376aed53bc00226a2435371b/delete-key/17bs1f18-7432-4d73-af00-115w9ae317cc',
    )

    assert response.status_code == 404
    assert response.json() == {'ok': False, 'message': 'API reference not found.'}

def test_verify_key_of_api_reference():
    response = client.post(
        '/api/v1/api-key-manager/verify-key',
        json={
            "api_reference_id": "676e0274bfacb02b8c4e3545",
            "api_key_id": "cebb17b8-532b-4c88-8c66-bd072cb20a8c",
            "api_key": "key_GkNEykN12pmaYP9GWH7jD8mb4e3yXOEr7fJbp5QcikU"
        }

        )
    
    assert response.status_code == 200, f"The status code is wrong, the expected is '200', the response is '{response.status_code}'"
    assert response.json()['ok'] == True
    assert response.json()['message'] == 'API Key is correct and verified.'
