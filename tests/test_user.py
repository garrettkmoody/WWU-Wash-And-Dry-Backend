"""
This file holds the tests for user routes
"""

#pylint: disable = W0613, E1101
#W0613: Unused argument 'app_context'
#E1101: Instance of 'scoped_session' has no 'add' member

import json
import pytest
from extensions import db
from app.models.user import User
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

# ---------------------------GET USER BY ID--------------------------------------


def test_get_user(app_context):
    """
    This method tests a succesful /getUser/{USER_TEST_PUBLIC_ID} API call
    Input Arguments: None
    Returns: Void
    """
    # create test user
    new_user = \
        User(constants.USER_TEST_PUBLIC_ID, constants.USER_TEST_NAME, constants.USER_TEST_EMAIL)
    db.session.add(new_user)
    db.session.commit()
    # send request
    response = app.test_client().get(
        f"/user/{constants.USER_TEST_PUBLIC_ID}", headers={"access_token": get_mock_token()}
    )
    # test response
    assert response.status_code == 200
    assert json.loads(response.data) == (
        {
            "Name": constants.USER_TEST_NAME,
            "Public_ID": constants.USER_TEST_PUBLIC_ID,
            "Email": constants.USER_TEST_EMAIL,
            "Dorm": None,
            "Floor": None
        }
    )


# ---------------------------UPDATE USER BY ID--------------------------------------


def test_update_user(app_context):
    """
    This method tests a successful /putUser/{USER_TEST_PUBLIC_ID} API call
    Input Arguments: app_context
    Returns: Void
    """

    response = app.test_client().put(f"/user/{constants.USER_TEST_PUBLIC_ID}", query_string={
        "Floor": constants.USER_TEST_FLOOR, "Dorm": constants.USER_TEST_DORM},
        headers={"access_token": get_mock_token()})
    assert response.status_code == 200
    assert json.loads(response.data) == (
        {
            "Name": constants.USER_TEST_NAME,
            "Public_ID": constants.USER_TEST_PUBLIC_ID,
            "Email": constants.USER_TEST_EMAIL,
            "Dorm": constants.USER_TEST_DORM,
            "Floor": constants.USER_TEST_FLOOR,
        }
    )

# ---------------------------DELETE USER BY ID--------------------------------------


def test_delete_user(app_context):
    """
    This method tests a succesful /deleteUser/{USER_TEST_PUBLIC_ID} API call
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().delete(
        f"/user/{constants.USER_TEST_PUBLIC_ID}", headers={"access_token": get_mock_token()}
    )
    assert response.status_code == 200
    assert (
        json.loads(response.data)
        == f"deleted information for user with ID: {constants.USER_TEST_PUBLIC_ID}"
    )
