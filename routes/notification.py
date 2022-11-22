"""
This file holds the API routes for sending notifications
"""

#pylint: disable = E1101, W0702
#E1101: Instance of '' has no '' member (no-member)
#W0702: No exception type(s) specified (bare-except)

import time
from flask import Blueprint, jsonify, make_response, abort
from flask_mail import Message
from extensions import db, mail
from models.machine import Machine
from models.user import User

notification = Blueprint('notification', __name__)

MSG_BODY = "Yo, go get your laundry"
MSG_SUBJECT = "Laundry is Done"

def send_email(msg_subject, msg_body, msg_recipients):
    """
    Sends an email from WWU-Wash-And-Dry@outlook.com
    Input Arguments:
        testing is a bool that will not send an email to recipients when true
        msg_subject is a string will be the subject of the email
        msg_body is a string that will be the body of the email
        msg_recipients is a list of strings of email addresses that will receive the email
    Returns: a confirmation message with a 200 status code if the email was successful
    and if there was an error it will return an error message with 400 status code
    """
    try:
        email = Message(
            subject=msg_subject,
            body=msg_body,
            sender="WWU-Wash-And-Dry@outlook.com",
            recipients=msg_recipients,
        )
        mail.send(email)
        return jsonify("Email was successfully sent")
    except:
        return make_response("Could not send email.", 400)


@notification.route("/send-notifications")
def send_notifications():
    """
    This method will send an email to the users whose laundry is done
    Input Arguments: None
    Returns: Void
    """
    current_time = int(time.time())
    finished_machines = Machine.query.filter_by(finish_time = current_time).all()
    counter = 0
    while counter < len(finished_machines):
        finished_machines[counter].status = "Free"
        finished_machines[counter].finish_time = None
        try:
            user = User.query.filter_by(name = finished_machines[counter].user_name).first_or_404()
            send_email(MSG_SUBJECT, MSG_BODY, [user.email])
            finished_machines[counter].user_name = None
            db.session.commit()
        except AttributeError:
            abort(404, f"Could not send email to user with name: {user.name}")
        counter+=1
    return jsonify("Notifications sent")
