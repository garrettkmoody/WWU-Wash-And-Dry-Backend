"""
This file holds the tests for the machine routes
"""

#pylint: disable = C0301, W0613, E1101, W0105
#C0301: Line too long (line 68 and line 312)
#W0613: Unused argument 'app_context'
#E1101: Instance of 'scoped_session' has no 'add' member
#W0105: String statement has no effect

import json
import time
import pytest
from app.models.machine import Machine
from extensions import db
from tests import constants
from tests.testapp import app, get_mock_token

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


# ---------------------------CREATE MACHINE BY ID--------------------------------------


def test_successful_create_machine_by_id_1(app_context):
    """
    This method tests a successful /createMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Completely proper create machine call
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().post(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID}",
        query_string={
            "Floor_id": constants.MACHINE_TEST_FLOOR_ID,
            "Dorm": constants.MACHINE_TEST_DORM,
            "Floor": constants.MACHINE_TEST_FLOOR,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 200
    assert (
        json.loads(response.data)
        == f"Created information for machine with ID: {constants.MACHINE_TEST_PUBLIC_ID}"
    )


def test_failed_create_machine_by_id_1(app_context):
    """
    This method tests a failed /createMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Integrity Error
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().post(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID}",
        query_string={
            "Floor_id": constants.MACHINE_TEST_FLOOR_ID,
            "Dorm": constants.MACHINE_TEST_DORM,
            "Floor": constants.MACHINE_TEST_FLOOR,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 500
    assert (json.loads(response.data)) == {
            'error': f'500 Internal Server Error: Machine {constants.MACHINE_TEST_PUBLIC_ID} is already registered'}


def test_failed_create_machine_by_id_2(app_context):
    """
    This method tests a failed /createMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Improper Input
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().post(
        "/machine/10",
        query_string={
            "Floor_id": constants.MACHINE_TEST_FLOOR_ID,
            "Dorm": constants.MACHINE_TEST_DORM,
            "Floor": "pizza",
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 400
    assert (json.loads(response.data)) == {
            'error': '400 Bad Request: Input(s) is not of correct type'}


def test_failed_create_machine_by_id_3(app_context):
    """
    This method tests a successful /createMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Not all required inputs given
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().post(
        "/machine/10",
        query_string={
            "Floor_id": constants.MACHINE_TEST_FLOOR_ID,
            "Floor": constants.MACHINE_TEST_FLOOR,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 400
    assert (json.loads(response.data)) == {
            'error': '400 Bad Request: Dorm: None, is not recognized as a valid dorm'}


# ---------------------------GET MACHINE BY ID--------------------------------------


def test_successful_get_machine_by_id(app_context):
    """
    This method tests a successful /getMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Completely Proper get machine by id call
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().get(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID}", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 200
    assert json.loads(response.data) == (
        {
            "Public_ID": 1,
            "Floor_ID": 1,
            "Floor": 1,
            "Dorm": "Sittner",
            "Status": "Free",
            "Last_Service_Date": None,
            "Installation_Date": "10-27-2022",
            "Finish_Time": None,
            "User_Name": None,
        }
    )


def test_failed_get_machine_by_id(app_context):
    """
    This method tests a successful /getMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Machine does not exist
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().get(
        "/machine/404", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 404
    assert (json.loads(response.data) == {
            'error': '404 Not Found: Could not GET machine with ID: 404'})


# ---------------------------PUT MACHINE BY ID--------------------------------------


def test_successful_put_machine_by_id_1(app_context):
    """
    This method tests a successful /putMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Completely Proper put machine call
    Input Arguments: app_context
    Returns: Void
    """

    response = app.test_client().put(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID}",
        query_string={
            "Floor_id": 5,
            "Floor": 1,
            "Status": "In_use",
            "Last_service_date": constants.MACHINE_TEST_LAST_SERVICE_DATE,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE,
            "Dorm": constants.MACHINE_TEST_DORM
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 200
    assert json.loads(response.data) == (
        {
            "Public_ID": 1,
            "Floor_ID": 5,
            "Floor": 1,
            "Dorm": "Sittner",
            "Status": "In_use",
            "Last_Service_Date": "10-27-2022",
            "Installation_Date": "10-27-2022",
            "Finish_Time": (int(time.time())+30),
            "User_Name": None,
        }
    )


def test_successful_put_machine_by_id_2(app_context):
    """
    This method tests a successful /putMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Completely Proper put machine call but not all inputs given
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().put(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID}",
        query_string={
            "Floor_id": 5,
            "Floor": 1,
            "Status": "In_use",
            "Last_service_date": constants.MACHINE_TEST_LAST_SERVICE_DATE,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE,
            "Dorm": constants.MACHINE_TEST_DORM,
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 200
    assert json.loads(response.data) == (
        {
            "Public_ID": 1,
            "Floor_ID": 5,
            "Floor": 1,
            "Dorm": "Sittner",
            "Status": "In_use",
            "Last_Service_Date": "10-27-2022",
            "Installation_Date": "10-27-2022",
            "User_Name": None,
            "Finish_Time": (int(time.time())+30),
        }
    )


def test_failed_put_machine_by_id(app_context):
    """
    This method tests a failed /putMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Improper Input
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().put(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID}",
        query_string={
            "Floor_id": 5,
            "Floor": "Fourth",  # improper input
            "Status": "In_use",
            "Last_service_date": constants.MACHINE_TEST_LAST_SERVICE_DATE,
            "Installation_date": constants.MACHINE_TEST_INSTALLATION_DATE,
            "Dorm": constants.MACHINE_TEST_DORM,
            "Finish_time": constants.MACHINE_TEST_FINISH_TIME,
            "User_name": "Taylor",
        },
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 400
    assert (json.loads(response.data)) == {
            'error': '400 Bad Request: Input(s) is not of correct type'}


# ---------------------------DELETE MACHINE BY ID--------------------------------------


def test_successful_delete_machine_by_id(app_context):
    """
    This method tests a succesful /deleteMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Completely proper delete machine call
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().delete(
        f"/machine/{constants.MACHINE_TEST_PUBLIC_ID}", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 200
    assert (
        json.loads(response.data)
        == f"Deleted information for machine with ID: {constants.MACHINE_TEST_PUBLIC_ID}"
    )


def test_failed_delete_machine_by_id(app_context):
    """
    This method tests a successful /deleteMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Case: Tries to delete a machine that does not exist
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().delete(
        "/machine/404", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 404


# --------------------------GET MACHINE BY DORM FLOOR FLOOR ID--------------------------------------


def test_successful_get_machine_by_dorm_floor_floor_id(app_context):
    """
    This method tests a successful
    /machine/{MACHINE_TEST_DORM}/{MACHINE_TEST_FLOOR}/{MACHINE_TEST_FLOOR_ID} API call
    Case: Completely Proper get machine by dorm floor floor_id
    Input Arguments: app_context
    Returns: Void
    """
    new_machine = Machine(
        constants.MACHINE_TEST_PUBLIC_ID,
        constants.MACHINE_TEST_FLOOR_ID,
        constants.MACHINE_TEST_DORM,
        constants.MACHINE_TEST_FLOOR,
        constants.MACHINE_TEST_INSTALLATION_DATE,
    )
    db.session.add(new_machine)
    db.session.commit()
    response = app.test_client().get(
        f"/machine/{constants.MACHINE_TEST_DORM}/{constants.MACHINE_TEST_FLOOR}/{constants.MACHINE_TEST_FLOOR_ID}",
        headers={"access_token": get_mock_token()},
    )
    Machine.query.filter_by(public_id=constants.MACHINE_TEST_PUBLIC_ID).delete()
    db.session.commit()
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "Public_ID": 1,
        "Status": constants.MACHINE_TEST_STATUS,
        "Finish_Time": constants.MACHINE_TEST_FINISH_TIME,
        "User_Name": constants.MACHINE_TEST_USER_NAME,
    }


def test_failed_get_machine_by_dorm_floor_floor_id(app_context):
    """
    This method tests a failed
    /machine/{MACHINE_TEST_DORM}/{MACHINE_TEST_FLOOR}/{MACHINE_TEST_FLOOR_ID} API call
    Case: machine does not exist
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().get(
        f"/machine/{constants.MACHINE_TEST_DORM}/{constants.MACHINE_TEST_FLOOR}/404",
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 404


# ---------------------------GET MACHINE BY DORM FLOOR--------------------------------------


def test_get_machines_by_dorm_floor(app_context):
    """
    This method tests a succesful /machine/{MACHINE_TEST_DORM}/{MACHINE_TEST_FLOOR} API call
    Input Arguments: app_context
    Return: Void
    """
    test_public_id = [1, 2, 3]
    test_floor_id = [1, 2, 3]
    new_machine0 = Machine(
        test_public_id[0],
        test_floor_id[0],
        constants.MACHINE_TEST_DORM,
        constants.MACHINE_TEST_FLOOR,
        constants.MACHINE_TEST_INSTALLATION_DATE,
    )
    new_machine1 = Machine(
        test_public_id[1],
        test_floor_id[1],
        constants.MACHINE_TEST_DORM,
        constants.MACHINE_TEST_FLOOR,
        constants.MACHINE_TEST_INSTALLATION_DATE,
    )
    new_machine2 = Machine(
        test_public_id[2],
        test_floor_id[2],
        constants.MACHINE_TEST_DORM,
        constants.MACHINE_TEST_FLOOR,
        constants.MACHINE_TEST_INSTALLATION_DATE,
    )
    db.session.add(new_machine0)
    db.session.add(new_machine1)
    db.session.add(new_machine2)
    db.session.commit()
    response = app.test_client().get(
        f"/machine/{constants.MACHINE_TEST_DORM}/{constants.MACHINE_TEST_FLOOR}",
        headers={"access_token": get_mock_token()},
    )
    Machine.query.filter_by(public_id=test_public_id[0]).delete()
    Machine.query.filter_by(public_id=test_public_id[1]).delete()
    Machine.query.filter_by(public_id=test_public_id[2]).delete()
    db.session.commit()
    assert response.status_code == 200
    assert json.loads(response.data) == [
        {"Public_ID": 1, "Floor_ID": 1, "Status": "Free"},
        {"Public_ID": 2, "Floor_ID": 2, "Status": "Free"},
        {"Public_ID": 3, "Floor_ID": 3, "Status": "Free"},
    ]


# TO-DO implement the code in the /routes/machine.py file for this test to pass
'''
def test_failed_get_machines_by_dorm_floor(app_context):
    """
    This method tests a succesful /machine/{MACHINE_TEST_DORM}/{MACHINE_TEST_FLOOR} API call
    Case: Floor does not exist
    Input Arguments: app_context
    Return: Void
    """
    response = app.test_client().get(
        f"/machine/{MACHINE_TEST_DORM}/404",
        headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 404
'''

# ---------------------------GET MACHINE BY DORM --------------------------------------


def test_get_machines_by_dorm(app_context):
    """
    This method tests a successful /machine/{MACHINE_TEST_DORM} API call
    Input Arguments: app_context
    Returns: Void
    """
    test_public_id = [1, 2, 3]
    test_floor_id = [1, 2, 3]
    test_floor = [1, 2, 3]
    new_machine0 = Machine(
        test_public_id[0],
        test_floor_id[0],
        constants.MACHINE_TEST_DORM,
        test_floor[0],
        constants.MACHINE_TEST_INSTALLATION_DATE,
    )
    new_machine1 = Machine(
        test_public_id[1],
        test_floor_id[1],
        constants.MACHINE_TEST_DORM,
        test_floor[1],
        constants.MACHINE_TEST_INSTALLATION_DATE,
    )
    new_machine2 = Machine(
        test_public_id[2],
        test_floor_id[2],
        constants.MACHINE_TEST_DORM,
        test_floor[2],
        constants.MACHINE_TEST_INSTALLATION_DATE,
    )
    db.session.add(new_machine0)
    db.session.add(new_machine1)
    db.session.add(new_machine2)
    db.session.commit()
    response = app.test_client().get(
        f"/machine/{constants.MACHINE_TEST_DORM}", headers={"access_token": get_mock_token()}
    )
    Machine.query.filter_by(public_id=test_public_id[0]).delete()
    Machine.query.filter_by(public_id=test_public_id[1]).delete()
    Machine.query.filter_by(public_id=test_public_id[2]).delete()
    db.session.commit()
    assert response.status_code == 200
    assert json.loads(response.data) == [
        {"Public_ID": 1, "Floor": 1, "Floor_ID": 1, "Status": "Free"},
        {"Public_ID": 2, "Floor": 2, "Floor_ID": 2, "Status": "Free"},
        {"Public_ID": 3, "Floor": 3, "Floor_ID": 3, "Status": "Free"},
    ]


# TO-DO implement the code in the /routes/machine.py file for this test to pass
'''
def test_get_machines_by_dorm(app_context):
    """
    This method tests a successful /machine/{MACHINE_TEST_DORM} API call
    Case: dorm does not exist
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().get(f"/machine/{MACHINE_TEST_DORM}",
    headers={"access_token": get_mock_token()})
    assert response.status_code == 404
'''
