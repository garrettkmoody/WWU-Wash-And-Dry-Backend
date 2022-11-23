"""
This file holds the tests for user routes
"""

#pylint: disable = E1101, W0613
#E1101: Instance of 'scoped_session' has no 'add' member
#W0613: Unused argument 'init_database' (unused-argument)

import json
from tests import constants
from tests.conftest import get_mock_token


def test_successful_get_user(test_client, init_database):
    """
    This method tests a succesful /getUser/{USER_TEST_PUBLIC_ID} API call
    Input Arguments: test_client, init_database
    Returns: Void
    """
    response = test_client.get(
        f"/user/{constants.USER_TEST_PUBLIC_ID1}", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 200
    assert json.loads(response.data) == (
        {
            "Name": constants.USER_TEST_NAME1,
            "Public_ID": constants.USER_TEST_PUBLIC_ID1,
            "Email": constants.USER_TEST_EMAIL1,
            "Dorm": None,
            "Floor": None
        }
    )

def test_failed_get_user(test_client, init_database):
    """
    This method tests a failed /getUser/{USER_TEST_PUBLIC_ID} API call
    Case: User does not exist
    Input Arguments: test_client, init_database
    Returns: Void
    """
    response = test_client.get(
        f"/user/{1000000}", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 404
    assert json.loads(response.data) == \
        {'error': '404 Not Found: Could not GET user with ID: 1000000'}

# ---------------------------UPDATE USER BY ID--------------------------------------


def test_update_user(test_client, init_database):
    """
    This method tests a successful /putUser/{USER_TEST_PUBLIC_ID} API call
    Input Arguments: test_client, init_database
    Returns: Void
    """
    response = test_client.put(f"/user/{constants.USER_TEST_PUBLIC_ID1}", query_string={
        "Floor": constants.USER_TEST_FLOOR1, "Dorm": constants.USER_TEST_DORM1},
        headers={"access_token": get_mock_token()})
    assert response.status_code == 200
    assert json.loads(response.data) == (
        {
            "Name": constants.USER_TEST_NAME1,
            "Public_ID": constants.USER_TEST_PUBLIC_ID1,
            "Email": constants.USER_TEST_EMAIL1,
            "Dorm": constants.USER_TEST_DORM1,
            "Floor": constants.USER_TEST_FLOOR1,
        }
    )

def test_failed_update_user1(test_client, init_database):
    """
    This method tests a failed /putUser/{USER_TEST_PUBLIC_ID} API call
    Case: Updated floor is out of range of possible floors
    Input Arguments: test_client, init_database
    Returns Void
    """
    response = test_client.put(f"/user/{constants.USER_TEST_PUBLIC_ID1}", query_string={
        "Floor": "1000", "Dorm": constants.USER_TEST_DORM1},
        headers={"access_token": get_mock_token()})
    assert response.status_code == 400
    assert json.loads(response.data) == \
        {'error': '400 Bad Request: Floor is out of range of the acceptable levels'}

def test_failed_update_user2(test_client, init_database):
    """
    This method tests a failed /putUser/{USER_TEST_PUBLIC_ID} API call
    Case: Updated dorm is not a possible dorm option
    Input Arguments: test_client, init_database
    Returns Void
    """
    response = test_client.put(f"/user/{constants.USER_TEST_PUBLIC_ID1}", query_string={
        "Floor": constants.USER_TEST_FLOOR1, "Dorm": "Bowers"},
        headers={"access_token": get_mock_token()})
    assert response.status_code == 400
    assert json.loads(response.data) == \
        {'error': '400 Bad Request: Dorm is not recognized as a valid dorm'}

def test_failed_update_user3(test_client, init_database):
    """
    This method tests a failed /putUser/{USER_TEST_PUBLIC_ID} API call
    Case: User does not exist
    Input Arguments: test_client, init_database
    Returns Void
    """
    response = test_client.put(f"/user/{100000}", query_string={
        "Floor": constants.USER_TEST_FLOOR1, "Dorm": constants.USER_TEST_DORM1},
        headers={"access_token": get_mock_token()})
    assert response.status_code == 404
    assert json.loads(response.data) == \
        {'error': '404 Not Found: Could not PUT user with ID: 100000'}


# ---------------------------DELETE USER BY ID--------------------------------------


def test_delete_user(test_client, init_database):
    """
    This method tests a succesful /deleteUser/{USER_TEST_PUBLIC_ID} API call
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.delete(
        f"/user/{constants.USER_TEST_PUBLIC_ID1}", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 200
    assert (
        json.loads(response.data)
        == f"deleted information for user with ID: {constants.USER_TEST_PUBLIC_ID1}"
    )

def test_failed_delete_user(test_client, init_database):
    """
    This method tests a failed /deleteUser/{USER_TEST_PUBLIC_ID} API call
    Case: User does not exist
    Input Arguments: test_client, init_database
    Returns: Void
    """
    response = test_client.delete(
        f"/user/{1000000}", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 404
    assert json.loads(response.data) == \
        {'error': '404 Not Found: User not deleted, user with ID: 1000000, does not exist'}
