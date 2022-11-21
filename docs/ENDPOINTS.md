# Parameters

Parameters have to follow the exact format and spelling as listed below otherwise
calls will not work.

- Public_id: The machine's ID. No machine will have the same Public_id as another.
- Floor_id: Machine ID for the machines on a single floor. Different ID than Public_id. Each floor will have a machine with Floor_ID 1 for example.
- Floor (Machine): Floor number that the machine is located on. Note Sittner machines are under floor 1 in our database.
- Floor (User): Floor number that is one of the user's preferences. Note Sittner machines are under floor 1 in our database.
- Dorm (User): Dorm name that is one of the user's preferences. Can be either "Sittner", "Foreman", or "Conard".
- Dorm (Machine): Dorm that the machines belong to. Can be either "Sittner", "Foreman", or "Conard".
- Last_service_date: Date the machine was last serviced on. Date must follow this format 10-10-2002
- Installation_date: Date the machine was installed. Date must follow this format 10-10-2002
- Status: Status of the machine. Can either be "Free", "In_use", or "Broken".

# Available Endpoints

> ## **POST** /machine/<Public_id>

Creates a new machine

> **HEADERS**

- **Authorization** : Admin

> **PARAMETERS**

All of these are required to create a machine

- Floor_id
- Dorm
- Floor
- Status
- Last_service_date
- Installation_date

> **Sample URL For Request**

- http://localhost:5000/machine/1?Floor_id=2&Floor=1&Dorm=Foreman&Status=Free&Last_service_date=01-20-2001&Installation_date=01-10-2001

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

> ## **GET** /machine/<Public_id>

Gets a specific machine by that machine's Public_ID

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- None

> **Sample URL For Request**

- http://localhost:5000/machine/1

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

> ## **DELETE** /machine/<Public_id>

- Deletes a Machine

> **HEADERS**

> **Authorization**: Admin

> **PARAMETERS**

- None

> **Sample URL For Request**

- http://localhost:5000/machine/1

> **RESPONSE**

- On success returns a JSON message saying the machine was deleted.
- Example Response:
  "deleted information for machine with ID: 1"

- On failure returns status code 404

> ## **PUT** /machine/<Public_ID>

- Modifies a machine's status
- Sets finish time

> **HEADERS**

- **Authorizations** : From Single Sign On

> **PARAMETERS**

These are parameters are optional

- Floor_id
- Dorm
- Floor
- Status
- Last_service_date
- Installation_date

> **Sample URL For Request**

- http://localhost:5000/machine/1?Floor_id=2&Floor=1&Dorm=Foreman&Status=Free&Last_service_date=01-20-2001&Installation_date=01-10-2001

> **RESPONSE**

- On success returns a JSON object with Public ID, Floor ID, Floor, Dorm, Machine status, Last service date, installation date, Finish time, and User name
- Example response:
  {
  "Public_ID": 1,
  "Floor_ID": 1,
  "Floor": 0,
  "Dorm": "Sittner",
  "Status": "free",
  "Last_Service_Date": "10-27-2022",
  "Installation_Date": "10-27-2022",
  "Finish_Time": None,
  "User_Name": Evan,
  }

- On failure due to not finding a machine with the specified public id returns status code 404

> ## **GET** /machine/ < Dorm > / < Floor > / < Floor_id >

- Gets information for one machine on a specified dorm and floor

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- None

> **Sample URL For Request**

- http://localhost:5000/machine/Sittner/1/1

> **RESPONSE**

- On success returns a JSON object for a specific machine with Public ID, Status, Finish time,
  and User name
- Example Response:
  {
  "Public_ID": 1,
  "Status": "In_use"
  "Finish_Time": 10:27
  "User_Name": "Evan"
  }

- On failure due to not finding a machine with the specified information returns status code 404

> ## **PUT** /machine/< Dorm >/< Floor >/< Floor_id >

- Modifies information for one machine on a specified dorm and floor

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

These parameters are optional

- Status

> **Sample URL For Request**

- http://localhost:5000/machine/Sittner/1/1?Status=Free

> **RESPONSE**

- On success returns a JSON object for the modified machine
- Example Response:
  {
  "Public_ID": 1,
  "Status": "In_use"
  "User_Name": "Evan"
  "Finish_Time": "10:27"
  }

- On failure due to not finding a machine with the specified information returns status code 404

> ## **GET** /machine/< Dorm >/< Floor >

- Gets information for all the machines on a floor in a dorm

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- None

> **Sample URL For Request**

- http://localhost:5000/machine/Sittner/1

> **RESPONSE**

- Returns a jsonified list of dicts for machines from the specified dorm and floor.
- Example Response:
  [{"Public_ID": 1, "Floor_ID": 1, "Status": "Free"},
  {"Public_ID": 2, "Floor_ID": 2, "Status": "Free"} ]

> ## **GET** /machine/< Dorm >

- Gets a list of dicts for all the machines in a dorm

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- None

> **Sample URL For Request**

- http://localhost:5000/machine/Sittner

> **RESPONSE**

- Returns a jsonified list of dicts for all machines in a dorm.
- Example Response:
  [{"Public_ID": 1, "Floor": 1, "Floor_ID": 1, "Status": "Free"},
  {"Public_ID": 2, "Floor": 1, "Floor_ID": 2, "Status": "In_use"} ]

> ## **GET** /user/<user_id>

- Gets information about a user

> **HEADERS**

- **Authorization** from Single Sign On

> **PARAMETERS**

- None

> **Sample URL for Request**

- http://localhost:5000/user/1

> **RESPONSE**

- On success returns JSON object that contains the Name, Public_ID, and Email of the requested user
- Example Response:
  {
  "Name": "Hayden",
  "Public_ID": 1,
  "Email": "USER_EMAIL",
  }

- On failure due to not finding a user with the specified user_id returns status code 404

> ## **DELETE** /user/<user_id>

- Deletes a user

> **HEADERS**

- **Authorization** from Single Sign On

> **PARAMETERS**

- None

> **Sample URL For Request**

- http://localhost:5000/user/1

> **RESPONSE**

- On success returns a JSON message that the user was deleted from database
- Example Response: "deleted information for user with ID: 1"

- On failure returns status code 404

> ## **PUT** /user/<user_id>

- Modifies preferance for user
- Not yet fully implemented

> **HEADERS**

- **Authorization** : Bearer {token}

> **PARAMETERS**

- Floor
- Dorm

> **Sample URL For Request**

- http://localhost:5000/user/1

> **RESPONSE**

- _Successfully Changes Preferance for user_
