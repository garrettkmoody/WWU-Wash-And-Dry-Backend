#pylint: disable=E1101,W0702,C0301, W3101, W0621, C0114, R0903, R0913, R0902
import datetime
import os
from functools import wraps
import time
import jwt
import requests
from dotenv import load_dotenv
from flask import Flask, redirect, request, jsonify, flash, abort
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=str(os.environ.get("SECRET_KEY")),
    SQLALCHEMY_DATABASE_URI="sqlite:///User.db",
    SQLALCHEMY_BINDS={"machine": "sqlite:///Machine.db"},
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    AZURE_OAUTH_TENANCY=str(os.environ.get("TENANT_ID")),
    AZURE_OAUTH_CLIENT_SECRET=str(os.environ.get("CLIENT_SECRET")),
    AZURE_OAUTH_APPLICATION_ID=str(os.environ.get("APPLICATION_ID")),
    ENVIRONMENT=str(os.environ.get("ENVIRONMENT")),
)
try:
    MAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
except:
    MAIL_PASSWORD = os.environ("EMAIL_PASSWORD")

mail_settings = {
    "MAIL_SERVER": "smtp.office365.com",
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": "WWU-Wash-And-Dry@outlook.com",
    "MAIL_PASSWORD": MAIL_PASSWORD,
}
app.config.update(mail_settings)
db = SQLAlchemy(app)

class User(db.Model):
    """
    User class
    Init: id, public_id, name, and email
    """
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)

    #pylint: disable=C0103, W0622
    def __init__(self, public_id, name, email):
        self.public_id = public_id
        self.name = name
        self.email = email


class Machine(db.Model):
    """
    Machine Class
    Init: id, floor_id, dorm, status, last_service_date, installation_date
    """
    __bind_key__ = "machine"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique=True)
    floor_id = db.Column(db.Integer)
    dorm = db.Column(db.String(10))
    floor = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    last_service_date = db.Column(db.String)
    installation_date = db.Column(db.String)
    finish_time = db.Column(db.Integer)
    user_name = db.Column(db.String(100))
    #pylint: disable=C0103,W0622

    def __init__(
        self,
        public_id,
        floor_id,
        dorm,
        floor,
        status,
        last_sevice_date,
        installation_date,
        finish_time
    ):
        self.public_id = public_id
        self.floor_id = floor_id
        self.dorm = dorm
        self.floor = floor
        self.status = status
        self.last_service_date = last_sevice_date
        self.installation_date = installation_date
        self.finish_time = finish_time


with app.app_context():
    db.create_all()


def token_required(function_decorator):
    """
    Token Function Decorator
    """
    @wraps(function_decorator)
    def decorator(*args, **kwargs):
        token = None
        if "access_token" in request.headers:
            token = request.headers["access_token"]

        if not token:
            return jsonify({"message": "Missing Authentication Token!"}), 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Invalid Authentication Token!"}), 401

        return function_decorator(current_user, *args, **kwargs)

    return decorator


# Callback URI for Azure AD
@app.route("/login/callback")
def callback():
    """
    callback for single sign on
    Returns: A redirect with an auth token or a redirect for auth failed
    """
    if request.args.get("error"):
        return request.args.get("error"), 403
    if not request.args.get("code"):
        return "Sign-in failed, no auth code.", 403

    body = {
        "grant_type": "authorization_code",
        "scope": "https://graph.microsoft.com/User.Read",
        "client_id": app.config["AZURE_OAUTH_APPLICATION_ID"],
        "code": request.args.get("code"),
        "client_secret": app.config["AZURE_OAUTH_CLIENT_SECRET"],
        "redirect_uri": 'http://localhost:5000/login/callback' if app.config["ENVIRONMENT"] == 'testing'
        else 'https://172.27.4.142:5000/login/callback'
    }
    request_data = requests.post(
        url="https://login.microsoftonline.com/d958f048-e431-4277-9c8d-ebfb75e7aa64/oauth2/v2.0/token",
        data=body,
    )
    data = request_data.json()
    try:
        auth_headers = {"Authorization": "Bearer " + data["access_token"]}
        user_response = requests.get(
            url="https://graph.microsoft.com/v1.0/me", headers=auth_headers
        )
        user_data = user_response.json()
        if not User.query.filter_by(public_id=user_data["id"]).first():
            #pylint: disable=E1120
            # Need to work this out
            new_user = User(
                user_data["id"],
                user_data["displayName"],
                user_data["mail"],
            )
            db.session.add(new_user)
            db.session.commit()
            print("New User Created!")

        token = jwt.encode(
            {
                "public_id": user_data["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=45),
            },
            app.config["SECRET_KEY"],
            "HS256",
        )
        return redirect("https://reece-reklai.github.io/DormitoryWasherAndDryer/?token=" + token)
    except:
        return redirect("https://reece-reklai.github.io/DormitoryWasherAndDryer/?error=AuthFailed")

@app.route("/machine/<int:requested_id>", methods=["GET", "DELETE", "POST"])
def machine_by_id(requested_id):
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
        finish_time = request.args.get("finish_time", None)
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
                    finish_time
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


@app.route(
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
        machine_info = Machine.query.filter_by(
            floor_id=requested_floor_id, floor=requested_floor, dorm=requested_dorm
        ).first_or_404()
        return jsonify([machine_info.public_id, machine_info.status])
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
        return jsonify([machine_info.public_id, machine_info.status, machine_info.user_name, machine_info.finish_time])
    abort(400)
    return jsonify("There was an error.")


@app.route("/machine/<string:requested_dorm>/<int:requested_floor>", methods=["GET"])
def machines_by_dorm_and_floor(requested_dorm, requested_floor):
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
        request_return_object = []
        request_return_object.append(machine_info[counter].public_id)
        request_return_object.append(machine_info[counter].floor_id)
        request_return_object.append(machine_info[counter].status)
        request_objects.append(request_return_object)
        machine_info_length -= 1
        counter += 1
    return jsonify(request_objects)


@app.route("/machine/<string:requested_dorm>", methods=["GET"])
def machines_by_dorm(requested_dorm):
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
        request_return_object = []
        request_return_object.append(machine_info[counter].public_id)
        request_return_object.append(machine_info[counter].floor)
        request_return_object.append(machine_info[counter].floor_id)
        request_return_object.append(machine_info[counter].status)
        request_objects.append(request_return_object)
        machine_info_length -= 1
        counter += 1
    return jsonify(request_objects)

# Unprotected route, no token required
@app.route("/unprotected")
def unprotected():
    """
    Unprotected endpoint
    Returns: A confirmation message
    """
    return jsonify("No Token No problem!")


# Protected route, token required
@app.route("/protected")
@token_required
def protected(current_user):
    """
    Protected endpoint
    Parameters: Current user
    Returns: A json message that greets the current user
    """
    return jsonify("Hello " + current_user.name)


@app.route("/user/<requested_user_id>", methods=["GET", "DELETE"])
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

# not found error


@app.errorhandler(404)
def catch_not_found(error):
    """
    Error handler for status code 404 which is not found error

    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 404


# bad request error
@app.errorhandler(400)
def catch_bad_requests(error):
    """
    Error handler for status code 404 which is a bad request
    Parameters: Takes in an error
    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 400


# internal server error
@app.errorhandler(500)
def catch_server_errors(error):
    """
    Error handler for status code 500 which is a server error

    Returns: A json message saying what the error is and the error code
    """
    return jsonify(error=str(error)), 500


# main driver function
if __name__ == "__main__":
    app.run()
