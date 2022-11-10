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
    # Create Flask Application
    app = Flask(__name__)

    #Configurations
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

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()


    app.register_blueprint(error)
    app.register_blueprint(login)
    app.register_blueprint(machine)
    app.register_blueprint(notification)
    app.register_blueprint(token)
    app.register_blueprint(user)

    return app

app = create_app()
app.run()