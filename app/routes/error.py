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


#-----------------------------Routes to test custom error templates-------------------

@error.route("/test400")
def test_400_endpoint():
    """
    Error handler for status code 400 which is a bad request
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    abort(400, "Bad Request")


@error.route("/test401")
def test_401_endpoint():
    """
    Test for 401 error handler
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    abort(401, "Unauthorized User")

@error.route("/test403")
def test_403_endpoint():
    """
    Test for 403 error handler
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    abort(403, "Forbidden API Call")

@error.route("/test404")
def test_404_endpoint():
    """
    Test for 404 error handler
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    abort(404, "Page Not Found")

@error.route("/test429")
def test_429_endpoint():
    """
    Test for 429 error handler
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    abort(429, "Too Many Requests")

@error.route("/test500")
def test_500_endpoint():
    """
    Test for 500 error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    abort(500, "Internal Server Error")

@error.route("/test502")
def test_502_endpoint():
    """
    Test for 502 error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    abort(502, "Bad Gateway")

@error.route("/test503")
def test_503_endpoint():
    """
    Test for 503 error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    abort(503, "Service Unavailable")

@error.route("/test504")
def test_504_endpoint():
    """
    Test for 504 error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    abort(504, "Gateway Timed Out")
