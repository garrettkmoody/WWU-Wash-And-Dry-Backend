"""
This file holds the tests for the custom errorhandlers
"""

#pylint: disable = W0613
#W0613: Unused argument 'app_context' (unused-argument)

import pytest
from flask import json
from tests.testapp import app

# This pytest fixture allows us to update database within our test file.
@pytest.fixture(name="app_context")
def fixture_app_context():
    """
    This method allows us to edit app content.
    Input Arguments: None
    Return: Void
    """
    with app.app_context():
        yield

# ---------------------------ERROR HANDLER TESTS --------------------------------------

def test_400_error(app_context):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = app.test_client().get("/test400")
    assert response.status_code == 400
    assert (json.loads(response.data) == {
            'error': '400 Bad Request: Bad Request'})


def test_401_error(app_context):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = app.test_client().get("/test401")
    assert response.status_code == 401
    assert (json.loads(response.data) == {
            'error': '401 Unauthorized: Unauthorized User'})


def test_403_error(app_context):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = app.test_client().get("/test403")
    assert response.status_code == 403
    assert (json.loads(response.data) == {
            'error': '403 Forbidden: Forbidden API Call'})


def test_404_error(app_context):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = app.test_client().get("/test404")
    assert response.status_code == 404
    assert json.loads(response.data) == {
            'error': '404 Not Found: Page Not Found'}


def test_429_error(app_context):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = app.test_client().get("/test429")
    assert response.status_code == 429
    assert (json.loads(response.data) == {
            'error': '429 Too Many Requests: Too Many Requests'})


def test_500_error(app_context):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = app.test_client().get("/test500")
    assert response.status_code == 500
    assert (json.loads(response.data) == {
            'error': '500 Internal Server Error: Internal Server Error'})


def test_502_error(app_context):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = app.test_client().get("/test502")
    assert response.status_code == 502
    assert (json.loads(response.data) == {
            'error': '502 Bad Gateway: Bad Gateway'})


def test_503_error(app_context):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = app.test_client().get("/test503")
    assert response.status_code == 503
    assert (json.loads(response.data) == {
            'error': '503 Service Unavailable: Service Unavailable'})


def test_504_error(app_context):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = app.test_client().get("/test504")
    assert response.status_code == 504
    assert (json.loads(response.data) == {
            'error': '504 Gateway Timeout: Gateway Timed Out'})
