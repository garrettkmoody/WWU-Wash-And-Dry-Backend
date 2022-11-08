"""
This file is to implement the email notification system
"""

#pylint: disable=W0621,W0702,E1101

import time
from flask import jsonify, make_response
from flask_mail import Mail, Message
from app import app, db, Machine, User

mail = Mail(app)
MSG_SUBJECT = "Laundry Done"
MSG_BODY = "This needs to be implemented"

def send_email(testing, msg_subject, msg_body, msg_recipients):
    """
    Sends an email from WWU-Wash-And-Dry@outlook.com
    Args:
        testing is a bool that will not send an email to recipients when true
        msg_subject is a string will be the subject of the email
        msg_body is a string that will be the body of the email
        msg_recipients is a list of strings of email addresses that will receive the email
    Returns a confirmation message with a 200 status code if the email was successful
    and if there was an error it will return an error message with 400 status code
    """
    try:
        if testing:
            app.config.update({"MAIL_SUPPRESS_SEND": True})
            mail = Mail(app)
        else:
            app.config.update({"MAIL_SUPPRESS_SEND": False})
            mail = Mail(app)
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

def notification_timer():
    """
    This method will provide the timer to call the send_notification method every minute

    Input Arguments: None
    Returns: Void
    """
    while 1:
        send_notifications()
        time.sleep(60)

def send_notifications():
    """
    This method will send an email to the users whose laundry is done

    Input Arguments: None
    Returns: Void
    """
    current_time = int(time.time_ns()/60000000000)
    finished_machines = Machine.query.filter_by(finish_time = current_time).all()
    counter = 0
    while counter < len(finished_machines):
        finished_machines[counter].status = "pick_up_laundry"
        finished_machines[counter].finish_time = None
        user = User.query.filter_by(name = finished_machines[counter].user_name).first_or_404()
        send_email(False, MSG_SUBJECT, MSG_BODY, user.email)
        finished_machines[counter].user_name = None
        db.session.commit()
        counter+=1
