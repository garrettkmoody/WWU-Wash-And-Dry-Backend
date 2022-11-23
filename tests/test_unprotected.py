"""
This file holds the tests for the unprotected route
"""

from flask import json

def test_unprotected_route(test_client):
    """
    This method tests a unprotected route and that a response is return succesfully
    Input Arguments: None
    Returns: Void
    """
    response = test_client.get("/unprotected")
    assert response.status_code == 200
    assert json.loads(response.data) == "No Token No problem!"
