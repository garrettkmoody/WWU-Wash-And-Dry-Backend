"""
This file holds the tests for the unprotected route
"""

from flask import json
import pytest
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


def test_unprotected_route():
    """
    This method tests a unprotected route and that a response is return succesfully
    Input Arguments: None
    Returns: Void
    """
    response = app.test_client().get("/unprotected")
    assert response.status_code == 200
    assert json.loads(response.data) == "No Token No problem!"
