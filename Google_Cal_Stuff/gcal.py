from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


class GCal:
    def __init__(self, mainID = "primary", secondID = "testing"):
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http= self.http)
        self.now = datetime.datetime.utcnow()
        self.mainID = mainID
        self.secondID = secondID





    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = Storage(credential_path)
        self.credentials = store.get()
        if not self.credentials or self.credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                self.credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                self.credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return self.credentials

    def create_event(self, name = "event", location = '', description = '', dateTime = datetime.datetime.utcnow() + datetime.timedelta(days = 1)):
        """
        Takes all parameters google can take with easy defaults
        Time is passed as a datetime object in UTC
        """
        dateTime2 = dateTime.isoformat() + 'Z'
        event = {
          'summary': name,
          'location': location,
          'description': description,
          'start': {
            'dateTime': dateTime2,
            'timeZone': 'America/Los_Angeles',
          },
          'end': {
            'dateTime': dateTime2,
            'timeZone': 'America/Los_Angeles',
          },
          'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
          ],
          'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
          ],
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 10},
            ],
          },
        }

        event = self.service.events().insert(calendarId= self.mainID, body=event).execute()

if __name__ == '__main__':
    cal = GCal()
    cal.create_event()
