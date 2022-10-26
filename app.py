import datetime
from functools import wraps
from flask import Flask, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import jwt
import os
import requests

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ.get("SECRET_KEY"))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.dbUser'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['AZURE_OAUTH_TENANCY'] = str(os.environ.get("TENANT_ID"))
app.config['AZURE_OAUTH_CLIENT_SECRET'] = str(os.environ.get("CLIENT_SECRET"))
app.config['AZURE_OAUTH_APPLICATION_ID'] = str(
    os.environ.get("APPLICATION_ID"))
dbUser = SQLAlchemy(app)
dbMachines = SQLAlchemy(app)

class User(dbUser.Model):
    id = dbUser.Column(dbUser.Integer, primary_key=True)
    public_id = dbUser.Column(dbUser.String(50), unique=True)
    name = dbUser.Column(dbUser.String(100))
    email = dbUser.Column(dbUser.String(70), unique=True)

class Machine(dbMachines.Model):
    id = dbMachines.Column(dbMachines.Integer, primary_key=True)
    public_id = dbMachines.Column(dbMachines.String(50), unique=True)
    dorm = dbMachines.Column(dbMachines.String(10))
    floor = dbMachines.Column(dbMachines.Integer)
    is_available = dbMachines.Column(dbMachines.Boolean)
    last_service_date = dbMachines.Column(dbMachines.Integer)
    installation_date = dbMachines.Column(dbMachines.Integer)

with app.app_context():
    dbUser.create_all()
# Token Function Decorator


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'access_token' in request.headers:
            token = request.headers['access_token']

        if not token:
            return jsonify({'message': 'Missing Authentication Token!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Invalid Authentication Token!'}), 401

        return f(current_user, *args, **kwargs)
    return decorator

# Callback URI for Azure AD


@app.route("/login/callback")
def callback():
    if request.args.get("error"):
        return request.args.get("error"), 403
    if not request.args.get("code"):
        return "Sign-in failed, no auth code.", 403

    body = {'grant_type': 'authorization_code',
            'scope': 'https://graph.microsoft.com/User.Read',
            'client_id': app.config['AZURE_OAUTH_APPLICATION_ID'],
            'code': request.args.get("code"),
            'client_secret': app.config['AZURE_OAUTH_CLIENT_SECRET']}

    r = requests.post(
        url='https://login.microsoftonline.com/d958f048-e431-4277-9c8d-ebfb75e7aa64/oauth2/v2.0/token', data=body)
    data = r.json()


    try:
        authHeaders = {
            'Authorization': 'Bearer ' + data['access_token']
        }
        userResponse = requests.get(url='https://graph.microsoft.com/v1.0/me', headers=authHeaders)
        userData = userResponse.json()
        if not User.query.filter_by(public_id=userData['id']).first():
            newUser = User(public_id=userData['id'], name=userData['displayName'], email=userData['mail'])
            dbUser.session.add(newUser)
            dbUser.session.commit()
            print("New User Created!")

        token = jwt.encode({'public_id': userData['id'], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
        return redirect("http://www.google.com?token=" + token)
    except:
        return redirect("http://www.google.com?error=AuthFailed")


# Unprotected route, no token required


@app.route('/unprotected')
def unprotected():
    return 'No Token No problem!'

# Protected route, token required


@app.route('/protected')
@token_required
def protected(current_user):
    return 'Hello ' + current_user.name


# main driver function
if __name__ == '__main__':
    app.run()
