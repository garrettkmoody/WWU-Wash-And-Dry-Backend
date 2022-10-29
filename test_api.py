from pickle import TRUE
from app import app, User, db, Machines
import pytest


def test_unprotected_route():
    response = app.test_client().get('/unprotected')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'No Token No problem!'

#This pytest fixture allows us to update database within our test file. 
@pytest.fixture ()
def app_context():
    with app.app_context():
        yield
        
def test_getUser(app_context):
    #create test user
    test_name="Hayden"
    test_public_ID=1
    test_email="Walla Walla"
    newUser = User(public_id=test_public_ID, name=test_name, email=test_email)
    db.session.add(newUser)
    db.session.commit()
    #send request to get information
    response=app.test_client().get(f'/user/{test_public_ID}')
    #get rid of test user from database
    User.query.filter_by(public_id=test_public_ID).delete()
    db.session.commit()
    assert response.status_code==200
    assert response.data.decode('utf-8')=='[\"Hayden\",\"1\",\"Walla Walla\"]\n'


def test_deleteUser(app_context):
    #create test user
    test_name="Hayden"
    test_public_ID=1
    test_email="Walla Walla"
    newUser = User(public_id=test_public_ID, name=test_name, email=test_email)
    db.session.add(newUser)
    db.session.commit()
    #send delete request
    response=app.test_client().delete(f'/user/{test_public_ID}')
    assert response.status_code==200
    assert response.data.decode('utf-8')==f'deleted information for user with ID: {test_public_ID}'

def test_getMachineById(app_context):
    #create test machine
    test_id = 1
    test_floorId= 1
    test_dorm = "Sittner"
    test_floor = 0
    test_isAvailable = True
    test_lastServiceDate = "10/27/2022"
    test_installationDate = "10/27/2022"
    newMachine = Machines(id = test_id, floor_id = test_floorId, dorm = test_dorm, floor = test_floor, is_available = test_isAvailable, last_service_date = test_lastServiceDate, installation_date = test_installationDate)
    db.session.add(newMachine)
    db.session.commit()
    response=app.test_client().get(f'/machines/{test_id}')
    Machines.query.filter_by(id = test_id).delete()
    db.session.commit()
    assert response.status_code == 200
    assert response.data.decode('utf-8')=='[1,1,0,\"Sittner\",true,\"10/27/2022\",\"10/27/2022\"]\n'

def test_deleteMachineById(app_context):
    test_id = 1
    test_floorId= 1
    test_dorm = "Sittner"
    test_floor = 0
    test_isAvailable = True
    test_lastServiceDate = "10/27/2022"
    test_installationDate = "10/27/2022"
    newMachine = Machines(id = test_id, floor_id = test_floorId, dorm = test_dorm, floor = test_floor, is_available = test_isAvailable, last_service_date = test_lastServiceDate, installation_date = test_installationDate)
    db.session.add(newMachine)
    db.session.commit()
    response=app.test_client().delete(f'/machines/{test_id}')
    Machines.query.filter_by(id = test_id).delete()
    assert response.status_code==200
    assert response.data.decode('utf-8')==f'deleted information for machine with ID: {test_id}'


def test_createMachineById(app_context):
    test_id = 1
    test_floorId= '1'
    test_dorm = "Sittner"
    test_floor = '0'
    test_isAvailable = 'True'
    test_lastServiceDate = "10/27/2022"
    test_installationDate = "10/27/2022"
    response = app.test_client().post(f'/machines/{test_id}', query_string = {'floor_id': test_floorId, 'dorm': test_dorm, 'floor':test_floor, 'is_available': test_isAvailable, 'last_service_date':test_lastServiceDate, 'installation_date': test_installationDate})
    Machines.query.filter_by(id = test_id).delete()
    db.session.commit()
    assert response.status_code==200
    assert response.data.decode('utf-8')==f'created information for machine with ID: {test_id}'

def test_getMachineByDormFloorFloorID(app_context):
    test_id = 1
    test_floorId= 1
    test_dorm = "Sittner"
    test_floor = 0
    test_isAvailable = True
    test_lastServiceDate = "10/27/2022"
    test_installationDate = "10/27/2022"
    newMachine = Machines(id = test_id, floor_id = test_floorId, dorm = test_dorm, floor = test_floor, is_available = test_isAvailable, last_service_date = test_lastServiceDate, installation_date = test_installationDate)
    db.session.add(newMachine)
    db.session.commit()
    response = app.test_client().get(f'/machines/{test_dorm}/{test_floor}/{test_floorId}')
    Machines.query.filter_by(id = test_id).delete()
    db.session.commit()
    assert response.status_code == 200
    assert response.data.decode('utf-8')=='[1,true]\n'

def test_getMachinesByDormFloor(app_context):
    test_id = [1, 2, 3]
    test_floorId= [1, 2, 3]
    test_dorm = "Sittner"
    test_floor = 1
    test_isAvailable = True
    test_lastServiceDate = "10/27/2022"
    test_installationDate = "10/27/2022"
    newMachine = Machines(id = test_id[0], floor_id = test_floorId[0], dorm = test_dorm, floor = test_floor, is_available = test_isAvailable, last_service_date = test_lastServiceDate, installation_date = test_installationDate)
    db.session.add(newMachine)
    db.session.commit()
    newMachine = Machines(id = test_id[1], floor_id = test_floorId[1], dorm = test_dorm, floor = test_floor, is_available = test_isAvailable, last_service_date = test_lastServiceDate, installation_date = test_installationDate)
    db.session.add(newMachine)
    db.session.commit()
    newMachine = Machines(id = test_id[2], floor_id = test_floorId[2], dorm = test_dorm, floor = test_floor, is_available = test_isAvailable, last_service_date = test_lastServiceDate, installation_date = test_installationDate)
    db.session.add(newMachine)
    db.session.commit()
    response = app.test_client().get(f'/machines/{test_dorm}/{test_floor}')
    print(response)
    Machines.query.filter_by(id = test_id[0]).delete()
    db.session.commit()
    Machines.query.filter_by(id = test_id[1]).delete()
    db.session.commit()
    Machines.query.filter_by(id = test_id[2]).delete()
    db.session.commit()
    assert response.status_code == 200
    assert response.data.decode('utf-8')=='[[1,1,true],[2,2,true],[3,3,true]]\n'
    
