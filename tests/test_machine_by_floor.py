"""
This file holds the tests for the machine/<dorm>/<floor> route
"""

#pylint: disable = C0301, E1101, W0105, W0613
# C0301: Line too long (line 68 and line 312)
# E1101: Instance of 'scoped_session' has no 'add' member
# W0613: Unused argument 'init_database' (unused-argument)

import json
from tests import constants
from tests.conftest import get_mock_token


# ---------------------------------GET--------------------------------------


def test_get_machines_by_dorm_floor(test_client, init_database):
    """
    This method tests a succesful /machine/<dorm>/<floor> API call
    Input Arguments: test_client
    Return: Void
    """
    response = test_client.get(
        f"/machine/{constants.MACHINE_TEST_DORM2}/{constants.MACHINE_TEST_FLOOR2}",
        headers={"access_token": get_mock_token()},
    )
    assert response.status_code == 200
    assert json.loads(response.data) == [
        {'Floor_ID': constants.MACHINE_TEST_FLOOR_ID2,
            'Public_ID': constants.MACHINE_TEST_PUBLIC_ID2, 'Status': constants.MACHINE_TEST_STATUS2},
        {'Floor_ID': constants.MACHINE_TEST_FLOOR_ID3,
            'Public_ID': constants.MACHINE_TEST_PUBLIC_ID3, 'Status': constants.MACHINE_TEST_STATUS3},
        {'Floor_ID': constants.MACHINE_TEST_FLOOR_ID4,
            'Public_ID': constants.MACHINE_TEST_PUBLIC_ID4, 'Status': constants.MACHINE_TEST_STATUS4}
    ]


def test_failed_get_machines_by_dorm_floor1(test_client, init_database):
    """
    This method tests a failed /machine/<dorm>/<floor> API call
    Case: Floor is out of range of acceptable floors (machine.py line 237)
    Input Arguments: test_client
    Return: Void
    """
    response = test_client.get(
        f"/machine/{constants.MACHINE_TEST_DORM2}/101",
        headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 400
    assert json.loads(response.data) == {
        'error': '400 Bad Request: Floor 101, is out of range of the acceptable levels'}


def test_failed_get_machines_by_dorm_floor2(test_client, init_database):
    """
    This method tests a failed /machine/<dorm>/<floor> API call
    Case: dorm is not in dorm list (machine.py line 237)
    Input Arguments: test_client
    Return: Void
    """
    response = test_client.get(
        f"/machine/Bowers/{constants.MACHINE_TEST_FLOOR2}",
        headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 400
    assert json.loads(response.data) == {
        'error': '400 Bad Request: Dorm: Bowers, is not recognized as a valid dorm'}


def test_failed_get_machines_by_dorm_floor3(test_client, init_database):
    """
    This method tests a succesful /machine/<dorm>/<floor> API call
    Case: Machines do not exist on specified floor (machine.py line 247-248)
    Input Arguments: test_client
    Return: Void
    """
    response = test_client.get(
        f"/machine/{constants.MACHINE_TEST_DORM3}/99",
        headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {
        'error': '404 Not Found: There are no machines in the dorm: Foreman, on floor: 99'}
