from app import app, User, db, Machine, send_email
import pytest
import json

#Test Parameters for User
user_test_id = 1
user_test_name = "Hayden"
user_test_public_ID =1
user_test_email = "Walla Walla"

#Test Parameters for Machine
machine_test_id = 1
machine_test_floorId= 1
machine_test_dorm = "Sittner"
machine_test_floor = 0
machine_test_isAvailable = True
machine_test_lastServiceDate = "10/27/2022"
machine_test_installationDate = "10/27/2022"

#Test Parameters for Emails
recipients=['WWU-Wash-And-Dry@outlook.com']
body='Testing email'
subject='Testing'

#This pytest fixture allows us to update database within our test file. 
@pytest.fixture ()
def app_context():
    with app.app_context():
        yield

def test_send_email(app_context):
    response=send_email(True, subject, body, recipients)
    assert json.loads(response.data)==['Email was successfully sent',200]

def test_email_failure(app_context):
    response=send_email(True, subject, body, [])
    assert json.loads(response.data)==['Could not send email.', 400]

def test_unprotected_route():
    response = app.test_client().get('/unprotected')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'No Token No problem!'
 
def test_getUser(app_context):
    #create test user
    newUser = User(user_test_id, user_test_public_ID, user_test_name, user_test_email)
    db.session.add(newUser)
    db.session.commit()
    #send request 
    response=app.test_client().get(f'/user/{user_test_public_ID}')
    #remove created user
    User.query.filter_by(public_id=user_test_public_ID).delete()
    db.session.commit()
    #test response
    assert response.status_code==200
    assert response.data.decode('utf-8')=='[\"Hayden\",\"1\",\"Walla Walla\"]\n'

def test_deleteUser(app_context):
    newUser = User(user_test_id, user_test_public_ID, user_test_name, user_test_email)
    db.session.add(newUser)
    db.session.commit()
    response=app.test_client().delete(f'/user/{user_test_public_ID}')
    assert response.status_code==200
    assert response.data.decode('utf-8')==f'deleted information for user with ID: {user_test_public_ID}'

def test_getMachineById(app_context):
    newMachine = Machine(machine_test_id, machine_test_floorId, machine_test_dorm, machine_test_floor, machine_test_isAvailable, machine_test_lastServiceDate, machine_test_installationDate)
    db.session.add(newMachine)
    db.session.commit()
    response=app.test_client().get(f'/machine/{machine_test_id}')
    Machine.query.filter_by(id = machine_test_id).delete()
    db.session.commit()
    assert response.status_code == 200
    assert response.data.decode('utf-8')=='[1,1,0,\"Sittner\",true,\"10/27/2022\",\"10/27/2022\"]\n'

def test_deleteMachineById(app_context):
    newMachine = Machine(machine_test_id, machine_test_floorId, machine_test_dorm, machine_test_floor, machine_test_isAvailable, machine_test_lastServiceDate, machine_test_installationDate)
    db.session.add(newMachine)
    db.session.commit()
    response=app.test_client().delete(f'/machine/{machine_test_id}')
    Machine.query.filter_by(id = machine_test_id).delete()
    assert response.status_code==200
    assert response.data.decode('utf-8')==f'deleted information for machine with ID: {machine_test_id}'

def test_createMachineById(app_context):
    response = app.test_client().post(f'/machine/{machine_test_id}', query_string = {'floor_id': machine_test_floorId, 'dorm': machine_test_dorm, 'floor':machine_test_floor, 'is_available': machine_test_isAvailable, 'last_service_date':machine_test_lastServiceDate, 'installation_date': machine_test_installationDate})
    Machine.query.filter_by(id = machine_test_id).delete()
    db.session.commit()
    assert response.status_code==200
    assert response.data.decode('utf-8')==f'created information for machine with ID: {machine_test_id}'

def test_getMachineByDormFloorFloorID(app_context):
    newMachine = Machine(machine_test_id, machine_test_floorId, machine_test_dorm, machine_test_floor, machine_test_isAvailable, machine_test_lastServiceDate, machine_test_installationDate)
    db.session.add(newMachine)
    db.session.commit()
    response = app.test_client().get(f'/machine/{machine_test_dorm}/{machine_test_floor}/{machine_test_floorId}')
    Machine.query.filter_by(id = machine_test_id).delete()
    db.session.commit()
    assert response.status_code == 200
    assert response.data.decode('utf-8')=='[1,true]\n'

def test_getMachinesByDormFloor(app_context):
    test_id = [1, 2, 3]
    test_floorId= [1, 2, 3]
    newMachine0 = Machine(test_id[0], test_floorId[0], machine_test_dorm, machine_test_floor, machine_test_isAvailable, machine_test_lastServiceDate, machine_test_installationDate)
    newMachine1 = Machine(test_id[1], test_floorId[1], machine_test_dorm, machine_test_floor, machine_test_isAvailable, machine_test_lastServiceDate, machine_test_installationDate)
    newMachine2 = Machine(test_id[2], test_floorId[2], machine_test_dorm, machine_test_floor, machine_test_isAvailable, machine_test_lastServiceDate, machine_test_installationDate)
    db.session.add(newMachine0)
    db.session.add(newMachine1)
    db.session.add(newMachine2)
    db.session.commit()
    response = app.test_client().get(f'/machine/{machine_test_dorm}/{machine_test_floor}')
    Machine.query.filter_by(id = test_id[0]).delete()
    Machine.query.filter_by(id = test_id[1]).delete()
    Machine.query.filter_by(id = test_id[2]).delete()
    db.session.commit()
    assert response.status_code == 200
    assert response.data.decode('utf-8')=='[[1,1,true],[2,2,true],[3,3,true]]\n'

def test_getMachinesByDorm(app_context):
    test_id = [1, 2, 3]
    test_floorId= [1, 2, 3]
    test_floor = [1, 2, 3]
    newMachine0 = Machine(test_id[0], test_floorId[0], machine_test_dorm, test_floor[0], machine_test_isAvailable, machine_test_lastServiceDate, machine_test_installationDate)
    newMachine1 = Machine(test_id[1], test_floorId[1], machine_test_dorm, test_floor[1], machine_test_isAvailable, machine_test_lastServiceDate, machine_test_installationDate)
    newMachine2 = Machine(test_id[2], test_floorId[2], machine_test_dorm, test_floor[2], machine_test_isAvailable, machine_test_lastServiceDate, machine_test_installationDate)
    db.session.add(newMachine0)
    db.session.add(newMachine1)
    db.session.add(newMachine2)
    db.session.commit()
    response = app.test_client().get(f'/machine/{machine_test_dorm}')
    Machine.query.filter_by(id = test_id[0]).delete()
    Machine.query.filter_by(id = test_id[1]).delete()
    Machine.query.filter_by(id = test_id[2]).delete()
    db.session.commit()
    assert response.status_code == 200
    assert response.data.decode('utf-8')=='[[1,1,1,true],[2,2,2,true],[3,3,3,true]]\n'
