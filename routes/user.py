"""
This file holds the API routes for get, delete, and put users
"""

#pylint: disable = E1101, W0613
#E1101: Instance of '' has no '' member (no-member)
#W0613: Unused argument 'current_user' (unused-argument)

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
        try:
            # Find user and return their information
            user_info = User.query.filter_by(
                public_id=requested_user_id
            ).first()
            return jsonify(
                {
                    "Name": user_info.name,
                    "Public_ID": user_info.public_id,
                    "Email": user_info.email,
                    "Dorm": user_info.dorm,
                    "Floor": user_info.floor
                }
            )
        except AttributeError:
            abort(404, f"Could not GET user with ID: {requested_user_id}")
    if request.method == "DELETE":
        # Find user and delete them
        delete_request = User.query.filter_by(
            public_id=requested_user_id
        ).delete()
        db.session.commit()
        if delete_request:
            return jsonify(
                f"deleted information for user with ID: {requested_user_id}"
            )
        abort(404, f"User not deleted, user with ID: {requested_user_id}, does not exist")
    if request.method == "PUT":
        dorm_list = ["Sittner", "Conard", "Foreman"]
        #Get parameters to update
        dorm = request.args.get("Dorm")
        floor = int(request.args.get("Floor"))
        # Checking Parameter Arguments
        if floor < 0 | floor > 100:
            abort(400, "Floor is out of range of the acceptable levels")
        if dorm not in dorm_list:
            abort(400, "Dorm is not recognized as a valid dorm")
        try:
            #Get User to update
            user_to_update = User.query.filter_by(public_id=requested_user_id).first()
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
        except AttributeError:
            abort(404, f"Could not PUT user with ID: {requested_user_id}")
    return abort(400, "No method available to handle that call")
