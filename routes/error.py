"""
This file holds the API routes for the error handlers
"""

#pylint: disable = W0621

from flask import Blueprint, jsonify

error = Blueprint('error',__name__)

@error.errorhandler(400)
def catch_bad_requests(error):
    """
    Error handler for status code 400 which is a bad request
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 400

@error.errorhandler(401)
def unauthorized_error(error):
    """
    Error handler for status code 401 which is a unauthorized user error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 403

@error.errorhandler(403)
def forbidden_error(error):
    """
    Error handler for status code 403 which is a Forbidden API error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 403

@error.errorhandler(404)
def catch_not_found(error):
    """
    Error handler for status code 404 which is not found error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 404

@error.errorhandler(429)
def too_many_requests_error(error):
    """
    Error handler for status code 429 which indicates to many requests
    have been made at this time
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 429

  # internal server error
@error.errorhandler(500)
def catch_server_errors(error):
    """
    Error handler for status code 500 which is a internal server error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 500

@error.errorhandler(502)
def bad_gateway_error(error):
    """
    Error handler for status code 502 which is a bad gateway error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 502

@error.errorhandler(503)
def service_unavailable_error(error):
    """
    Error handler for status code 503 which is a service unavailable error
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 503

@error.errorhandler(504)
def gateway_timeout_error(error):
    """
    Error handler for status code 504 which indicates the gateway has timed out
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 504
