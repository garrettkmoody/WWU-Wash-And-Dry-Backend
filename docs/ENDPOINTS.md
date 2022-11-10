# Available Endpoints

> ## **GET** /machine

- Not yet fully implemented
- Gets a list of all machine and details about them

> **HEADERS**

- **Authorization** : Bearer {Token}

> **PARAMETERS**

- None

> **RESPONSE**

- Returns a list of dicts.

> ## **DELETE** /user

- Deletes a user

> **HEADERS**

- **Authorization** from Single Sign On

> **PARAMETERS**

- **_UserID_**

> **RESPONSE**

- A confirmation message that the user was deleted from database
- Example Response: "deleted information for user with ID: 1"

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
  [{"Public_ID":1,"Floor_ID":1,"Status":"Free"},
  {"Public_ID":2,"Floor_ID":2,"Status":"Free"} ]

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

> **Authorization**

- Admin

> **PARAMETERS**

- Public_ID

> **RESPONSE**

- Sends a confirmation message saying the machine was deleted.
- Example Response:
  "deleted information for machine with ID: 1"

> ## **PUT** /user/<id>

- Modifies preferance for user
- Not yet fully implemented

> **HEADERS**

- **Authorization** : Bearer {token}

> **PARAMETERS**

- preferance ID

> **RESPONSE**

- _Successfully Changes Preferance for user_
