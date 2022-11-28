"""
This file holds the tests for the machine/<dorm>/<floor>/<floor_id> route
"""

#pylint: disable = C0301, E1101, W0105, W0613
# C0301: Line too long (line 68 and line 312)
# E1101: Instance of 'scoped_session' has no 'add' member
# W0613: Unused argument 'init_database' (unused-argument)

import json
import time
from tests import constants
from tests.conftest import get_mock_token


# ------------------------------------GET-----------------------------------------------


def test_successful_get_machine_by_dorm_floor_floor_id(test_client, init_database):
    """
    This method tests a successful
    /machine/<dorm>/<floor>/<floor_id> API call
    Case: Completely proper get API call
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.get(
        f"/machine/{constants.MACHINE_TEST_DORM2}/{constants.MACHINE_TEST_FLOOR2}/{constants.MACHINE_TEST_FLOOR_ID2}",
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "Public_ID": constants.MACHINE_TEST_PUBLIC_ID2,
        "Status": constants.MACHINE_TEST_STATUS2,
        "Finish_Time": constants.MACHINE_TEST_FINISH_TIME2,
        "User_Name": constants.MACHINE_TEST_USER_NAME2,
    }


def test_failed_get_machine_by_dorm_floor_floor_id(test_client, init_database):
    """
    This method tests a failed
    /machine/<dorm>/<floor>/<floor_id> API call
    Case: Machine does not exist
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.get(
        f"/machine/{constants.MACHINE_TEST_DORM2}/{constants.MACHINE_TEST_FLOOR2}/404",
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {
        'error': '404 Not Found: Could not GET machine with Floor_ID: 404'}


# ------------------------------------PUT----------------------------------------


def test_successful_put_machine_by_dorm_floor_floor_id1(test_client, init_database):
    """
    This method tests a successful put
    /machine/<dorm>/<floor>/<floor_id> API call
    Case: Completely proper put API call
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.put(
        f"/machine/{constants.MACHINE_TEST_DORM2}/{constants.MACHINE_TEST_FLOOR2}/{constants.MACHINE_TEST_FLOOR_ID2}",
        query_string={
            "status": "In_use",
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "Public_ID": constants.MACHINE_TEST_PUBLIC_ID2,
        "Status": "In_use",
        "User_Name": "Hayden",
        "Finish_Time": (int(time.time())+1800)//300,
    }


def test_successful_put_machine_by_dorm_floor_floor_id2(test_client, init_database):
    """
    This method tests a successful put
    /machine/<dorm>/<floor>/<floor_id> API call
    Case: Completely proper put API call
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.put(
        f"/machine/{constants.MACHINE_TEST_DORM2}/{constants.MACHINE_TEST_FLOOR2}/{constants.MACHINE_TEST_FLOOR_ID2}",
        query_string={
            "status": "Broken",
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "Public_ID": constants.MACHINE_TEST_PUBLIC_ID2,
        "Status": "Broken",
        "User_Name": None,
        "Finish_Time": None,
    }


def test_failed_put_machine_by_dorm_floor_floor_id(test_client, init_database):
    """
    This method tests a failed put
    /machine/<dorm>/<floor>/<floor_id> API call
    Case: Machine does not exist
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.put(
        f"/machine/{constants.MACHINE_TEST_DORM2}/{constants.MACHINE_TEST_FLOOR2}/404",
        query_string={
            "status": "Broken",
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {
        "error": "404 Not Found: Could not PUT machine with Floor_ID: 404"
    }
