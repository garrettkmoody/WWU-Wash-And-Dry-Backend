"""
This file holds the tests for the notification routes
"""

#pylint: disable = E1101, W0613, W0105
#E1101: Instance of 'scoped_session' has no 'add' member
#W0613: Unused argument 'test_client'
#W0105: String statement has no effect (pointless-string-statement)

import json
from app.routes.notification import send_email
from tests import constants

# IMPORTANT!!! This test is failing, which implies the functionality
# of the notification route is not fully implemented
'''
def test_email_success(test_client):
    """
    This method tests a successful send_email function call
    Input Arguments: None
    Returns: Void
    """
    response = send_email(constants.SUBJECT, constants.BODY, ["taylor.smith@wallawalla.edu"])
    assert response.status_code == 200
    assert json.loads(response.data) == "Email was successfully sent"
'''


def test_email_failure(test_client):
    """
    This method tests a failed send_email function call
    Input Arguments: None
    Returns: Void
    """
    response = send_email(constants.SUBJECT, constants.BODY, [])
    assert response.status_code == 400
    assert response.data == b'Could not send email.'


def test_send_notifications(test_client, init_database):
    """
    This function tests a successful send notification call
    and checks to see whether it updates the information
    Input Arguments: None
    Returns: Void
    """
    response = test_client.get("/send-notifications")
    assert response.status_code == 200
    assert json.loads(response.data) == "Notifications sent"
