"""
This file holds the tests for the machine routes
"""

#pylint: disable = C0301, E1101, W0105, W0613
#C0301: Line too long (line 68 and line 312)
#E1101: Instance of 'scoped_session' has no 'add' member
#W0613: Unused argument 'init_database' (unused-argument)

import json
import time
from tests import constants
from tests.conftest import get_mock_token


# ---------------------------CREATE MACHINE BY ID--------------------------------------


def test_successful_create_machine_by_id_1(test_client, init_database):
    """
    This method tests a successful /createMachine/{MACHINE_TEST_PUBLIC_ID} API call
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
    This method tests a failed /createMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Integrity Error
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.post(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID2}",
        query_string={
            "Floor_id": constants.MACHINE_TEST_FLOOR_ID2,
            "Dorm": constants.MACHINE_TEST_DORM2,
            "Floor": constants.MACHINE_TEST_FLOOR2,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE2,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 500
    assert (json.loads(response.data)) == {
            'error': f'500 Internal Server Error: Machine {constants.MACHINE_TEST_PUBLIC_ID2} is already registered'}


def test_failed_create_machine_by_id_2(test_client, init_database):
    """
    This method tests a failed /createMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Improper Input
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.post(
        "/machine/10",
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
    This method tests a successful /createMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Not all required inputs given
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.post(
        "/machine/10",
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


# ---------------------------GET MACHINE BY ID--------------------------------------


def test_successful_get_machine_by_id(test_client, init_database):
    """
    This method tests a successful /getMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Completely Proper get machine by id call
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
    This method tests a successful /getMachine/{MACHINE_TEST_PUBLIC_ID} API call
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


# ---------------------------PUT MACHINE BY ID--------------------------------------


def test_successful_put_machine_by_id_1(test_client, init_database):
    """
    This method tests a successful /putMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Completely Proper put machine call
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
    This method tests a successful /putMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Completely Proper put machine call but not all inputs given
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


def test_failed_put_machine_by_id(test_client, init_database):
    """
    This method tests a failed /putMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Improper Input
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.put(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID2}",
        query_string={
            "Floor_id": 5,
            "Floor": "Fourth",  # improper input
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


# ---------------------------DELETE MACHINE BY ID--------------------------------------


def test_successful_delete_machine_by_id(test_client, init_database):
    """
    This method tests a succesful /deleteMachine/{MACHINE_TEST_PUBLIC_ID} API call
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
    This method tests a successful /deleteMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Tries to delete a machine that does not exist
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.delete(
        "/machine/404", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {'error': '404 Not Found: Machine not deleted, machine with the ID: 404, does not exist'}


# --------------------------GET MACHINE BY DORM FLOOR FLOOR ID--------------------------------------


def test_successful_get_machine_by_dorm_floor_floor_id(test_client, init_database):
    """
    This method tests a successful
    /machine/{MACHINE_TEST_DORM}/{MACHINE_TEST_FLOOR}/{MACHINE_TEST_FLOOR_ID} API call
    Case: Completely Proper get machine by dorm floor floor_id
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
    /machine/{MACHINE_TEST_DORM}/{MACHINE_TEST_FLOOR}/{MACHINE_TEST_FLOOR_ID} API call
    Case: machine does not exist
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.get(
        f"/machine/{constants.MACHINE_TEST_DORM2}/{constants.MACHINE_TEST_FLOOR2}/404",
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {'error': '404 Not Found: Could not GET machine with Floor_ID: 404'}


# ---------------------------GET MACHINE BY DORM FLOOR--------------------------------------


def test_get_machines_by_dorm_floor(test_client, init_database):
    """
    This method tests a succesful /machine/{MACHINE_TEST_DORM}/{MACHINE_TEST_FLOOR} API call
    Input Arguments: test_client
    Return: Void
    """
    response = test_client.get(
        f"/machine/{constants.MACHINE_TEST_DORM2}/{constants.MACHINE_TEST_FLOOR2}",
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 200
    assert json.loads(response.data) == [
        {'Floor_ID': constants.MACHINE_TEST_FLOOR_ID2, 'Public_ID': constants.MACHINE_TEST_PUBLIC_ID2, 'Status': constants.MACHINE_TEST_STATUS2},
        {'Floor_ID': constants.MACHINE_TEST_FLOOR_ID3, 'Public_ID': constants.MACHINE_TEST_PUBLIC_ID3, 'Status': constants.MACHINE_TEST_STATUS3},
        {'Floor_ID': constants.MACHINE_TEST_FLOOR_ID4, 'Public_ID': constants.MACHINE_TEST_PUBLIC_ID4, 'Status': constants.MACHINE_TEST_STATUS4}
    ]


def test_failed_get_machines_by_dorm_floor(test_client, init_database):
    """
    This method tests a succesful /machine/{MACHINE_TEST_DORM}/{MACHINE_TEST_FLOOR} API call
    Case: Floor does not exist
    Input Arguments: test_client
    Return: Void
    """
    response = test_client.get(
        f"/machine/{constants.MACHINE_TEST_DORM3}/404",
        headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {'error': '404 Not Found: There are no machines in the dorm: Foreman, on floor: 404'}


# ---------------------------GET MACHINE BY DORM --------------------------------------


def test_get_machines_by_dorm(test_client, init_database):
    """
    This method tests a successful /machine/{MACHINE_TEST_DORM} API call
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.get(
        f"/machine/{constants.MACHINE_TEST_DORM3}", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 200
    assert json.loads(response.data) == [
        {'Floor': constants.MACHINE_TEST_FLOOR2, 'Floor_ID': constants.MACHINE_TEST_FLOOR_ID2, 'Public_ID': constants.MACHINE_TEST_PUBLIC_ID2, 'Status': constants.MACHINE_TEST_STATUS2},
        {'Floor': constants.MACHINE_TEST_FLOOR3, 'Floor_ID': constants.MACHINE_TEST_FLOOR_ID3, 'Public_ID': constants.MACHINE_TEST_PUBLIC_ID3, 'Status': constants.MACHINE_TEST_STATUS3},
        {'Floor': constants.MACHINE_TEST_FLOOR4, 'Floor_ID': constants.MACHINE_TEST_FLOOR_ID4, 'Public_ID': constants.MACHINE_TEST_PUBLIC_ID4, 'Status': constants.MACHINE_TEST_STATUS4}
    ]


def test_failed_get_machines_by_dorm(test_client, init_database):
    """
    This method tests a successful /machine/{MACHINE_TEST_DORM} API call
    Case: dorm does not exist
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.get("/machine/Bowers",
    headers={"access_token": get_mock_token()})
    assert response.status_code == 400
    assert json.loads(response.data) == {'error': '400 Bad Request: Dorm: Bowers, is not recognized as a valid dorm'}
