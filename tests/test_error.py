"""
This file holds the tests for the custom errorhandlers
"""

from flask import json

def test_400_error(test_client):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = test_client.get("/test/400")
    assert response.status_code == 400
    assert (json.loads(response.data) == {
            'error': '400 Bad Request: ERROR MESSAGE'})


def test_401_error(test_client):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = test_client.get("/test/401")
    assert response.status_code == 401
    assert (json.loads(response.data) == {
            'error': '401 Unauthorized: ERROR MESSAGE'})


def test_403_error(test_client):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = test_client.get("/test/403")
    assert response.status_code == 403
    assert (json.loads(response.data) == {
            'error': '403 Forbidden: ERROR MESSAGE'})


def test_404_error(test_client):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = test_client.get("/test/404")
    assert response.status_code == 404
    assert json.loads(response.data) == {
            'error': '404 Not Found: ERROR MESSAGE'}


def test_429_error(test_client):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = test_client.get("/test/429")
    assert response.status_code == 429
    assert (json.loads(response.data) == {
            'error': '429 Too Many Requests: ERROR MESSAGE'})


def test_500_error(test_client):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = test_client.get("/test/500")
    assert response.status_code == 500
    assert (json.loads(response.data) == {
            'error': '500 Internal Server Error: ERROR MESSAGE'})


def test_502_error(test_client):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = test_client.get("/test/502")
    assert response.status_code == 502
    assert (json.loads(response.data) == {
            'error': '502 Bad Gateway: ERROR MESSAGE'})


def test_503_error(test_client):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = test_client.get("/test/503")
    assert response.status_code == 503
    assert (json.loads(response.data) == {
            'error': '503 Service Unavailable: ERROR MESSAGE'})


def test_504_error(test_client):
    """
    This function is to test the bad request error
    Inputs: None
    Returns: Void
    """
    response = test_client.get("/test/504")
    assert response.status_code == 504
    assert (json.loads(response.data) == {
            'error': '504 Gateway Timeout: ERROR MESSAGE'})
