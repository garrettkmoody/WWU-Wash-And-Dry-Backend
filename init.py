"""
File for the initialization of the app
"""

#pylint: disable = W0621

import os
from dotenv import load_dotenv
from flask import Flask
from extensions import db, mail, migrate
from routes.error import error
from routes.login import login
from routes.machine import machine
from routes.notification import notification
from routes.token import token
from routes.user import user

#Include dotenv
load_dotenv()


def create_app():
    """
    This function creates an app instance with the proper app
    configurations, mail configurations, registered blueprints,
    and database creation.

    Input Arguments: None
    Returns: App instance
    """

    #Create Flask Application
    app = Flask(__name__)

    #App Configurations
    app.config.from_mapping(
        SECRET_KEY=str(os.environ.get("SECRET_KEY")),
        SQLALCHEMY_DATABASE_URI="sqlite:///User.db",
        SQLALCHEMY_BINDS={"machine": "sqlite:///Machine.db"},
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        AZURE_OAUTH_TENANCY=str(os.environ.get("TENANT_ID")),
        AZURE_OAUTH_CLIENT_SECRET=str(os.environ.get("CLIENT_SECRET")),
        AZURE_OAUTH_APPLICATION_ID=str(os.environ.get("APPLICATION_ID")),
        ENVIRONMENT=str(os.environ.get("ENVIRONMENT")),
    )
    #pylint: disable = C0103, W0702
    try:
        MAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    except:
        MAIL_PASSWORD = os.environ("EMAIL_PASSWORD")

    mail_settings = {
        "MAIL_SERVER": "smtp.office365.com",
        "MAIL_PORT": 587,
        "MAIL_USE_TLS": True,
        "MAIL_USE_SSL": False,
        "MAIL_USERNAME": "WWU-Wash-And-Dry@outlook.com",
        "MAIL_PASSWORD": MAIL_PASSWORD,
    }
    app.config.update(mail_settings)

    #Initialize database, mail, and migrate
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    #Create the database
    with app.app_context():
        db.create_all()

    #Register blueprints for routes
    app.register_blueprint(error)
    app.register_blueprint(login)
    app.register_blueprint(machine)
    app.register_blueprint(notification)
    app.register_blueprint(token)
    app.register_blueprint(user)

    #Return an instance of the app
    return app

#Main Driver Function
if __name__ == "__main__":
    app = create_app()
    app.run()
