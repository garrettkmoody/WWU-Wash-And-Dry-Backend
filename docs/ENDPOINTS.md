# Available Endpoints

> ## **GET** /machines

Gets a list of all machines and details about them

> **HEADERS**  

- **Authorization** : Bearer {Token}

> **PARAMETERS**

***NONE***

> **RESPONSE**

>## **GET** /machines/sittner/<floor>

Gets a list of machines and their details by floor in sittner

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- floor
- id???

> **RESPONSE**

Returns a list of machine objects from the sittner dorm

>## **GET** /machines/foreman/<floor>

Gets a list of machines and their details 

> **HEADERS**

 - **Authorization** : User {token}

 > **PARAMETERS**

 - floor
 - id???

 > **RESPONSE**

 Returns a list of machines objects by floor from the foreman dorm

>## **GET** /machine/<id>

Gets a specific machine by that machine's id number

> **HEADERS**

- **Authorization** : User {token}

> **PARAMETERS**

- id

> **RESPONSE**

Returns a specific machine object by id number


