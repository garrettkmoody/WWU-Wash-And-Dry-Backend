"""
This file holds the tests for the SSO login route
"""

from tests.conftest import get_mock_token

def test_login_error(test_client):
    """
    This function tests the /login/callback route with an error query
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.get(
        "/login/callback", query_string={
        "error": "error"},
        headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 403
    assert response.data == b"error"

def test_sign_in_failed(test_client):
    """
    This function tests a sign-in failed response
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.get(
        "/login/callback", query_string={
        "user": "Taylor"},
        headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 403
    assert response.data == b"Sign-in failed, no auth code."

def test_failed_authentication(test_client):
    """
    This function tests authentication
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.get(
        "/login/callback", query_string={
        "code": "failed_authentication"},
        headers={"access_token": get_mock_token()}
    )
    # assert the status code is a redirect status code
    assert response.status_code == 302
    