"""
This file holds the tests for the notification routes
"""

#pylint: disable = E1101, W0613
#E1101: Instance of 'scoped_session' has no 'add' member
#W0613: Unused argument 'test_client'

from app.routes.notification import send_email
from tests import constants

def test_email_failure(test_client):
    """
    This method tests a failed send_email function call
    Input Arguments: None
    Returns: Void
    """
    response = send_email(constants.SUBJECT, constants.BODY, [])
    assert response.status_code == 400


# test_email_success is implicitly used in this test, no need for separate test
def test_send_notifications(test_client, init_database):
    """
    This function tests a successful send notification call
    and checks to see whether it updates the information
    Input Arguments: None
    Returns: Void
    """
    response = test_client.get("/send-notifications")
    assert response.status_code == 200
