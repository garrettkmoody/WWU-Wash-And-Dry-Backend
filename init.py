"""
File for the initialization of the app
"""

# pylint: disable = W0702, C0103
# W0702: No exception type(s) specified (bare-except)
# C0103: Variable name "MAIL_PASSWORD" doesn't conform to snake_case naming style

import os
from dotenv import load_dotenv
from extensions import db, mail, app
from app.routes.error import (
    error,
    custom_400_errorhandler,
    custom_404_errorhandler,
    custom_500_errorhandler,
)
from app.routes.login import login
from app.routes.machine import machine
from app.routes.notification import notification
from app.routes.token import tokens
from app.routes.user import user
from app.models.machine import Machine

# Include dotenv
load_dotenv()


def configure_app(app_to_configure):
    """
    This function creates an app instance with the proper app
    configurations, mail configurations, registered blueprints,
    and database creation.

    Input Arguments: None
    Returns: App instance
    """

    # App Configurations
    app_to_configure.config.from_mapping(
        SECRET_KEY=str(os.environ.get("SECRET_KEY")),
        SQLALCHEMY_DATABASE_URI="sqlite:///User.db",
        SQLALCHEMY_BINDS={"machine": "sqlite:///Machine.db"},
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        AZURE_OAUTH_TENANCY=str(os.environ.get("TENANT_ID")),
        AZURE_OAUTH_CLIENT_SECRET=str(os.environ.get("CLIENT_SECRET")),
        AZURE_OAUTH_APPLICATION_ID=str(os.environ.get("APPLICATION_ID")),
        ENVIRONMENT=str(os.environ.get("ENVIRONMENT")),
    )

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
        "MAIL_SUPPRESS": True,
    }
    app_to_configure.config.update(mail_settings)

    # Initialize database, mail, and migrate
    db.init_app(app_to_configure)
    mail.init_app(app_to_configure)

    # Register blueprints for routes
    app_to_configure.register_blueprint(error)
    app_to_configure.register_blueprint(login)
    app_to_configure.register_blueprint(machine)
    app_to_configure.register_blueprint(notification)
    app_to_configure.register_blueprint(tokens)
    app_to_configure.register_blueprint(user)

    # Register error routes
    app_to_configure.register_error_handler(400, custom_400_errorhandler)
    app_to_configure.register_error_handler(404, custom_404_errorhandler)
    app_to_configure.register_error_handler(500, custom_500_errorhandler)

    # Return an instance of the app
    return app_to_configure


# pylint: disable =W0621
def populateDb(db):
    """
    Function that initializes our database
    """
    counter = 1
    # Create Machines for Sittner
    for i in range(1, 11):
        newMachine = Machine(counter, i, "Sittner", 1, "09-21-22")
        db.session.add(newMachine)
        counter += 1
    newMachine = Machine(counter, 1, "Foreman", 2, "09-21-22")
    db.session.add(newMachine)
    counter += 1
    # Create Machines for Foreman
    for i in range(3, 8):
        for j in range(1, 3):
            newMachine = Machine(counter, j, "Foreman", i, "09-21-22")
            db.session.add(newMachine)
            counter += 1
    # Create Machines for Conard floor 1
    for i in range(1, 4):
        newMachine = Machine(counter, i, "Conard", 1, "09-21-22")
        db.session.add(newMachine)
        counter += 1
    # Create Machines for the rest of Conard
    for i in range(2, 5):
        newMachine = Machine(counter, 1, "Conard", i, "09-21-22")
        db.session.add(newMachine)
        counter += 1
    db.session.commit()


# Main Driver Function
if __name__ == "__main__":
    app = configure_app(app)
    # Create the database
    with app.app_context():
        db.create_all()
        try:
            populateDb(db)
        except:
            pass
    app.run()
