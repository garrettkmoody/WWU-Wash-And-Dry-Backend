# WWU-Wash-And-Dry-Backend

A Python Flask Application based on simple REST principles, the WWU Wash and Dry API endpoints return JSON metadata about WWU washing and drying machines.

This Web API also provides access to user related data, like user name, email, and floor and dorm preferences.

The API provides a set of endpoints, each with its own unique path. To access private data through the Web API, such as user information and washing/drying machine data.

## Endpoints

Refer to the endpoints documentation in the docs folder for more information on specific endpoint parameters and returns.


## Setup and Installation

In order to setup the WWU Wash and Dry API you must have Python 3.11.0 installed as well as GIT.

Clone in the WWU Wash and Dry Web API into your repository using:

```sh
git clone https://github.com/garrettkmoody/WWU-Wash-And-Dry-Backend.git
```

In your local repository, open a terminal and install the needed requirements using:

```sh
pip install -r requirements.txt
```

### Hosting the API Locally

To run the API from your local machine, open the repository in a terminal and use the command:

```sh
python init.py
```

### Testing the Web API

To test the API, open the repository in a terminal and use the command:

```sh
pytest
```

To ensure that any changes in a file meets the required style guides, use the command:

```sh
pylint "/path/to/file"
```

## Developer Notes

---

- SSO through Azure AD will expire `4/20/2023` and need to be renewed through by the WWU IT Department
- There is an .env file which contains SSO and App configuration that should NOT be pushed to version control
- The SSO Authorization URL **(TESTING/DEVELOPMENT)** - `https://login.microsoftonline.com/d958f048-e431-4277-9c8d-ebfb75e7aa64/oauth2/v2.0/authorize?client_id=b011ad62-bda8-449f-99d3-519a3d973218&response_type=code&response_mode=query&scope=https://graph.microsoft.com/User.Read&redirect_uri=http://localhost:5000/login/callback`
- The SSO Authorization URL **(PRODUCTION)** - `https://login.microsoftonline.com/d958f048-e431-4277-9c8d-ebfb75e7aa64/oauth2/v2.0/authorize?client_id=b011ad62-bda8-449f-99d3-519a3d973218&response_type=code&response_mode=query&scope=https://graph.microsoft.com/User.Read&redirect_uri=https://172.27.4.142:5000/login/callback`
