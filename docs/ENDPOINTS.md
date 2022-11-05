# Available Endpoints

> ## **GET** /machine

Gets a list of all machine and details about them

> **HEADERS**

- **Authorization** : Bearer {Token}

> **PARAMETERS**

**_NONE_**

> **RESPONSE**

- Information about machine

> ## **Delete** /user

Deletes a user

> **HEADERS**

- **Authorization** from Single Sign On

> **PARAMETERS**

- **_UserID_**

> **RESPONSE**

- _Successfully deleted user_

> ## **GET** /user

Gets information about a user

> **HEADERS**

- **Authorization** from Single Sign On

> **PARAMETERS**

- **_UserID_**

> **RESPONSE**

- _Returns information about the User_

> ## **GET** /machine/sittner/<floor>

Gets a list of machine and their details by floor in sittner

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- floor
- ID???

> **RESPONSE**

Returns a list of machine objects from the sittner dorm

> ## **GET** /machine/foreman/<floor>

Gets a list of machine and their details

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- floor
- ID???

> **RESPONSE**

Returns a list of machine objects by floor from the foreman dorm

> ## **GET** /machine/<id>

Gets a specific machine by that machine's ID number

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- id

> **RESPONSE**

Returns a specific machine object by ID number

## **DELETE** /machine/<id>

Deletes a Machine

> **HEADERS**

- **Authorization** : Admin

> **PARAMETERS**

- ID

> **RESPONSE**

- _Successfully Deleted Machine_

## **Put** /user/<id>

Modifies preferance for user

> **HEADERS**

- **Authorization** : Bearer {token}

> **PARAMETERS**

- preferance ID

> **RESPONSE**

- _Successfully Changes Preferance for user_
