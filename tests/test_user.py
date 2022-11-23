"""
This file holds the tests for user routes
"""

#pylint: disable = E1101, W0613
#E1101: Instance of 'scoped_session' has no 'add' member
#W0613: Unused argument 'init_database' (unused-argument)

import json
from tests import constants
from tests.conftest import get_mock_token


def test_get_user(test_client, init_database):
    """
    This method tests a succesful /getUser/{USER_TEST_PUBLIC_ID} API call
    Input Arguments: test_client
    Returns: Void
    """
    # send request
    response = test_client.get(
        f"/user/{constants.USER_TEST_PUBLIC_ID1}", headers={"access_token": get_mock_token()}
    )
    # test response
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


# ---------------------------UPDATE USER BY ID--------------------------------------


def test_update_user(test_client, init_database):
    """
    This method tests a successful /putUser/{USER_TEST_PUBLIC_ID} API call
    Input Arguments: test_client
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
