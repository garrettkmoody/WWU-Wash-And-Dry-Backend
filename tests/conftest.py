"""
This file holds the app and mock tocked for the test application
"""
import pytest
import datetime
import jwt
from extensions import app, db
from init import configure_app
from tests import constants
from app.models.user import User
from app.models.machine import Machine

app = configure_app(app)

# This pytest fixture allows us to update database within our test file.
@pytest.fixture(scope = "module")
def test_client():
    """
    This method allows us to edit app content.
    Input Arguments: None
    Return: Void
    """
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

@pytest.fixture(scope='function')
def init_database(test_client):
    db.create_all()

    # Can insert test data here later
    new_user = \
        User(constants.USER_TEST_PUBLIC_ID1, constants.USER_TEST_NAME1, constants.USER_TEST_EMAIL1)
    db.session.add(new_user)

    # For test_machines
    new_machine1 = Machine(
        constants.MACHINE_TEST_PUBLIC_ID2,
        constants.MACHINE_TEST_FLOOR_ID2,
        constants.MACHINE_TEST_DORM2,
        constants.MACHINE_TEST_FLOOR2,
        constants.MACHINE_TEST_INSTALLATION_DATE2,
    )
    new_machine2 = Machine(
        constants.MACHINE_TEST_PUBLIC_ID3,
        constants.MACHINE_TEST_FLOOR_ID3,
        constants.MACHINE_TEST_DORM3,
        constants.MACHINE_TEST_FLOOR3,
        constants.MACHINE_TEST_INSTALLATION_DATE3,
    )
    new_machine3 = Machine(
        constants.MACHINE_TEST_PUBLIC_ID4,
        constants.MACHINE_TEST_FLOOR_ID4,
        constants.MACHINE_TEST_DORM4,
        constants.MACHINE_TEST_FLOOR4,
        constants.MACHINE_TEST_INSTALLATION_DATE4,
    )
    db.session.add(new_machine1)
    db.session.add(new_machine2)
    db.session.add(new_machine3)
    db.session.commit()

    yield

    db.drop_all()

# ---------------------------MOCK TOKEN FOR API CALLS --------------------------------------

def get_mock_token():
    """
    Will return a temporary JWT token for authenticated test api calls
    Input Arguments: None
    Returns: Token (String)
    """
    return jwt.encode(
        {
            "public_id": constants.USER_TEST_PUBLIC_ID1,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        },
        app.config["SECRET_KEY"],
        "HS256",
    )
