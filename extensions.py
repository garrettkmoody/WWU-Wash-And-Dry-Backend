"""
File to create shared instance of db, mail, and migrate
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

#Create Flask Application
app = Flask(__name__)

#Initialize Database
db=SQLAlchemy()

#Initialize Mail
mail = Mail()
