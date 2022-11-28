"""
This file holds the API routes for the error handlers
"""

from flask import Blueprint, jsonify, abort

error = Blueprint('error',__name__)

@error.errorhandler(400)
def custom_400_errorhandler(error_message):
    """
    Error handler for status code 400 which is a bad request
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error_message)), 400

@error.errorhandler(401)
def custom_401_errorhandler(error_message):
    """
    Error handler for status code 401 which is a unauthorized user error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error_message)), 401

@error.errorhandler(403)
def custom_403_errorhandler(error_message):
    """
    Error handler for status code 403 which is a Forbidden API error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error_message)), 403

@error.errorhandler(404)
def custom_404_errorhandler(error_message):
    """
    Error handler for status code 404 which is not found error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error_message)), 404

@error.errorhandler(429)
def custom_429_errorhandler(error_message):
    """
    Error handler for status code 429 which indicates to many requests
    have been made at this time
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error_message)), 429

@error.errorhandler(500)
def custom_500_errorhandler(error_message):
    """
    Error handler for status code 500 which is a internal server error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error_message)), 500

@error.errorhandler(502)
def custom_502_errorhandler(error_message):
    """
    Error handler for status code 502 which is a bad gateway error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error_message)), 502

@error.errorhandler(503)
def custom_503_errorhandler(error_message):
    """
    Error handler for status code 503 which is a service unavailable error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error_message)), 503

@error.errorhandler(504)
def custom_504_errorhandler(error_message):
    """
    Error handler for status code 504 which indicates the gateway has timed out
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error_message)), 504


#-----------------------------Route to test custom error templates-------------------

@error.route("/test/<int:error_code>")
def test_400_endpoint(error_code):
    """
    Error handler test end point
    Parameters: Takes in an error code
    Returns: A json message saying what the error is and the error code
    """
    abort(error_code, "ERROR MESSAGE")
