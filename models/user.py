"""
This file holds the User Model
"""

#pylint: disable = R0903

from extensions import db

class User(db.Model):
    """
    User class
    Init: id, public_id, name, and email
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    dorm = db.Column(db.String(10))
    floor = db.Column(db.Integer)

    #pylint: disable=C0103, W0622
    def __init__(self, public_id, name, email):
        self.public_id = public_id
        self.name = name
        self.email = email
        self.dorm = None
        self.floor = None
