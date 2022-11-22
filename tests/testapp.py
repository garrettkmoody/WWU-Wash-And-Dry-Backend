"""
This file holds the app and mock tocked for the test application
"""

import datetime
import jwt
from extensions import app
from init import configure_app
from tests import constants

app = configure_app(app)

# ---------------------------MOCK TOKEN FOR API CALLS --------------------------------------

def get_mock_token():
    """
    Will return a temporary JWT token for authenticated test api calls

    Returns: Token (String)
    """
    return jwt.encode(
        {
            "public_id": constants.USER_TEST_PUBLIC_ID,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        },
        app.config["SECRET_KEY"],
        "HS256",
    )
