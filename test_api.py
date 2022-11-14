"""
Test functions to ensure functionality of WWU-Wash-And-Dry-Backend's API endpoints.
"""

# pylint: disable = E1101, W0613

import datetime
import time
import json
import jwt
import pytest
from init import configure_app
from models.machine import Machine
from models.user import User
from routes.notification import send_email
from extensions import db, app

app = configure_app(app)

# Test Parameters for User
USER_TEST_ID = 1
USER_TEST_NAME = "Hayden"
USER_TEST_PUBLIC_ID = "10101"
USER_TEST_EMAIL = "Walla Walla"

# Test Parameters for Machine
MACHINE_TEST_PUBLIC_ID = 1
MACHINE_TEST_FLOOR_ID = 1
MACHINE_TEST_DORM = "Sittner"
MACHINE_TEST_FLOOR = 0
MACHINE_TEST_STATUS = "free"
MACHINE_TEST_LAST_SERVICE_DATE = "10/27/2022"
MACHINE_TEST_INSTALLATION_DATE = "10/27/2022"
MACHINE_TEST_FINISH_TIME = None
MACHINE_TEST_USER_NAME = None

# Test Parameters for Emails
RECIPIENTS = ["WWU-Wash-And-Dry@outlook.com"]
BODY = "Testing email"
SUBJECT = "Testing"

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


def test_unprotected_route():
    """
    This method tests a unprotected route and that a response is return succesfully
    Input Arguments: None
    Returns: Void
    """
    response = app.test_client().get("/unprotected")
    assert response.status_code == 200
    assert json.loads(response.data) == "No Token No problem!"


def test_get_user(app_context):
    """
    This method tests a succesful /getUser/{USER_TEST_PUBLIC_ID} API call
    Input Arguments: None
    Returns: Void
    """
    # create test user
    new_user = User(USER_TEST_PUBLIC_ID, USER_TEST_NAME, USER_TEST_EMAIL)
    db.session.add(new_user)
    db.session.commit()
    # send request
    response = app.test_client().get(f"/user/{USER_TEST_PUBLIC_ID}",
    headers={"access_token": get_mock_token()})
    # remove created user
    User.query.filter_by(public_id=USER_TEST_PUBLIC_ID).delete()
    db.session.commit()
    # test response
    assert response.status_code == 200
    assert json.loads(response.data) == (
        {
            "Name": USER_TEST_NAME,
            "Public_ID": USER_TEST_PUBLIC_ID,
            "Email": USER_TEST_EMAIL,
        }
    )


def test_delete_user(app_context):
    """
    This method tests a succesful /deleteUser/{USER_TEST_PUBLIC_ID} API call
    Input Arguments: app_context
    Returns: Void
    """
    new_user = User(USER_TEST_PUBLIC_ID, USER_TEST_NAME, USER_TEST_EMAIL)
    db.session.add(new_user)
    db.session.commit()
    response = app.test_client().delete(f"/user/{USER_TEST_PUBLIC_ID}",
    headers={"access_token": get_mock_token()})
    assert response.status_code == 200
    assert (
        json.loads(response.data)
        == f"deleted information for user with ID: {USER_TEST_PUBLIC_ID}"
    )


def test_get_machine_by_id(app_context):
    """
    This method tests a successful /getMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Input Arguments: app_context
    Returns: Void
    """
    new_machine = Machine(
        MACHINE_TEST_PUBLIC_ID,
        MACHINE_TEST_FLOOR_ID,
        MACHINE_TEST_DORM,
        MACHINE_TEST_FLOOR,
        MACHINE_TEST_STATUS,
        MACHINE_TEST_LAST_SERVICE_DATE,
        MACHINE_TEST_INSTALLATION_DATE,
        MACHINE_TEST_FINISH_TIME,
        MACHINE_TEST_USER_NAME,
    )
    db.session.add(new_machine)
    db.session.commit()
    response = app.test_client().get(f"/machine/{MACHINE_TEST_PUBLIC_ID}",
    headers={"access_token": get_mock_token()})
    Machine.query.filter_by(public_id=MACHINE_TEST_PUBLIC_ID).delete()
    db.session.commit()
    assert response.status_code == 200
    assert json.loads(response.data) == (
        {
            "Public_ID": 1,
            "Floor_ID": 1,
            "Floor": 0,
            "Dorm": "Sittner",
            "Status": "free",
            "Last_Service_Date": "10/27/2022",
            "Installation_Date": "10/27/2022",
            "Finish_Time": None,
            "User_Name": None,
        }
    )


def test_delete_machine_by_id(app_context):
    """
    This method tests a succesful /deleteMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Input Arguments: app_context
    Returns: Void
    """
    new_machine = Machine(
        MACHINE_TEST_PUBLIC_ID,
        MACHINE_TEST_FLOOR_ID,
        MACHINE_TEST_DORM,
        MACHINE_TEST_FLOOR,
        MACHINE_TEST_STATUS,
        MACHINE_TEST_LAST_SERVICE_DATE,
        MACHINE_TEST_INSTALLATION_DATE,
        MACHINE_TEST_FINISH_TIME,
        MACHINE_TEST_USER_NAME,
    )
    db.session.add(new_machine)
    db.session.commit()
    response = app.test_client().delete(f"/machine/{MACHINE_TEST_PUBLIC_ID}",
                                        headers={"access_token": get_mock_token()})
    Machine.query.filter_by(public_id=MACHINE_TEST_PUBLIC_ID).delete()
    assert response.status_code == 200
    assert (
        json.loads(response.data)
        == f"deleted information for machine with ID: {MACHINE_TEST_PUBLIC_ID}"
    )


def test_create_machine_by_id(app_context):
    """
    This method tests a successful /createMachine/{MACHINE_TEST_PUBLIC_ID} API call
    Input Arguments: app_context
    Returns: Void
    """
    response = app.test_client().post(
        f"/machine/{MACHINE_TEST_PUBLIC_ID}",
        query_string={
            "floor_id": MACHINE_TEST_FLOOR_ID,
            "dorm": MACHINE_TEST_DORM,
            "floor": MACHINE_TEST_FLOOR,
            "status": MACHINE_TEST_STATUS,
            "last_service_date": MACHINE_TEST_LAST_SERVICE_DATE,
            "installation_date": MACHINE_TEST_INSTALLATION_DATE,
            "finish_time": MACHINE_TEST_FINISH_TIME,
            "user_name": MACHINE_TEST_USER_NAME,
        },
        headers={"access_token": get_mock_token()})
    Machine.query.filter_by(public_id=MACHINE_TEST_PUBLIC_ID).delete()
    db.session.commit()
    assert response.status_code == 200
    assert (
        json.loads(response.data)
        == f"created information for machine with ID: {MACHINE_TEST_PUBLIC_ID}"
    )


def test_get_machine_by_dorm_floor_floor_id(app_context):
    """
    This method tests a successful
    /machine/{MACHINE_TEST_DORM}/{MACHINE_TEST_FLOOR}/{MACHINE_TEST_FLOOR_ID} API call
    Input Arguments: app_context
    Returns: Void
    """
    new_machine = Machine(
        MACHINE_TEST_PUBLIC_ID,
        MACHINE_TEST_FLOOR_ID,
        MACHINE_TEST_DORM,
        MACHINE_TEST_FLOOR,
        MACHINE_TEST_STATUS,
        MACHINE_TEST_LAST_SERVICE_DATE,
        MACHINE_TEST_INSTALLATION_DATE,
        MACHINE_TEST_FINISH_TIME,
        MACHINE_TEST_USER_NAME,
    )
    db.session.add(new_machine)
    db.session.commit()
    response = app.test_client().get(
        f"/machine/{MACHINE_TEST_DORM}/{MACHINE_TEST_FLOOR}/{MACHINE_TEST_FLOOR_ID}",
        headers={"access_token": get_mock_token()}
    )
    Machine.query.filter_by(public_id=MACHINE_TEST_PUBLIC_ID).delete()
    db.session.commit()
    assert response.status_code == 200
    assert json.loads(response.data) == {"Public_ID": 1, "Status": "free"}


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
        MACHINE_TEST_DORM,
        MACHINE_TEST_FLOOR,
        MACHINE_TEST_STATUS,
        MACHINE_TEST_LAST_SERVICE_DATE,
        MACHINE_TEST_INSTALLATION_DATE,
        MACHINE_TEST_FINISH_TIME,
        MACHINE_TEST_USER_NAME,
    )
    new_machine1 = Machine(
        test_public_id[1],
        test_floor_id[1],
        MACHINE_TEST_DORM,
        MACHINE_TEST_FLOOR,
        MACHINE_TEST_STATUS,
        MACHINE_TEST_LAST_SERVICE_DATE,
        MACHINE_TEST_INSTALLATION_DATE,
        MACHINE_TEST_FINISH_TIME,
        MACHINE_TEST_USER_NAME,
    )
    new_machine2 = Machine(
        test_public_id[2],
        test_floor_id[2],
        MACHINE_TEST_DORM,
        MACHINE_TEST_FLOOR,
        MACHINE_TEST_STATUS,
        MACHINE_TEST_LAST_SERVICE_DATE,
        MACHINE_TEST_INSTALLATION_DATE,
        MACHINE_TEST_FINISH_TIME,
        MACHINE_TEST_USER_NAME,
    )
    db.session.add(new_machine0)
    db.session.add(new_machine1)
    db.session.add(new_machine2)
    db.session.commit()
    response = app.test_client().get(
        f"/machine/{MACHINE_TEST_DORM}/{MACHINE_TEST_FLOOR}",
        headers={"access_token": get_mock_token()}
    )
    Machine.query.filter_by(public_id=test_public_id[0]).delete()
    Machine.query.filter_by(public_id=test_public_id[1]).delete()
    Machine.query.filter_by(public_id=test_public_id[2]).delete()
    db.session.commit()
    assert response.status_code == 200
    assert json.loads(response.data) == [
        {"Public_ID": 1, "Floor_ID": 1, "Status": "free"},
        {"Public_ID": 2, "Floor_ID": 2, "Status": "free"},
        {"Public_ID": 3, "Floor_ID": 3, "Status": "free"},
    ]


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
        MACHINE_TEST_DORM,
        test_floor[0],
        MACHINE_TEST_STATUS,
        MACHINE_TEST_LAST_SERVICE_DATE,
        MACHINE_TEST_INSTALLATION_DATE,
        MACHINE_TEST_FINISH_TIME,
        MACHINE_TEST_USER_NAME,
    )
    new_machine1 = Machine(
        test_public_id[1],
        test_floor_id[1],
        MACHINE_TEST_DORM,
        test_floor[1],
        MACHINE_TEST_STATUS,
        MACHINE_TEST_LAST_SERVICE_DATE,
        MACHINE_TEST_INSTALLATION_DATE,
        MACHINE_TEST_FINISH_TIME,
        MACHINE_TEST_USER_NAME,
    )
    new_machine2 = Machine(
        test_public_id[2],
        test_floor_id[2],
        MACHINE_TEST_DORM,
        test_floor[2],
        MACHINE_TEST_STATUS,
        MACHINE_TEST_LAST_SERVICE_DATE,
        MACHINE_TEST_INSTALLATION_DATE,
        MACHINE_TEST_FINISH_TIME,
        MACHINE_TEST_USER_NAME,
    )
    db.session.add(new_machine0)
    db.session.add(new_machine1)
    db.session.add(new_machine2)
    db.session.commit()
    response = app.test_client().get(f"/machine/{MACHINE_TEST_DORM}",
    headers={"access_token": get_mock_token()})
    Machine.query.filter_by(public_id=test_public_id[0]).delete()
    Machine.query.filter_by(public_id=test_public_id[1]).delete()
    Machine.query.filter_by(public_id=test_public_id[2]).delete()
    db.session.commit()
    assert response.status_code == 200
    assert json.loads(response.data) == [
        {"Public_ID": 1, "Floor": 1, "Floor_ID": 1, "Status": "free"},
        {"Public_ID": 2, "Floor": 2, "Floor_ID": 2, "Status": "free"},
        {"Public_ID": 3, "Floor": 3, "Floor_ID": 3, "Status": "free"},
    ]


def test_email_failure(app_context):
    """
    This method tests a failed send_email function call
    Input Arguments: app_context
    Returns: Void
    """
    response = send_email(SUBJECT, BODY, [])
    assert response.status_code == 400


# test_email_success is implicitly used in this test, no need for separate test
def test_send_notifications(app_context):
    """
    This function tests a successful send notification call
    and checks to see whether it updates the information

    Input Arguments: app_context
    Returns: Void
    """
    new_user = User(USER_TEST_PUBLIC_ID, "Taylor", "WWU-Wash-And-Dry@outlook.com")
    db.session.add(new_user)
    new_machine = Machine(
        MACHINE_TEST_PUBLIC_ID,
        MACHINE_TEST_FLOOR_ID,
        MACHINE_TEST_DORM,
        MACHINE_TEST_FLOOR,
        "in_use",
        MACHINE_TEST_LAST_SERVICE_DATE,
        MACHINE_TEST_INSTALLATION_DATE,
        int((time.time_ns() / 60000000000)),
        "Taylor",
    )
    db.session.add(new_machine)
    db.session.commit()
    app.test_client().get("/send-notifications")
    test_machine = Machine.query.filter_by(
        public_id=MACHINE_TEST_PUBLIC_ID
    ).first_or_404()
    User.query.filter_by(public_id=USER_TEST_PUBLIC_ID).delete()
    Machine.query.filter_by(public_id=USER_TEST_PUBLIC_ID).delete()
    Machine.query.filter_by(public_id=MACHINE_TEST_PUBLIC_ID).delete()
    db.session.commit()
    assert test_machine.status == "pick_up_laundry"
    assert test_machine.finish_time is None
    assert test_machine.user_name is None


def get_mock_token():
    """
    Will return a temporary JWT token for authenticated test api calls

    Returns: Token (String)
    """
    return jwt.encode(
        {
            "public_id": USER_TEST_PUBLIC_ID,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        },
        app.config["SECRET_KEY"],
        "HS256",
    )
