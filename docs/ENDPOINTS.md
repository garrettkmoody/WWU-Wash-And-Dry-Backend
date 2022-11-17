# Available Endpoints

> ## **POST** /machine

Creates a new machine

> **HEADERS**

- **Authorization** : Admin

> **PARAMETERS**

- public_id
- floor_id
- dorm
- floor
- status
- last_service_date
- installation_date

> **RESPONSE**
- On success returns a JSON message saying that a machine has been created and status code 200
- Example response: 
    "created information for machine with ID: 1"

- On failure due to missing argument returns a JSON message saying that the value is required 
  and status code 400
- Example rsponse:
    "floor_id is required"

- On failure due to a machine already existing with 'requested_id' returns a JSON message saying
  that a machine with that id is already registered and status code 500
- Example response:
    "Machine 1 is already registered"

> ## **GET** /machine/<id>

Gets a specific machine by that machine's Public_ID

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- public_id

> **RESPONSE**

- On success returns a JSON object with the machine information
- Example Return:
{
  "Public_ID": 1,
  "Floor_ID": 1,
  "Floor": 0,
  "Dorm": "Sittner",
  "Status": "free",
  "Last_Service_Date": "10/27/2022",
  "Installation_Date": "10/27/2022",
  "Finish_Time": None,
  "User_Name": Evan,
}

- On failure due to not finding a machine with the specified id returns status code 404

> ## **DELETE** /machine/<id>

- Deletes a Machine

> **HEADERS**

> **Authorization**: Admin

> **PARAMETERS**

- public_id

> **RESPONSE**

- On success returns a JSON message saying the machine was deleted.
- Example Response:
    "deleted information for machine with ID: 1"

- On failure returns status code 404

> ## **PUT** /machine/<id>

- Modifies a machine's status
- Sets finish time

> **HEADERS**

- **Authorizations** : From Single Sign On

> **PARAMETERS**

- public_id
- floor_id
- dorm
- floor
- status
- last_service_date
- installation_date
- finish_time
- user_name

> **RESPONSE**

- On success returns a JSON object with Public ID, Floor ID, Floor, Dorm, Machine status, Last service date, installation date, Finish time, and User name
- Example response:
{
  "Public_ID": 1,
  "Floor_ID": 1,
  "Floor": 0,
  "Dorm": "Sittner",
  "Status": "free",
  "Last_Service_Date": "10/27/2022",
  "Installation_Date": "10/27/2022",
  "Finish_Time": None,
  "User_Name": Evan,
}

- On failure due to not finding a machine with the specified public id returns status code 404

> ## **GET** /machine/dorm/floor/<floor_id>

- Gets information for one machine on a specified dorm and floor

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- dorm
- floor
- floor_id

> **RESPONSE**

- On success returns a JSON object for a specific machine with Public ID, Status, Finish time, 
  and User name
- Example Response:
  {
    "Public_ID": 1, 
    "Status": "in_use"
    "Finish_Time": 10:27
    "User_Name": "Evan"
  }

- On failure due to not finding a machine with the specified information returns status code 404

> ## **PUT** /machine/dorm/floor/<floor_id>

- Modifies information for one machine on a specified dorm and floor

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- dorm
- floor
- floor_id

> **RESPONSE**

- On success returns a JSON object for the modified machine
- Example Response:
{
  "Public_ID": 1, 
  "Status": "in_use"
  "User_Name": "Evan"
  "Finish_Time": "10:27"
}

- On failure due to not finding a machine with the specified information returns status code 404

> ## **GET** /machine/dorm/<floor>

- Gets information for all the machines on a floor in a dorm

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- dorm
- floor

> **RESPONSE**

- Returns a jsonified list of dicts for machines from the specified dorm and floor.
- Example Response:
  [{"Public_ID": 1, "Floor_ID": 1, "Status": "Free"},
  {"Public_ID": 2, "Floor_ID": 2, "Status": "Free"} ]

> ## **GET** /machine/dorm

- Gets a list of dicts for all the machines in a dorm

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- dorm

> **RESPONSE**

- Returns a jsonified list of dicts for all machines in a dorm.
- Example Response:
  [{"Public_ID": 1, "Floor": 1, "Floor_ID": 1, "Status": "Free"},
  {"Public_ID": 2, "Floor": 1, "Floor_ID": 2, "Status": "In use"} ]

> ## **GET** /user

- Gets information about a user

> **HEADERS**

- **Authorization** from Single Sign On

> **PARAMETERS**

- user_id

> **RESPONSE**

- On success returns JSON object that contains the Name, Public_ID, and Email of the requested user
- Example Response:
{
  "Name": "Hayden",
  "Public_ID": 1,
  "Email": "USER_EMAIL",
}

- On failure due to not finding a user with the specified user_id returns status code 404

> ## **DELETE** /user

- Deletes a user

> **HEADERS**

- **Authorization** from Single Sign On

> **PARAMETERS**

- user_id

> **RESPONSE**

- On success returns a JSON message that the user was deleted from database
- Example Response: "deleted information for user with ID: 1"

- On failure returns status code 404

> ## **PUT** /user/<id>

- Modifies preferance for user
- Not yet fully implemented

> **HEADERS**

- **Authorization** : Bearer {token}

> **PARAMETERS**

- preferance ID

> **RESPONSE**

- _Successfully Changes Preferance for user_
