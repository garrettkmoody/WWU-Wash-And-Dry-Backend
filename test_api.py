from app import app
import pytest

def test_unprotected_route():
    response = app.test_client().get('/unprotected')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'No Token No problem!'
