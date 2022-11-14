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
                "Favorite_Machine": user_info.favorite_machine,
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
    #TO-DO implement tests for this endpoint
    if request.method == "PUT":
        #Gather request arguments
        favorite_machine = request.args.get("favorite_machine")
        #Find User to update
        user_to_update = User.query.filter_by(public_id=requested_user_id).first_or_404()
        #Update the Change
        if favorite_machine != "None" and favorite_machine is not None:
            user_to_update.favorite_machine = int(favorite_machine)
        #Commit Changes
        db.session.commit()
        #Return Changes
        return jsonify(
            {
                "Name": user_to_update.name,
                "Public_ID": user_to_update.public_id,
                "Email": user_to_update.email,
                "Favorite_Machine": user_to_update.favorite_machine,
            }
        )
    abort(400)
    return jsonify("There was an error")
