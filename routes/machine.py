"""
This file holds the API routes for post, get, delete, and put machines
"""

#pylint: disable = C0301, E1101

import time
from flask import Blueprint, request, jsonify, flash, abort
from extensions import db
from models.machine import Machine
from routes.token import token_required

machine = Blueprint('machine', __name__)

@machine.route("/machine/<int:requested_id>", methods=["GET", "DELETE", "POST"])
@token_required
def machine_by_id(current_user, requested_id):
    """
    Endpoint for getting/posting/deleting a machine by its ID
    Parameter: ID for the machine
    Returns: Post: A confirmation message if it works
             Deletes: A confirmation message that the machine has been deleted
             Get: The machine's information
    """
    if request.method == "POST":
        # Accepting Parameter Arguments
        floor_id = request.args.get("floor_id")
        dorm = request.args.get("dorm")
        floor = request.args.get("floor", None)
        status = request.args.get("status")
        last_service_date = request.args.get("last_service_date")
        installation_date = request.args.get("installation_date")
        error = None
        # Checking Parameter Arguments
        if not floor_id:
            error = "floor_id is required"
        elif not dorm:
            error = "dorm is required"
        elif not floor:
            error = "floor is required"
        elif not status:
            error = "status is required"
        elif not installation_date:
            error = "installation_date is required"
        # Parameter Arguments are valid, attempt to create user
        if error is None:
            try:
                new_machine = Machine(
                    requested_id,
                    int(floor_id),
                    dorm,
                    int(floor),
                    bool(status),
                    last_service_date,
                    installation_date,
                    None,
                    None
                )
                db.session.add(new_machine)
                db.session.commit()
            except db.IntegrityError:
                error = f"Machine {requested_id} is already registered."
        flash(error)
        return jsonify(f"created information for machine with ID: {requested_id}")



    if request.method == "GET":
        machine_info = Machine.query.filter_by(public_id=requested_id).first_or_404()
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
                "User_Name": machine_info.user_name
            }
        )
    if request.method == "DELETE":
        delete_request = Machine.query.filter_by(public_id=requested_id).delete()
        db.session.commit()
        if delete_request:
            return jsonify(f"deleted information for machine with ID: {requested_id}")
        abort(404)
    abort(400)
    return jsonify("There was an error.")


@machine.route(
    "/machine/<string:requested_dorm>/<int:requested_floor>/<int:requested_floor_id>",
    methods=["GET","PUT"],
)
@token_required
def machine_by_dorm_floor_floor_id(current_user, requested_dorm, requested_floor, requested_floor_id):
    """
    Endpoint for getting machine by dorm, floor, and floorid
    Paramters: Dorm, Floor number, and the floor id
    Returns: A json object with information about the specific machine
    """
    if request.method == "GET":
        machine_info = Machine.query.filter_by(
            floor_id=requested_floor_id, floor=requested_floor, dorm=requested_dorm
        ).first_or_404()
        return jsonify(
            {"Public_ID": machine_info.public_id, "Status": machine_info.status}
        )
    if request.method == "PUT":
        status = request.args.get("status")
        user_name = request.args.get("user_name")
        machine_info = Machine.query.filter_by(
            floor_id=requested_floor_id, floor=requested_floor, dorm=requested_dorm
        ).first_or_404()
        machine_info.status  = status
        if status == "in_use":
            #Sets end time 30 minutes from current time
            machine_info.finish_time = int((time.time_ns() + 1.8 * 10 ** 12)/60000000000)
            machine_info.user_name = user_name
        else:
            machine_info.finish_time = None
        return jsonify(
            {
                "Public_ID": machine_info.public_id,
                "Status": machine_info.status,
                "User_Name": machine_info.user_name,
                "Finish_Time": machine_info.finish_time,
            }
        )
    abort(400)
    return jsonify("There was an error.")


@machine.route("/machine/<string:requested_dorm>/<int:requested_floor>", methods=["GET"])
@token_required
def machines_by_dorm_and_floor(current_user, requested_dorm, requested_floor):
    """
    Endpoint for getting machines by dorm and floor
    Parameter: Dorm and Floor number
    Returns: A json object that has a list of machines objects for that floor and dorm
    """
    machine_info = Machine.query.filter_by(
        floor=requested_floor, dorm=requested_dorm
    ).all()
    machine_info_length = len(machine_info)
    counter = 0
    request_objects = []
    while machine_info_length != 0:
        request_return_dicts = {
            "Public_ID": machine_info[counter].public_id,
            "Floor_ID": machine_info[counter].floor_id,
            "Status": machine_info[counter].status,
        }
        request_objects.append(request_return_dicts)
        machine_info_length -= 1
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
    machine_info = Machine.query.filter_by(dorm=requested_dorm).all()
    machine_info_length = len(machine_info)
    counter = 0
    request_objects = []
    while machine_info_length != 0:
        request_return_dict = {
            "Public_ID": machine_info[counter].public_id,
            "Floor": machine_info[counter].floor,
            "Floor_ID": machine_info[counter].floor_id,
            "Status": machine_info[counter].status,
        }
        request_objects.append(request_return_dict)
        machine_info_length -= 1
        counter += 1
    return jsonify(request_objects)
