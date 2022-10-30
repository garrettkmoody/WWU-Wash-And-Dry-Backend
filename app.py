import datetime
from functools import wraps
from itertools import count
from math import floor
from flask import Flask, render_template, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import jwt
import os
import requests

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ.get("SECRET_KEY"))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.db'
app.config['SQLALCHEMY_BINDS'] = {'machines' : 'sqlite:///Machine.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['AZURE_OAUTH_TENANCY'] = str(os.environ.get("TENANT_ID"))
app.config['AZURE_OAUTH_CLIENT_SECRET'] = str(os.environ.get("CLIENT_SECRET"))
app.config['AZURE_OAUTH_APPLICATION_ID'] = str(
    os.environ.get("APPLICATION_ID"))

#This might not need to be split
db = SQLAlchemy(app)
db = SQLAlchemy(app)

class User(db.Model):
    #The tablename may be unnecessary 
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)

class Machines(db.Model):
    __bind_key__ = 'machines'
    #Unique id for each machine
    id = db.Column(db.Integer, primary_key=True)
    #An id based on floor
    floor_id = db.Column(db.Integer)
    dorm = db.Column(db.String(10))
    floor = db.Column(db.Integer)
    is_available = db.Column(db.Boolean)
    last_service_date = db.Column(db.String)
    installation_date = db.Column(db.String)

with app.app_context():
    db.create_all()


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
            db.session.add(newUser)
            db.session.commit()
            print("New User Created!")

        token = jwt.encode({'public_id': userData['id'], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
        return redirect("http://www.google.com?token=" + token)
    except:
        return redirect("http://www.google.com?error=AuthFailed")


@app.route('/machines/<int:requested_id>', methods=['GET' , 'DELETE', 'POST'])
def get_machine_by_id(requested_id):
    if request.method == 'POST':
        floor_id= request.args.get('floor_id')
        dorm = request.args.get('dorm')
        floor = request.args.get('floor')
        is_available = request.args.get('is_available')
        last_service_date = request.args.get('last_service_date')
        installation_date = request.args.get('installation_date')
        newMachine = Machines(id = requested_id, floor_id = int(floor_id), dorm = dorm, floor = int(floor), is_available = bool(is_available), last_service_date = last_service_date, installation_date = installation_date)
        db.session.add(newMachine)
        db.session.commit()
        get_request = Machines.query.filter_by(id = requested_id)
        if get_request:
            return f'created information for machine with ID: {requested_id}', 200
        else: 
            return f'could not create information for machine with ID: {requested_id}',404
    elif request.method == 'GET':
        machine_info= Machines.query.filter_by(id = requested_id).first_or_404()
        return [machine_info.id, machine_info.floor_id, machine_info.floor, machine_info.dorm, machine_info.is_available, machine_info.last_service_date, machine_info.installation_date]
    elif request.method == 'DELETE':
        delete_request = Machines.query.filter_by(id = requested_id).delete()
        db.session.commit()
        if delete_request:
            return f'deleted information for machine with ID: {requested_id}', 200
        else: 
            return f'could not find information for machine with ID: {requested_id}',404
    

@app.route('/machines/<string:requested_dorm>/<int:requested_floor>/<int:requested_floor_id>', methods=['GET'])
def get_machine_by_dorm_floor_floorid(requested_dorm, requested_floor, requested_floor_id):
    machine_info = Machines.query.filter_by(floor_id = requested_floor_id, floor = requested_floor, dorm = requested_dorm).first_or_404()
    return [machine_info.id, machine_info.is_available]

@app.route('/machines/<string:requested_dorm>/<int:requested_floor>', methods=['GET'])
def get_machines_by_dorm_and_floor(requested_dorm, requested_floor):
    machine_info = Machines.query.filter_by(floor = requested_floor, dorm = requested_dorm).all()
    x= len(machine_info)
    counter=0
    request_objects = []
    while x!=0:
        request_return_object = []
        request_return_object.append(machine_info[counter].id)
        request_return_object.append(machine_info[counter].floor_id)
        request_return_object.append(machine_info[counter].is_available)
        request_objects.append(request_return_object)
        x-=1
        counter+=1
    return request_objects

@app.route('/machines/<string:requested_dorm>', methods=['GET'])
def get_machines_by_dorm( requested_dorm):
    machine_info = Machines.query.filter_by(dorm = requested_dorm).all()
    x = len(machine_info)
    counter = 0
    request_objects = []
    while x!= 0:
        request_return_object = []
        request_return_object.append(machine_info[counter].id)
        request_return_object.append(machine_info[counter].floor)
        request_return_object.append(machine_info[counter].floor_id)
        request_return_object.append(machine_info[counter].is_available)
        request_objects.append(request_return_object)
        x-=1
        counter +=1
        print(request_objects)
    return request_objects



# Unprotected route, no token required


@app.route('/unprotected')
def unprotected():
    return 'No Token No problem!'

# Protected route, token required


@app.route('/protected')
@token_required
def protected(current_user):
    return 'Hello ' + current_user.name

@app.route('/user/<requested_UserID>',methods=['GET','DELETE'])
def get_user(requested_UserID):
    if request.method=='GET':
        #Filter can be changed later to be more secure
        #First_or_404 will abort if not found and send a 404
        user_info=User.query.filter_by(public_id=requested_UserID).first_or_404()
        return [user_info.name,user_info.public_id,user_info.email]
    elif request.method=='DELETE':
        #Filter can be changed later to be more secure
        delete_Request=User.query.filter_by(public_id=requested_UserID).delete()
        db.session.commit()
        if delete_Request:
            return f'deleted information for user with ID: {requested_UserID}', 200
        else: 
            return f'Could not find information for User with ID: {requested_UserID}',404


# main driver function
if __name__ == '__main__':
    app.run()
