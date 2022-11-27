"""
This file holds the tests for the machine/<public_id> route
"""

#pylint: disable = C0301, W0613
#C0301: Line too long (113/100) (line-too-long)
#W0613: Unused argument 'init_database' (unused-argument)

import json
import time
from tests import constants
from tests.conftest import get_mock_token


# ---------------------------POST--------------------------------------


def test_successful_create_machine_by_id_1(test_client, init_database):
    """
    This method tests a successful post /machine/<public_id> API call
    Case: Completely proper create machine call
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.post(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID1}",
        query_string={
            "Floor_id": constants.MACHINE_TEST_FLOOR_ID1,
            "Dorm": constants.MACHINE_TEST_DORM1,
            "Floor": constants.MACHINE_TEST_FLOOR1,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE1,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 200
    assert (
        json.loads(response.data)
        == f"Created information for machine with ID: {constants.MACHINE_TEST_PUBLIC_ID1}"
    )


def test_failed_create_machine_by_id_1(test_client, init_database):
    """
    This method tests a failed post /machine/<public_id> API call
    Case: Integrity Error
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.post(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID2}",
        query_string={
            "Floor_id": constants.MACHINE_TEST_FLOOR_ID1,
            "Dorm": constants.MACHINE_TEST_DORM1,
            "Floor": constants.MACHINE_TEST_FLOOR1,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE2,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 500
    assert (json.loads(response.data)) == {
        'error': f'500 Internal Server Error: Machine {constants.MACHINE_TEST_PUBLIC_ID2} is already registered'}


def test_failed_create_machine_by_id_2(test_client, init_database):
    """
    This method tests a failed post /machine/<public_id> API call
    Case: Improper Input: Floor
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.post(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID1}",
        query_string={
            "Floor_id": constants.MACHINE_TEST_FLOOR_ID1,
            "Dorm": constants.MACHINE_TEST_DORM1,
            "Floor": "pizza",
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE1,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 400
    assert (json.loads(response.data)) == {
        'error': '400 Bad Request: Input(s) is not of correct type'}


def test_failed_create_machine_by_id_3(test_client, init_database):
    """
    This method tests a failed pu /machine/<public_id> API call
    Case: Not all required inputs given: Dorm
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.post(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID1}",
        query_string={
            "Floor_id": constants.MACHINE_TEST_FLOOR_ID1,
            "Floor": constants.MACHINE_TEST_FLOOR1,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE1,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 400
    assert (json.loads(response.data)) == {
        'error': '400 Bad Request: Dorm: None, is not recognized as a valid dorm'}


def test_failed_create_machine_by_id_4(test_client, init_database):
    """
    This method tests a failed post /machine/<public_id> API call
    Case: floor_id is out of range (machine.py line 51)
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.post(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID1}",
        query_string={
            "Floor_id": "101",
            "Dorm": constants.MACHINE_TEST_DORM1,
            "Floor": constants.MACHINE_TEST_FLOOR1,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE1,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 400
    assert (json.loads(response.data)) == {
        'error': '400 Bad Request: Floor_id: 101, is out of range of the acceptable ids'}


def test_failed_create_machine_by_id_5(test_client, init_database):
    """
    This method tests a failed post /machine/<public_id> API call
    Case: Floor is not a valid floor (machine.py line 55)
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.post(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID1}",
        query_string={
            "Floor_id": constants.MACHINE_TEST_FLOOR_ID1,
            "Dorm": constants.MACHINE_TEST_DORM1,
            "Floor": 11,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE1,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 400
    assert (json.loads(response.data)) == {
        'error': '400 Bad Request: Floor: 11, is out of range of the acceptable levels'}


def test_failed_create_machine_by_id_6(test_client, init_database):
    """
    This method tests a failed post /machine/<public_id> API call
    Case: Installation date is not formatted properly (machine.py line 58-59)
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.post(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID1}",
        query_string={
            "Floor_id": constants.MACHINE_TEST_FLOOR_ID1,
            "Dorm": constants.MACHINE_TEST_DORM1,
            "Floor": constants.MACHINE_TEST_FLOOR1,
            "Installation_date": 10/27/22,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 400
    assert (json.loads(response.data)) == {
        'error': '400 Bad Request: Installation date is not formatted properly, use: %m-%d-%Y'}


# ---------------------------GET------------------------------------


def test_successful_get_machine_by_id(test_client, init_database):
    """
    This method tests a successful get /machine/<public_id> API call
    Case: Completely proper get machine by id call
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.get(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID2}", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 200
    assert json.loads(response.data) == (
        {
            "Public_ID": constants.MACHINE_TEST_PUBLIC_ID2,
            "Floor_ID": constants.MACHINE_TEST_FLOOR_ID2,
            "Floor": constants.MACHINE_TEST_FLOOR2,
            "Dorm": constants.MACHINE_TEST_DORM2,
            "Status": constants.MACHINE_TEST_STATUS2,
            "Last_Service_Date": None,
            "Installation_Date": constants.MACHINE_TEST_INSTALLATION_DATE2,
            "Finish_Time": constants.MACHINE_TEST_FINISH_TIME2,
            "User_Name": constants.MACHINE_TEST_USER_NAME2,
        }
    )


def test_failed_get_machine_by_id(test_client, init_database):
    """
    This method tests a successful get /machine/<public_id> API call
    Case: Machine does not exist
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.get(
        "/machine/404", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 404
    assert (json.loads(response.data) == {
            'error': '404 Not Found: Could not GET machine with ID: 404'})


# ---------------------------PUT--------------------------------------


def test_successful_put_machine_by_id_1(test_client, init_database):
    """
    This method tests a successful put /machine/<public_id> API call
    Case: Completely proper put machine call
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.put(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID2}",
        query_string={
            "Floor_id": 5,
            "Floor": 1,
            "Status": "In_use",
            "Last_service_date": constants.MACHINE_TEST_LAST_SERVICE_DATE2,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE2,
            "Dorm": constants.MACHINE_TEST_DORM2
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 200
    assert json.loads(response.data) == (
        {
            "Public_ID": constants.MACHINE_TEST_PUBLIC_ID2,
            "Floor_ID": 5,
            "Floor": 1,
            "Dorm": constants.MACHINE_TEST_DORM2,
            "Status": "In_use",
            "Last_Service_Date": constants.MACHINE_TEST_LAST_SERVICE_DATE2,
            "Installation_Date": constants.MACHINE_TEST_INSTALLATION_DATE2,
            "Finish_Time": (int(time.time())+1800)//300,
            "User_Name": 'Hayden',
        }
    )


def test_successful_put_machine_by_id_2(test_client, init_database):
    """
    This method tests a successful put /machine/<public_id> API call
    Case: Completely proper put machine call but not all inputs given:
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.put(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID2}",
        query_string={
            "Floor_id": 5,
            "Floor": 1,
            "Status": "In_use",
            "Last_service_date": constants.MACHINE_TEST_LAST_SERVICE_DATE2,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE2,
            "Dorm": constants.MACHINE_TEST_DORM2,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 200
    assert json.loads(response.data) == (
        {
            "Public_ID": constants.MACHINE_TEST_PUBLIC_ID2,
            "Floor_ID": 5,
            "Floor": 1,
            "Dorm": constants.MACHINE_TEST_DORM2,
            "Status": "In_use",
            "Last_Service_Date": constants.MACHINE_TEST_LAST_SERVICE_DATE2,
            "Installation_Date": constants.MACHINE_TEST_INSTALLATION_DATE2,
            "User_Name": 'Hayden',
            "Finish_Time": (int(time.time())+1800)//300,
        }
    )


def test_failed_put_machine_by_id1(test_client, init_database):
    """
    This method tests a failed put /machine/<public_id> API call
    Case: Improper input: Floor
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.put(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID2}",
        query_string={
            "Floor_id": 5,
            "Floor": "Fourth",
            "Status": "In_use",
            "Last_service_date": constants.MACHINE_TEST_LAST_SERVICE_DATE2,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE2,
            "Dorm": constants.MACHINE_TEST_DORM2,
            "Finish_time": constants.MACHINE_TEST_FINISH_TIME2,
            "User_name": "Taylor",
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 400
    assert (json.loads(response.data)) == {
        'error': '400 Bad Request: Input(s) is not of correct type'}


def test_failed_put_machine_by_id2(test_client, init_database):
    """
    This method tests a failed put /machine/<public_id> API call
    Case: Inproper input: Status
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.put(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID2}",
        query_string={
            "Floor_id": 5,
            "Floor": 1,
            "Status": "Available",
            "Last_service_date": constants.MACHINE_TEST_LAST_SERVICE_DATE2,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE2,
            "Dorm": constants.MACHINE_TEST_DORM2,
            "Finish_time": constants.MACHINE_TEST_FINISH_TIME2,
            "User_name": "Taylor",
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 400
    assert (json.loads(response.data)) == {
        'error': "400 Bad Request: Status is not an acceptable status, use: 'Free', 'In_use', 'Broken'"}


def test_failed_put_machine_by_id3(test_client, init_database):
    """
    This method tests a failed put /machine/<public_id> API call
    Case: last_service_date is not formatted properly
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.put(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID2}",
        query_string={
            "Floor_id": 5,
            "Floor": 1,
            "Status": "In_use",
            "Last_service_date": 10/27/22,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE2,
            "Dorm": constants.MACHINE_TEST_DORM2,
            "Finish_time": constants.MACHINE_TEST_FINISH_TIME2,
            "User_name": "Taylor",
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 400
    assert (json.loads(response.data)) == {
        'error': "400 Bad Request: Installation date is not formatted properly, use: %m-%d-%Y"}


def test_failed_put_machine_by_id4(test_client, init_database):
    """
    This method tests a failed put /machine/<public_id> API call
    Case: Machine does not exist (machine.py line 157-158)
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.put(
        "/machine/404",
        query_string={
            "Floor_id": 5,
            "Floor": 1,
            "Status": "In_use",
            "Last_service_date": constants.MACHINE_TEST_LAST_SERVICE_DATE2,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE2,
            "Dorm": constants.MACHINE_TEST_DORM2,
            "Finish_time": constants.MACHINE_TEST_FINISH_TIME2,
            "User_name": "Taylor",
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 404
    assert (json.loads(response.data)) == {
        'error': '404 Not Found: Could not PUT machine with ID: 404'}


# ---------------------------DELETE--------------------------------------


def test_successful_delete_machine_by_id(test_client, init_database):
    """
    This method tests a succesful delete /machine/<public_id> API call
    Case: Completely proper delete machine call
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.delete(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID2}", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 200
    assert (
        json.loads(response.data)
        == f"Deleted information for machine with ID: {constants.MACHINE_TEST_PUBLIC_ID2}"
    )


def test_failed_delete_machine_by_id(test_client, init_database):
    """
    This method tests a failed delete /machine/<public_id> API call
    Case: Machine does not exist
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.delete(
        "/machine/404", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {
        'error': '404 Not Found: Machine not deleted, machine with the ID: 404, does not exist'}
