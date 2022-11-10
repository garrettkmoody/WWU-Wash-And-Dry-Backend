from flask import Blueprint, jsonify

error = Blueprint('error',__name__)

# not found error
@error.errorhandler(404)
def catch_not_found(error):
    """
    Error handler for status code 404 which is not found error

    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 404


# bad request error
@error.errorhandler(400)
def catch_bad_requests(error):
    """
    Error handler for status code 404 which is a bad request
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 400


# internal server error
@error.errorhandler(500)
def catch_server_errors(error):
    """
    Error handler for status code 500 which is a server error

    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 500