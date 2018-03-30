# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from twilio.rest import Client
from config import *

# Find these values at https://twilio.com/user/account

client = Client(ACCOUNT_SID, AUTH_TOKEN)

client.api.account.messages.create(
    to="+12063713726",
    from_="+14252797386",
    body="This Twilio thing is so cool! ~Vienna")
