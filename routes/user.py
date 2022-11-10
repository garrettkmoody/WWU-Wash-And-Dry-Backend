from flask import Blueprint, request, jsonify, abort

from extensions import db
from models.user import User

user = Blueprint('user', __name__)

@user.route("/user/<requested_user_id>", methods=["GET", "DELETE"])
def user_by_id(requested_user_id):
    """
    Endpoint for getting and deleting user by their public ID
    Parameters: Takes in a user public ID
    Returns: For Get request returns information on user
             For Delete request returns a confirmation message
             Will also return errors if anything goes wrong
    """
    if request.method == "GET":
        # Filter can be changed later to be more secure
        # First_or_404 will abort if not found and send a 404
        user_info = User.query.filter_by(
            public_id=requested_user_id
        ).first_or_404()
        return jsonify(
            {
                "Name": user_info.name,
                "Public_ID": user_info.public_id,
                "Email": user_info.email,
            }
        )
    if request.method == "DELETE":
        # Filter can be changed later to be more secure
        delete_request = User.query.filter_by(
            public_id=requested_user_id
        ).delete()
        db.session.commit()
        if delete_request:
            return jsonify(
                f"deleted information for user with ID: {requested_user_id}"
            )
        abort(404)
    abort(400)
    return jsonify("There was an error")