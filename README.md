# WWU-Wash-And-Dry-Backend

Python Flask Application to serve as the backend for WWU Wash and Dry

## Setup

- Install...

## Developer Notes

---

- SSO through Azure AD will expire `4/20/2023` and need to be renewed through by the WWU IT Department
- There is an .env file which contains SSO and App configuration that should NOT be pushed to version control
- The SSO Authorization URL - `https://login.microsoftonline.com/d958f048-e431-4277-9c8d-ebfb75e7aa64/oauth2/v2.0/authorize?client_id=b011ad62-bda8-449f-99d3-519a3d973218&response_type=code&response_mode=query&scope=https://graph.microsoft.com/User.Read`
