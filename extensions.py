from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate

#Initialize Database
db=SQLAlchemy()

#Initialize Mail
mail = Mail()

#Initialize Migrate
migrate = Migrate()