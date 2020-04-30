from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACbcbbf914aa3b54a0c02fbb423bd51ee9'
auth_token = 'f2d332b0dfb9684482b437c5a282b16e'
client = Client(account_sid, auth_token)
message = client.messages.create(body='Hi there! We are doing a survey. Can you help us in doing that.',from_='+12195330397',to='+919987680977')


# def sms_ahoy_reply():
#     """Respond to incoming messages with a friendly SMS."""
#     # Start our response
#     resp = MessagingResponse()
#     print(resp)
#     # Add a message
#     resp.message("Ahoy! Thanks so much for your message.")
#
#     return str(resp)


def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'hello':
        resp.message("Hi! How are you?")
    elif body == 'bye':
        resp.message("Goodbye! Have a nice day.ok")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
