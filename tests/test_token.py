"""
This file holds the tests for the unprotected route
"""

#pylint: disable = W0105
#W0105: String statement has no effect (pointless-string-statement)

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

# TO-DO: Implement this test
'''
def test_protected_route(test_client):
    """
    This method tests a unprotected route and that a response is return succesfully
    Input Arguments: None
    Returns: Void
    """
    response = test_client.get("/protected", headers={"access_token": get_mock_token()})
    assert response.status_code == 200
    assert json.loads(response.data) == "Hello Hayden"
'''
