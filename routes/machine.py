"""
This file holds the API routes for post, get, delete, and put machines
"""

#pylint: disable = C0301, E1101

from email import message
import time
from flask import Blueprint, request, jsonify, abort
from extensions import db
from models.machine import Machine

machine = Blueprint('machine', __name__)

#TODO Implement tests for PUT and failed requests
@machine.route("/machine/<int:requested_id>", methods=["GET", "DELETE", "POST", "PUT"])
def machine_by_id(requested_id):
    """
    Endpoint for getting/posting/deleting a machine by its ID
    Parameter: ID for the machine
    Returns: Post: A confirmation message if it works
             Deletes: A confirmation message that the machine has been deleted
             Get: The machine's information
    """
    if request.method == "POST":
        return_message = None
        # Accepting Parameter Arguments
        floor_id = request.args.get("floor_id")
        dorm = request.args.get("dorm")
        floor = request.args.get("floor", None)
        status = request.args.get("status")
        last_service_date = request.args.get("last_service_date")
        installation_date = request.args.get("installation_date")
        # Checking Parameter Arguments
        if not floor_id:
            return_message = "floor_id is required"
        elif not dorm:
            return_message = "dorm is required"
        elif not floor:
            return_message = "floor is required"
        elif not status:
            return_message = "status is required"
        elif not installation_date:
            return_message = "installation_date is required"
        # Parameter Arguments are valid, attempt to create user
        if return_message is None:
            try:
                new_machine = Machine(
                    requested_id,
                    floor_id,
                    dorm,
                    floor,
                    status,
                    last_service_date,
                    installation_date,
                    None,
                    None
                )
                db.session.add(new_machine)
                db.session.commit()
                return_message = "Created information for machine with ID: " + str(requested_id)
            except db.IntegrityError:
                return_message = "Machine " + str(requested_id) + " is already registered."
        return jsonify(return_message)
    if request.method == "GET":
        #Find the Machine
        machine_info = Machine.query.filter_by(public_id=requested_id).first_or_404()
        #Return as a json dictionary
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
        #Try to delete the machine, if not abort with a 404 error
        delete_request = Machine.query.filter_by(public_id=requested_id).delete()
        db.session.commit()
        if delete_request:
            return jsonify(f"Deleted information for machine with ID: {requested_id}")
        abort(404)
    if request.method == "PUT":
        #Gather request arguments
        floor_id = request.args.get("floor_id", None)
        dorm = request.args.get("dorm", None)
        floor = request.args.get("floor", None)
        status = request.args.get("status", None)
        last_service_date = request.args.get("last_service_date", None)
        installation_date = request.args.get("installation_date", None)
        #Find machine to update
        machine_to_update = Machine.query.filter_by(public_id=requested_id).first_or_404()
        #Update the changes
        if floor_id is not None:
            machine_to_update.floor_id = floor_id
        if dorm is not None:
            machine_to_update.dorm = dorm
        if floor is not None:
            machine_to_update.floor = floor
        if status is not None :
            machine_to_update.status = status
        if installation_date is not None:
            machine_to_update.installation_date = installation_date
        if last_service_date is not None:
            machine_to_update.last_service_date = last_service_date
        #Commit Changes
        db.session.commit()
        #Returns Changes
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
                "User_Name": machine_to_update.user_name
            }
        )
    #If no method works, return 400 error
    abort(400)
    return jsonify("There was an error.")


@machine.route(
    "/machine/<string:requested_dorm>/<int:requested_floor>/<int:requested_floor_id>",
    methods=["GET","PUT"],
)
def machine_by_dorm_floor_floor_id(requested_dorm, requested_floor, requested_floor_id):
    """
    Endpoint for getting machine by dorm, floor, and floorid
    Paramters: Dorm, Floor number, and the floor id
    Returns: A json object with information about the specific machine
    """
    if request.method == "GET":
        #Get machine ID and Status and return it as a Json Dictionary
        machine_info = Machine.query.filter_by(
            floor_id=requested_floor_id, floor=requested_floor, dorm=requested_dorm
        ).first_or_404()
        return jsonify(
            {"Public_ID": machine_info.public_id, 
            "Status": machine_info.status, 
            "Finish_Time": machine_info.finish_time, 
            "User_Name": machine_info.user_name}
        )
    if request.method == "PUT":
        #Updates machine status
        status = request.args.get("status")
        user_name = request.args.get("user_name", None)
        machine_info = Machine.query.filter_by(
            floor_id=requested_floor_id, floor=requested_floor, dorm=requested_dorm
        ).first_or_404()
        machine_info.status  = status
        #If the status is in_use and a user is provided, then assigns a user and finish_time to the machine
        if status == "in_use" and user_name is not None:
            #Sets end time 30 minutes from current time
            #TODO: Try to implement a time.time() method to improve readability
            machine_info.finish_time = int((time.time_ns() + 1.8 * 10 ** 12)/60000000000)
            machine_info.user_name = user_name
        else:
            machine_info.finish_time = None
        db.session.commit()
        #Returns the changes
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
def machines_by_dorm_and_floor(requested_dorm, requested_floor):
    """
    Endpoint for getting machines by dorm and floor
    Parameter: Dorm and Floor number
    Returns: A json object that has a list of machines objects for that floor and dorm
    """
    #Find all machines on the requested floor
    machine_info = Machine.query.filter_by(
        floor=requested_floor, dorm=requested_dorm
    ).all()
    counter = 0
    request_objects = []
    while counter < len(machine_info):
        #Creating a list of dictionaries
        request_return_dicts = {
            "Public_ID": machine_info[counter].public_id,
            "Floor_ID": machine_info[counter].floor_id,
            "Status": machine_info[counter].status,
        }
        request_objects.append(request_return_dicts)
        counter += 1
    return jsonify(request_objects)


@machine.route("/machine/<string:requested_dorm>", methods=["GET"])
def machines_by_dorm(requested_dorm):
    """
    Endpoint for getting machines by dorm
    Parameters: The requested dorm
    Returns: A json object with a list of machines nd their information
    """
    #Find all machines in the requested dorm
    machine_info = Machine.query.filter_by(dorm=requested_dorm).all()
    counter = 0
    request_objects = []
    while counter < len(machine_info):
        #Creating a list of dictionaries
        request_return_dict = {
            "Public_ID": machine_info[counter].public_id,
            "Floor": machine_info[counter].floor,
            "Floor_ID": machine_info[counter].floor_id,
            "Status": machine_info[counter].status,
        }
        request_objects.append(request_return_dict)
        counter += 1
    return jsonify(request_objects)
