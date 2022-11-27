"""
This file holds the tests for the machine/<dorm> route
"""

#pylint: disable = E1101, W0105, W0613, C0301
#E1101: Instance of 'scoped_session' has no 'add' member
#W0613: Unused argument 'init_database' (unused-argument)
#C0301: Line too long (102/100) (line-too-long)

import json
from tests import constants
from tests.conftest import get_mock_token


# ---------------------------GET MACHINE BY DORM --------------------------------------


def test_get_machines_by_dorm(test_client, init_database):
    """
    This method tests a successful /machine/<dorm> API call
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.get(
        f"/machine/{constants.MACHINE_TEST_DORM3}", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 200
    assert json.loads(response.data) == [
        {'Floor': constants.MACHINE_TEST_FLOOR2, 'Floor_ID': constants.MACHINE_TEST_FLOOR_ID2,
            'Public_ID': constants.MACHINE_TEST_PUBLIC_ID2, 'Status': constants.MACHINE_TEST_STATUS2},
        {'Floor': constants.MACHINE_TEST_FLOOR3, 'Floor_ID': constants.MACHINE_TEST_FLOOR_ID3,
            'Public_ID': constants.MACHINE_TEST_PUBLIC_ID3, 'Status': constants.MACHINE_TEST_STATUS3},
        {'Floor': constants.MACHINE_TEST_FLOOR4, 'Floor_ID': constants.MACHINE_TEST_FLOOR_ID4,
            'Public_ID': constants.MACHINE_TEST_PUBLIC_ID4, 'Status': constants.MACHINE_TEST_STATUS4}
    ]


def test_failed_get_machines_by_dorm(test_client, init_database):
    """
    This method tests a successful /machine/<dorm> API call
    Case: dorm does not exist
    Input Arguments: test_client
    Returns: Void
    """
    response = test_client.get("/machine/Bowers",
                               headers={"access_token": get_mock_token()})
    assert response.status_code == 400
    assert json.loads(response.data) == {
        'error': '400 Bad Request: Dorm: Bowers, is not recognized as a valid dorm'}
