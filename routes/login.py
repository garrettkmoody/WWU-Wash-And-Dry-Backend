"""
This file holds the API routes for SSO login
"""
import datetime
from flask import Blueprint, request, redirect
import requests
import jwt
from extensions import db
from models.user import User

login = Blueprint('login', __name__)

# Callback URI for Azure AD
@login.route("/login/callback")
def callback():
    """
    callback for single sign on
    Returns: A redirect with an auth token or a redirect for auth failed
    """
    if request.args.get("error"):
        return request.args.get("error"), 403
    if not request.args.get("code"):
        return "Sign-in failed, no auth code.", 403

    body = {
        "grant_type": "authorization_code",
        "scope": "https://graph.microsoft.com/User.Read",
        "client_id": app.config["AZURE_OAUTH_APPLICATION_ID"],
        "code": request.args.get("code"),
        "client_secret": app.config["AZURE_OAUTH_CLIENT_SECRET"],
        "redirect_uri": 'http://localhost:5000/login/callback' if app.config["ENVIRONMENT"] == 'testing'
        else 'https://172.27.4.142:5000/login/callback'
    }
    request_data = requests.post(
        url="https://login.microsoftonline.com/d958f048-e431-4277-9c8d-ebfb75e7aa64/oauth2/v2.0/token",
        data=body,
    )
    data = request_data.json()
    try:
        auth_headers = {"Authorization": "Bearer " + data["access_token"]}
        user_response = requests.get(
            url="https://graph.microsoft.com/v1.0/me", headers=auth_headers
        )
        user_data = user_response.json()
        if not User.query.filter_by(public_id=user_data["id"]).first():
            #pylint: disable=E1120
            # Need to work this out
            new_user = User(
                user_data["id"],
                user_data["displayName"],
                user_data["mail"],
            )
            db.session.add(new_user)
            db.session.commit()
            print("New User Created!")

        token = jwt.encode(
            {
                "public_id": user_data["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=45),
            },
            app.config["SECRET_KEY"],
            "HS256",
        )
        print("Authentication Successful!")
        return redirect("https://reece-reklai.github.io/DormitoryWasherAndDryer/?token=" + token)
    except:
        print("Auth failed")
        return redirect("https://reece-reklai.github.io/DormitoryWasherAndDryer/?error=AuthFailed")
