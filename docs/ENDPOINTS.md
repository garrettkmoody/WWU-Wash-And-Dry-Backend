# Available Endpoints

>## **POST** /machine

Creates a new machine

> **HEADERS**

- **Authorization** : Admin

> **PARAMETERS**

- requested_id
- floor_id
- dorm
- floor
- status
- last_service_date
- installation_date

> **RESPONSE**

- Returns a message saying that a machine has been created
- Example response: 
    "created information for machine with ID: 1"

> ## **GET** /machine/<id>

Gets a specific machine by that machine's Public_ID

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- Machine's Public_ID

> **RESPONSE**

- Returns a dict with the machine information
- Example Return:
  {"Public_ID": 1,
  "Floor_ID": 1,
  "Floor": 0,
  "Dorm": "Sittner",
  "Status": "free",
  "Last_Service_Date": "10/27/2022",
  "Installation_Date": "10/27/2022",
  "Finish_Time": None,
  "User_Name": None,
  }

> ## **DELETE** /machine/<id>

- Deletes a Machine

> **HEADERS**

> **Authorization**: Admin

> **PARAMETERS**

- Public_ID

> **RESPONSE**

- Sends a confirmation message saying the machine was deleted.
- Example Response:
  "deleted information for machine with ID: 1"

> ## **GET** /machine/dorm/floor/<floor_id>

- Gets a list of dicts for one machine on a specified dorm and floor

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- dorm
- floor
- floor_id

> **RESPONSE**

- Returns a list of dicts for a specific machine
- Example Response:
  {
    "Public_ID": 1, "Status": "in_use"
  }

>## **PUT** /machine/<id>

- Modifies a machine's status
- Sets finish time

> **HEADERS**

- **Authorizations** : From Single Sign On

> **PARAMETERS**

- dorm
- floor
- floor_id

> **RESPONSE**

Currently returns a dict with Public ID, machine status, user name, and finish time
Example response:
  {
    "Public_ID": 1,
    "Status": "in_use",
    "User_Name": "Evan",
    "Finish_Time": 10:02,
  }

  > ## **GET** /machine/dorm/<floor>

- Gets a list of dicts for all the machines on a floor in a dorm

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- dorm
- floor

> **RESPONSE**

- Returns a list of dicts for machines from the sittner dorm.
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

- Returns a list of dicts for machines in the Sittner dorm.
- Example Response:
  [{"Public_ID": 1, "Floor": 1, "Floor_ID": 1, "Status": "Free"},
  {"Public_ID": 2, "Floor": 1, "Floor_ID": 2, "Status": "In use"} ]

> ## **GET** /user

- Gets information about a user

> **HEADERS**

- **Authorization** from Single Sign On

> **PARAMETERS**

- **_UserID_**

> **RESPONSE**

- Returns a dict that contains the Name, Public_ID, and Email of the requested user
- Example Response:
  {
  "Name": "Hayden",
  "Public_ID": 1,
  "Email": "USER_EMAIL",
  }

> ## **DELETE** /user

- Deletes a user

> **HEADERS**

- **Authorization** from Single Sign On

> **PARAMETERS**

- **_UserID_**

> **RESPONSE**

- A confirmation message that the user was deleted from database
- Example Response: "deleted information for user with ID: 1"

> ## **PUT** /user/<id>

- Modifies preferance for user
- Not yet fully implemented

> **HEADERS**

- **Authorization** : Bearer {token}

> **PARAMETERS**

- preferance ID

> **RESPONSE**

- _Successfully Changes Preferance for user_

> ## **GET** /machine

- Not yet fully implemented
- Gets a list of all machine and details about them

> **HEADERS**

- **Authorization** : Bearer {Token}

> **PARAMETERS**

- requested_id

> **RESPONSE**

- Returns a list of dicts with the machine's information.
- Example response:
  {
    "Public_ID": 1,
    "Floor_ID": 1,
    "Floor": 1,
    "Dorm": "Sittner",
    "Status": "in_use",
    "Last_Service_Date": 11/10/2022,
    "Installation_Date": 10/10/2022,
    "Finish_Time": 10:02,
    "User_Name": "Evan",
  }
