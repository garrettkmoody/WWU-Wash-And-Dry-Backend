"""
This file holds the API routes for access tokens
"""

#pylint: disable = W0702
#W0702: No exception type(s) specified (bare-except)

from functools import wraps
from flask import Blueprint, jsonify, request
import jwt
from extensions import app
from app.models.user import User

tokens = Blueprint('token', __name__)

def token_required(function_decorator):
    """
    Token Function Decorator
    """
    @wraps(function_decorator)
    def decorator(*args, **kwargs):
        token = None
        if "access_token" in request.headers:
            token = request.headers["access_token"]

        if not token:
            return jsonify({"message": "Missing Authentication Token!"}), 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Invalid Authentication Token!"}), 401

        return function_decorator(current_user, *args, **kwargs)

    return decorator

# Unprotected route, no token required
@tokens.route("/unprotected")
def unprotected():
    """
    Unprotected endpoint
    Returns: A confirmation message
    """
    return jsonify("No Token No problem!")


# Protected route, token required
@tokens.route("/protected")
@token_required
def protected(current_user):
    """
    Protected endpoint
    Parameters: Current user
    Returns: A json message that greets the current user
    """
    return jsonify("Hello " + current_user.name)
