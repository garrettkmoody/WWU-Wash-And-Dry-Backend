"""
This file holds the API routes for post, get, delete, and put machines
"""


# pylint: disable = C0301, E1101, R0911, R0912, R0915, W0613
import datetime
import time
from flask import Blueprint, request, jsonify, abort
from extensions import db
from models.machine import Machine
from routes.token import token_required

machine = Blueprint("machine", __name__)


# TO-DO Implement tests for PUT and failed requests
@machine.route("/machine/<int:requested_id>", methods=["GET", "DELETE", "POST", "PUT"])
@token_required
def machine_by_id(current_user, requested_id):
    """
    Endpoint for getting/posting/deleting a machine by its ID
    Parameter: ID for the machine
    Returns: Post: A confirmation message if it works
             Deletes: A confirmation message that the machine has been deleted
             Get: The machine's information
    """
    # Pylint: disable=R0914
    dorm_list = ["Sittner", "Conard", "Foreman"]
    status_list = ["Free", "In_use", "Broken"]
    if request.args:
        # Accepting Parameter Arguments
        floor_id = request.args.get("Floor_id")
        dorm = request.args.get("Dorm")
        floor = request.args.get("Floor")
        status = request.args.get("Status")
        last_service_date = request.args.get("Last_service_date")
        installation_date = request.args.get("Installation_date")
        if current_user is not None:
            user_name = current_user.name
        # Checking Parameter Arguments
        if int(floor_id) < 0 | int(floor_id) > 100:
            abort(400)
        if dorm not in dorm_list:
            abort(400)
        if int(floor) < 0 | int(floor) > 10:
            abort(400)
        if status not in status_list:
            abort(400)
        try:
            datetime.datetime.strptime(installation_date, "%m-%d-%Y")
            datetime.datetime.strptime(last_service_date, "%m-%d-%Y")
        except:
            abort(400)
        # Parameter Arguments are valid, attempt to create user
    if request.method == "POST":
        try:
            new_machine = Machine(
                int(requested_id),
                int(floor_id),
                str(dorm),
                int(floor),
                str(status),
                str(last_service_date),
                str(installation_date),
                0,
                "None",
            )
            db.session.add(new_machine)
            db.session.commit()
            return (
                jsonify(
                    "Created information for machine with ID: " + str(requested_id)
                ),
                200,
            )
        except db.IntegrityError:
            return (
                jsonify("Machine " + str(requested_id) + " is already registered."),
                500,
            )
    if request.method == "GET":
        # Find the Machine
        machine_info = Machine.query.filter_by(public_id=requested_id).first_or_404()
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
    if request.method == "DELETE":
        # Try to delete the machine, if not abort with a 404 error
        delete_request = Machine.query.filter_by(public_id=requested_id).delete()
        db.session.commit()
        if delete_request:
            return jsonify(f"Deleted information for machine with ID: {requested_id}")
        abort(404)
    if request.method == "PUT":
        # Gather request arguments
        # Edit Later
        finish_time = request.args.get("finish_time")
        # Find machine to update
        machine_to_update = Machine.query.filter_by(
            public_id=requested_id
        ).first_or_404()
        # Update the changes
        if floor_id != "None" and floor_id is not None:
            machine_to_update.floor_id = int(floor_id)
        if dorm != "None" and dorm is not None:
            machine_to_update.dorm = str(dorm)
        if floor != "None" and floor is not None:
            machine_to_update.floor = int(floor)
        if status != "None" and status is not None:
            machine_to_update.status = str(status)
        if installation_date != "None" and installation_date is not None:
            machine_to_update.installation_date = str(installation_date)
        if last_service_date != "None" and last_service_date is not None:
            machine_to_update.last_service_date = str(last_service_date)
        # TO-DO: implement that a finish time can not be update without a username
        # And vice versa
        if finish_time != "None" and finish_time is not None:
            machine_to_update.finish_time = int(finish_time)
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
    # If no method works, return 400 error
    abort(400)


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
    Paramters: Dorm, Floor number, and the floor id
    Returns: A json object with information about the specific machine
    """
    status_list = ["Free", "In_use", "Broken"]
    if request.method == "GET":
        # Get machine ID and Status and return it as a Json Dictionary
        machine_info = Machine.query.filter_by(
            floor_id=requested_floor_id, floor=requested_floor, dorm=requested_dorm
        ).first_or_404()
        return jsonify(
            {
                "Public_ID": machine_info.public_id,
                "Status": machine_info.status,
                "Finish_Time": machine_info.finish_time,
                "User_Name": machine_info.user_name,
            }
        )
    if request.method == "PUT":
        # Updates machine status
        status = request.args.get("status")
        if status not in status_list:
            abort(400)
        user_name = current_user.name
        machine_info = Machine.query.filter_by(
            floor_id=requested_floor_id, floor=requested_floor, dorm=requested_dorm
        ).first_or_404()
        machine_info.status = status
        # If the status is in_use and a user is provided, then assigns a user and finish_time to the machine
        if status == "in_use" and user_name is not None:
            # Sets end time 30 minutes from current time
            # TO-DO: Try to implement a time.time() method to improve readability
            machine_info.finish_time = int(
                (time.time_ns() + 1.8 * 10**12) / 60000000000
            )
            machine_info.user_name = user_name
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
    abort(400)


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
