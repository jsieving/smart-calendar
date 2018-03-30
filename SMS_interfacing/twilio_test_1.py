# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "ACe4bd8ebc5960bb0a8445a872ca603903"
auth_token = "your_auth_token"

client = Client('ACe4bd8ebc5960bb0a8445a872ca603903', 'a46a75ee7b2bd6289a6a5609f86caf94')

client.api.account.messages.create(
    to="+12063713726",
    from_="+14252797386",
    body="This Twilio thing is so cool! ~Vienna")
