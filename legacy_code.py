'''
@app.route("/test_email")
# Remove this endpoint in the future when we implement a way for machines to send emails
def test_email():
    """
    This is an endpoint to test the functionality of the send email function
    Will remove in the future when we implement the notifying users
    Parameters: none
    Returns: A json response from the send email function
    """
    return send_email(
        False, "Test_email endpoint", "Endpoint works", ["WWU-Wash-And-Dry@outlook.com"]
    )
'''
