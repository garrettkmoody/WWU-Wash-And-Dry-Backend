"""
This file holds the API routes for post, get, delete, and put machines
"""

#pylint: disable = E1101, R0912, R0915, W0613
#E1101: Instance of '' has no '' member (no-member)
#R0912: Too many branches (23/12) (too-many-branches)
#R0915: Too many statements (63/50) (too-many-statements)
#W0613: Unused argument 'current_user' (unused-argument)

import datetime
import time
from flask import Blueprint, request, jsonify, abort
from extensions import db
from models.machine import Machine
from routes.token import token_required

machine = Blueprint("machine", __name__)

DORM_LIST = ["Sittner", "Conard", "Foreman"]
STATUS_LIST = ["Free", "In_use", "Broken"]
TIMER = 30


@machine.route("/machine/<int:requested_id>", methods=["GET", "DELETE", "POST", "PUT"])
@token_required
def machine_by_id(current_user, requested_id):
    """
    Endpoint for getting/posting/deleting/putting a machine by its ID
    Parameter: ID for the machine
    Returns: POST: A confirmation message if it works
             DELETE: A confirmation message that the machine has been deleted
             GET: The machine's information
             PUT: The machine's updated information
    """
    #Accepting General Use Parameter Arguments
    if request.args:
        # Accepting Parameter Arguments
        floor_id = int(request.args.get("Floor_id"))
        dorm = request.args.get("Dorm")
        floor = int(request.args.get("Floor"))
        installation_date = request.args.get("Installation_date")
        # Checking Parameter Arguments
        if floor_id < 0 | floor_id > 100:
            abort(400, "Floor_id is out of range of the acceptable ids")
        if dorm not in DORM_LIST:
            abort(400, "Dorm is not recognized as a valid dorm")
        if floor < 0 | floor > 10:
            abort(400, "Floor is out of range of the acceptable levels")
        try:
            datetime.datetime.strptime(installation_date, "%m-%d-%Y")
        except ValueError:
            abort(400, "Installation date is not formatted properly, use: %m-%d-%Y")
        # Parameter Arguments are valid, attempt to create user
    if request.method == "POST":
        try:
            new_machine = Machine(
                int(requested_id),
                floor_id,
                dorm,
                floor,
                installation_date,
            )
            db.session.add(new_machine)
            db.session.commit()
            return (
                jsonify(
                    f"Created information for machine with ID: {requested_id}"
                ), 200
            )
        except db.IntegrityError:
            abort(500, f"Machine {requested_id} is already registered.")
    if request.method == "GET":
        try:
            # Find the Machine
            machine_info = Machine.query.filter_by(public_id=requested_id).first()
            # Return as a json dictionary
            return jsonify(
                {
                    "Public_ID": machine_info.public_id,
                    "Floor_ID": machine_info.floor_id,
                    "Floor": machine_info.floor,
                    "Dorm": machine_info.dorm,
                    "Status": machine_info.status,
                    "Last_Service_Date": machine_info.last_service_date,
                    "Installation_Date": machine_info.installation_date,
                    "Finish_Time": machine_info.finish_time,
                    "User_Name": machine_info.user_name,
                }
            )
        except AttributeError:
            abort(404, f"Could not GET machine with ID: {requested_id}")
    if request.method == "DELETE":
        # Try to delete the machine, if not abort with a 404 error
        delete_request = Machine.query.filter_by(public_id=requested_id).delete()
        db.session.commit()
        if delete_request:
            return jsonify(f"Deleted information for machine with ID: {requested_id}")
        abort(404, f"Machine not deleted, machine with the ID: {requested_id}, does not exist")
    if request.method == "PUT":
        # Accept Parameters only used by PUT
        status = request.args.get("Status")
        last_service_date = request.args.get("Last_service_date")
        if status not in STATUS_LIST:
            abort(400, "Status is not an acceptable status, use: 'Free', 'In_use', 'Broken'")
        try:
            datetime.datetime.strptime(last_service_date, "%m-%d-%Y")
        except ValueError:
            abort(400, "Installation date is not formatted properly, use: %m-%d-%Y")
        try:
            # Find machine to update
            machine_to_update = Machine.query.filter_by(
                public_id=requested_id
            ).first()
            # Update the changes
            if floor_id is not None:
                machine_to_update.floor_id = floor_id
            if dorm is not None:
                machine_to_update.dorm = dorm
            if floor is not None:
                machine_to_update.floor = floor
            if status is not None:
                machine_to_update.status = status
                if status == "In_use":
                    machine_to_update.finish_time = int(time.time()) + TIMER
            if installation_date is not None:
                machine_to_update.installation_date = installation_date
            if last_service_date is not None:
                machine_to_update.last_service_date = last_service_date
            if current_user is not None:
                machine_to_update.user_name = str(current_user.name)
            # Commit Changes
            db.session.commit()
            # Returns Changes
            return jsonify(
                {
                    "Public_ID": machine_to_update.public_id,
                    "Floor_ID": machine_to_update.floor_id,
                    "Floor": machine_to_update.floor,
                    "Dorm": machine_to_update.dorm,
                    "Status": machine_to_update.status,
                    "Last_Service_Date": machine_to_update.last_service_date,
                    "Installation_Date": machine_to_update.installation_date,
                    "Finish_Time": machine_to_update.finish_time,
                    "User_Name": machine_to_update.user_name,
                }
            )
        except AttributeError:
            abort(404, f"Could not PUT machine with ID: {requested_id}")
    # If no method works, return 400 error
    return abort(400, "No method available to handle that call")


@machine.route(
    "/machine/<string:requested_dorm>/<int:requested_floor>/<int:requested_floor_id>",
    methods=["GET", "PUT"],
)
@token_required
def machine_by_dorm_floor_floor_id(
    current_user, requested_dorm, requested_floor, requested_floor_id
):
    """
    Endpoint for getting machine by dorm, floor, and floorid
    Paramters: Dorm, floor number, and the floor id
    Returns: GET: A json object with information about the specific machine
             PUT: A json object with the updated information about the specific machine
    """
    if request.method == "GET":
        # Get machine ID and Status and return it as a Json Dictionary
        try:
            machine_info = Machine.query.filter_by(
                floor_id=requested_floor_id, floor=requested_floor, dorm=requested_dorm
            ).first()
            return jsonify(
                {
                    "Public_ID": machine_info.public_id,
                    "Status": machine_info.status,
                    "Finish_Time": machine_info.finish_time,
                    "User_Name": machine_info.user_name,
                }
            )
        except AttributeError:
            abort(404, f"Could not GET machine with Floor_ID: {requested_floor_id}")
    if request.method == "PUT":
        # Updates machine status
        status = request.args.get("status")
        if status not in STATUS_LIST:
            abort(400, "Status is not an acceptable status, use: 'Free', 'In_use', 'Broken'")
        try:
            machine_info = Machine.query.filter_by(
                floor_id=requested_floor_id, floor=requested_floor, dorm=requested_dorm
            ).first()
            machine_info.status = status
            # If the status is in_use and a user is provided,
            # then assigns a user and finish_time to the machine
            if status == "In_use" and current_user.name is not None:
                machine_info.finish_time = int(time.time()) + TIMER
                machine_info.user_name = current_user.name
            else:
                machine_info.finish_time = None
            db.session.commit()
            # Returns the changes
            return jsonify(
                {
                    "Public_ID": machine_info.public_id,
                    "Status": machine_info.status,
                    "User_Name": machine_info.user_name,
                    "Finish_Time": machine_info.finish_time,
                }
            )
        except AttributeError:
            abort(404, f"Could not PUT machine with Floor_ID: {requested_floor_id}")
    return abort(400, "No method available to handle that call")


@machine.route(
    "/machine/<string:requested_dorm>/<int:requested_floor>", methods=["GET"]
)
@token_required
def machines_by_dorm_and_floor(current_user, requested_dorm, requested_floor):
    """
    Endpoint for getting machines by dorm and floor
    Parameter: Dorm and Floor number
    Returns: A json object that has a list of machines objects for that floor and dorm
    """
    # Find all machines on the requested floor
    machine_info = Machine.query.filter_by(
        floor=requested_floor, dorm=requested_dorm
    ).all()
    counter = 0
    request_objects = []
    while counter < len(machine_info):
        # Creating a list of dictionaries
        request_return_dicts = {
            "Public_ID": machine_info[counter].public_id,
            "Floor_ID": machine_info[counter].floor_id,
            "Status": machine_info[counter].status,
        }
        request_objects.append(request_return_dicts)
        counter += 1
    return jsonify(request_objects)


@machine.route("/machine/<string:requested_dorm>", methods=["GET"])
@token_required
def machines_by_dorm(current_user, requested_dorm):
    """
    Endpoint for getting machines by dorm
    Parameters: The requested dorm
    Returns: A json object with a list of machines nd their information
    """
    # Find all machines in the requested dorm
    machine_info = Machine.query.filter_by(dorm=requested_dorm).all()
    counter = 0
    request_objects = []
    while counter < len(machine_info):
        # Creating a list of dictionaries
        request_return_dict = {
            "Public_ID": machine_info[counter].public_id,
            "Floor": machine_info[counter].floor,
            "Floor_ID": machine_info[counter].floor_id,
            "Status": machine_info[counter].status,
        }
        request_objects.append(request_return_dict)
        counter += 1
    return jsonify(request_objects)
