"""
This file holds the Machine Model
"""

#pylint: disable = R0913, R0903, R0902
#R0913: Too many arguments (6/5) (too-many-arguments)
#R0903: Too few public methods (0/2) (too-few-public-methods)
#R0902: Too many instance attributes (8/7) (too-many-instance-attributes)

from extensions import db

class Machine(db.Model):
    """
    Machine Class
    Init: id, floor_id, dorm, status, last_service_date, installation_date
    """
    __bind_key__ = "machine"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique=True)
    floor_id = db.Column(db.Integer)
    dorm = db.Column(db.String(10))
    floor = db.Column(db.Integer)
    status = db.Column(db.String)
    last_service_date = db.Column(db.String)
    installation_date = db.Column(db.String)
    finish_time = db.Column(db.Integer)
    user_name = db.Column(db.String(100))

    def __init__(
        self,
        public_id,
        floor_id,
        dorm,
        floor,
        installation_date
    ):
        self.public_id = public_id
        self.floor_id = floor_id
        self.dorm = dorm
        self.floor = floor
        self.status = "Free"
        self.installation_date = installation_date
