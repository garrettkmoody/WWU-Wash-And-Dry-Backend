"""
This file holds the tests for the notification routes
"""

#pylint: disable = W0613, E1101
#W0613: Unused argument 'app_context'
#E1101: Instance of 'scoped_session' has no 'add' member

import pytest
from extensions import db
from app.models.machine import Machine
from app.models.user import User
from app.routes.notification import send_email
from tests import constants
from tests.testapp import app

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


# ---------------------------EMAIL AND NOTIFICATIONS --------------------------------------


def test_email_failure(app_context):
    """
    This method tests a failed send_email function call
    Input Arguments: app_context
    Returns: Void
    """
    response = send_email(constants.SUBJECT, constants.BODY, [])
    assert response.status_code == 400


# test_email_success is implicitly used in this test, no need for separate test
def test_send_notifications(app_context):
    """
    This function tests a successful send notification call
    and checks to see whether it updates the information

    Input Arguments: app_context
    Returns: Void
    """
    new_user = User(constants.USER_TEST_PUBLIC_ID, "Taylor",
                    "WWU-Wash-And-Dry@outlook.com")
    db.session.add(new_user)
    new_machine = Machine(
        constants.MACHINE_TEST_PUBLIC_ID2,
        constants.MACHINE_TEST_FLOOR_ID2,
        constants.MACHINE_TEST_DORM2,
        constants.MACHINE_TEST_FLOOR2,
        constants.MACHINE_TEST_INSTALLATION_DATE2,
    )
    db.session.add(new_machine)
    db.session.commit()
    app.test_client().get("/send-notifications")
    test_machine = Machine.query.filter_by(
        public_id=constants.MACHINE_TEST_PUBLIC_ID2
    ).first_or_404()
    User.query.filter_by(public_id=constants.USER_TEST_PUBLIC_ID).delete()
    Machine.query.filter_by(public_id=constants.USER_TEST_PUBLIC_ID).delete()
    Machine.query.filter_by(public_id=constants.MACHINE_TEST_PUBLIC_ID2).delete()
    db.session.commit()
    assert test_machine.status == "Free"
    assert test_machine.finish_time is None
    assert test_machine.user_name is None
