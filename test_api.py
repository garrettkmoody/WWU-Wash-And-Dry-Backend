from app import app
import pytest

def test_unprotected_route():
    response = app.test_client().get('/unprotected')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'No Token No problem!'

def test_getUser_route():
    user_ID=2
    response=app.test_client().get(f'/user/{user_ID}')
    assert response.status_code==200
    assert response.data.decode('utf-8')==f'got information for user with ID: {user_ID}'


def test_deleteUser_route():
    user_ID=2
    response=app.test_client().delete(f'/user/{user_ID}')
    assert response.status_code==200
    assert response.data.decode('utf-8')==f'deleted information for user with ID: {user_ID}'