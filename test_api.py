from app import app, User, dbUser, Machines, dbMachines
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
    dbUser.session.add(newUser)
    dbUser.session.commit()
    #send request to get information
    response=app.test_client().get(f'/user/{test_public_ID}')
    #get rid of test user from database
    delete_Request=User.query.filter_by(public_id=test_public_ID).delete()
    dbUser.session.commit()
    assert response.status_code==200
    assert response.data.decode('utf-8')=='[\"Hayden\",\"1\",\"Walla Walla\"]\n'


def test_deleteUser(app_context):
    #create test user
    test_name="Hayden"
    test_public_ID=1
    test_email="Walla Walla"
    newUser = User(public_id=test_public_ID, name=test_name, email=test_email)
    dbUser.session.add(newUser)
    dbUser.session.commit()
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
    dbMachines.session.add(newMachine)
    dbMachines.session.commit()
    response=app.test_client().get(f'/machines/{test_id}')
    assert response.status_code == 200
    assert response.data.decode('utf-8')=='[\"1\",\"1\",\"Sittner\",\"0\",\"True\",\"10/27/2022\",\"10/27/2022\"]\n'



