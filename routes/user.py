"""
This file holds the API routes for get, delete, and put users
"""

#pylint: disable = E1101, W0613

from flask import Blueprint, request, jsonify, abort
from extensions import db
from models.user import User
from routes.token import token_required

user = Blueprint('user', __name__)

@user.route("/user/<requested_user_id>", methods=["GET", "DELETE", "PUT"])
@token_required
def user_by_id(current_user, requested_user_id):
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
                "Dorm": user_info.dorm,
                "Floor": user_info.floor
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
    if request.method == "PUT":
        dorm_list = ["Sittner", "Conard", "Foreman"]
        #Get Parameters to update
        dorm = request.args.get("Dorm")
        floor = request.args.get("Floor")
        # Checking Parameter Arguments
        if int(floor) < 0 | int(floor) > 100:
            abort(400)
        if dorm not in dorm_list:
            abort(400)
        #Get User to update
        user_to_update = User.query.filter_by(public_id=requested_user_id).first_or_404()
        #Update User
        user_to_update.dorm = dorm
        user_to_update.floor = floor
        #Save changes
        db.session.commit()
        #Return dict with updated changes
        return jsonify(
            {
                "Name": user_to_update.name,
                "Public_ID": user_to_update.public_id,
                "Email": user_to_update.email,
                "Dorm": user_to_update.dorm,
                "Floor": user_to_update.floor
            }
        )

    abort(400)
    return jsonify("There was an error")
