import datetime
import os
from functools import wraps
import jwt
import requests

from dotenv import load_dotenv
from flask import Flask, redirect, request, jsonify, flash, abort, make_response
from flask_mail import Mail, Message
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
mail = Mail(app)
db = SQLAlchemy(app)


def send_email(testing, msg_subject, msg_body, msg_recipients):
    """
    Sends an email from WWU-Wash-And-Dry@outlook.com
    Args:
        testing is a bool that will not send an email to recipients when true
        msg_subject is a string will be the subject of the email
        msg_body is a string that will be the body of the email
        msg_recipients is a list of strings of email addresses that will receive the email
    Returns a confirmation message with a 200 status code if the email was successful
    and if there was an error it will return an error message with 400 status code
    """
    try:
        if testing:
            app.config.update({"MAIL_SUPPRESS_SEND": True})
            mail = Mail(app)
        else:
            app.config.update({"MAIL_SUPPRESS_SEND": False})
            mail = Mail(app)
        email = Message(
            subject=msg_subject,
            body=msg_body,
            sender="WWU-Wash-And-Dry@outlook.com",
            recipients=msg_recipients,
        )
        mail.send(email)
        return jsonify("Email was successfully sent")
    except:
        return make_response("Could not send email.", 400)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)

    def __init__(self, id, public_id, name, email):
        self.id = id
        self.public_id = public_id
        self.name = name
        self.email = email


class Machine(db.Model):
    __bind_key__ = "machine"
    id = db.Column(db.Integer, primary_key=True)
    floor_id = db.Column(db.Integer)
    dorm = db.Column(db.String(10))
    floor = db.Column(db.Integer)
    is_available = db.Column(db.Boolean)
    last_service_date = db.Column(db.String)
    installation_date = db.Column(db.String)

    def __init__(
        self,
        id,
        floor_id,
        dorm,
        floor,
        is_available,
        last_sevice_date,
        installation_date,
    ):
        self.id = id
        self.floor_id = floor_id
        self.dorm = dorm
        self.floor = floor
        self.is_available = is_available
        self.last_service_date = last_sevice_date
        self.installation_date = installation_date


with app.app_context():
    db.create_all()


# Token Function Decorator
def token_required(f):
    @wraps(f)
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

        return f(current_user, *args, **kwargs)

    return decorator


# Callback URI for Azure AD
@app.route("/login/callback")
def callback():
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
    }

    r = requests.post(
        url="https://login.microsoftonline.com/d958f048-e431-4277-9c8d-ebfb75e7aa64/oauth2/v2.0/token",
        data=body,
    )
    data = r.json()

    try:
        authHeaders = {"Authorization": "Bearer " + data["access_token"]}
        userResponse = requests.get(
            url="https://graph.microsoft.com/v1.0/me", headers=authHeaders
        )
        userData = userResponse.json()
        if not User.query.filter_by(public_id=userData["id"]).first():
            newUser = User(
                public_id=userData["id"],
                name=userData["displayName"],
                email=userData["mail"],
            )
            db.session.add(newUser)
            db.session.commit()
            print("New User Created!")

        token = jwt.encode(
            {
                "public_id": userData["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=45),
            },
            app.config["SECRET_KEY"],
            "HS256",
        )
        return redirect("http://www.google.com?token=" + token)
    except:
        return redirect("http://www.google.com?error=AuthFailed")


@app.route("/machine/<int:requested_id>", methods=["GET", "DELETE", "POST"])
def machine_by_id(requested_id):
    if request.method == "POST":
        # Accepting Parameter Arguments
        floor_id = request.args.get("floor_id")
        dorm = request.args.get("dorm")
        floor = request.args.get("floor", None)
        is_available = request.args.get("is_available")
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
        elif not is_available:
            error = "is_available is required"
        elif not installation_date:
            error = "installation_date is required"
        # Parameter Arguments are valid, attempt to create user
        if error is None:
            try:
                newMachine = Machine(
                    requested_id,
                    int(floor_id),
                    dorm,
                    int(floor),
                    bool(is_available),
                    last_service_date,
                    installation_date,
                )
                db.session.add(newMachine)
                db.session.commit()
            except db.IntegrityError:
                error = f"Machine {requested_id} is already registered."
        flash(error)
        return jsonify(f"created information for machine with ID: {requested_id}")
    elif request.method == "GET":
        machine_info = Machine.query.filter_by(id=requested_id).first_or_404()
        return jsonify(
            {
                "ID": machine_info.id,
                "Floor_ID": machine_info.floor_id,
                "Floor": machine_info.floor,
                "Dorm": machine_info.dorm,
                "Is_Available": machine_info.is_available,
                "Last_Service_Date": machine_info.last_service_date,
                "Installation_Date": machine_info.installation_date,
            }
        )
    elif request.method == "DELETE":
        delete_request = Machine.query.filter_by(id=requested_id).delete()
        db.session.commit()
        if delete_request:
            return jsonify(f"deleted information for machine with ID: {requested_id}")
        else:
            abort(404)


@app.route(
    "/machine/<string:requested_dorm>/<int:requested_floor>/<int:requested_floor_id>",
    methods=["GET"],
)
def machine_by_dorm_floor_floorid(requested_dorm, requested_floor, requested_floor_id):
    machine_info = Machine.query.filter_by(
        floor_id=requested_floor_id, floor=requested_floor, dorm=requested_dorm
    ).first_or_404()
    return jsonify([machine_info.id, machine_info.is_available])


@app.route("/machine/<string:requested_dorm>/<int:requested_floor>", methods=["GET"])
def machines_by_dorm_and_floor(requested_dorm, requested_floor):
    machine_info = Machine.query.filter_by(
        floor=requested_floor, dorm=requested_dorm
    ).all()
    x = len(machine_info)
    counter = 0
    request_objects = []
    while x != 0:
        request_return_object = []
        request_return_object.append(machine_info[counter].id)
        request_return_object.append(machine_info[counter].floor_id)
        request_return_object.append(machine_info[counter].is_available)
        request_objects.append(request_return_object)
        x -= 1
        counter += 1
    return jsonify(request_objects)


@app.route("/machine/<string:requested_dorm>", methods=["GET"])
def machines_by_dorm(requested_dorm):
    machine_info = Machine.query.filter_by(dorm=requested_dorm).all()
    x = len(machine_info)
    counter = 0
    request_objects = []
    while x != 0:
        request_return_object = []
        request_return_object.append(machine_info[counter].id)
        request_return_object.append(machine_info[counter].floor)
        request_return_object.append(machine_info[counter].floor_id)
        request_return_object.append(machine_info[counter].is_available)
        request_objects.append(request_return_object)
        x -= 1
        counter += 1
    return jsonify(request_objects)


@app.route("/test_email")
# Remove this endpoint in the future when we implement a way for machines to send emails
def test_email():
    return send_email(
        False, "Test_email endpoint", "Endpoint works", ["WWU-Wash-And-Dry@outlook.com"]
    )


# Unprotected route, no token required
@app.route("/unprotected")
def unprotected():
    return jsonify("No Token No problem!")


# Protected route, token required
@app.route("/protected")
@token_required
def protected(current_user):
    return jsonify("Hello " + current_user.name)


@app.route("/user/<requested_Public_UserID>", methods=["GET", "DELETE"])
def user_by_id(requested_Public_UserID):
    if request.method == "GET":
        # Filter can be changed later to be more secure
        # First_or_404 will abort if not found and send a 404
        user_info = User.query.filter_by(
            public_id=requested_Public_UserID
        ).first_or_404()
        return jsonify(
            {
                "Name": user_info.name,
                "Public_ID": user_info.public_id,
                "Email": user_info.email,
            }
        )
    elif request.method == "DELETE":
        # Filter can be changed later to be more secure
        delete_Request = User.query.filter_by(
            public_id=requested_Public_UserID
        ).delete()
        db.session.commit()
        if delete_Request:
            return jsonify(
                f"deleted information for user with ID: {requested_Public_UserID}"
            )
        else:
            abort(404)


# not found error
@app.errorhandler(404)
def catch_not_found(e):
    return jsonify("Error 404 not found")


# bad request error
@app.errorhandler(400)
def catch_bad_requests(e):
    return jsonify("Error 400, bad request")


# internal server error
@app.errorhandler(500)
def catch_server_errors(e):
    return jsonify("Error 500, something went wrong with server")


# main driver function
if __name__ == "__main__":
    app.run()
