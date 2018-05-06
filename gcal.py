"""
GCal is a class that directly handles all API functions with Google Calendar,
 from authentication to event creation. All items passed out of GCal are in our
 own Event object format for increased usability for our functions. In essence,
 this class makes it so other classes do not have to deal with any of the
 intricacies of the API.
"""

from __future__ import print_function
import httplib2
import os

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import time
import datetime
import pytz
import preferenceScoring
import scheduleHelpers
from pprint import pprint


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
    def __init__(self, mainID = "primary", timeZone = 'America/Los_Angeles'):
        """
        mainID is the id of the calendar that events are pulled from and created into
        All users of google calendar have a default calendar with the id of "primary"
        timeZone is a string that gets passed into the body of some API calls for event creation
        """
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http= self.http)
        self.now = datetime.datetime.utcnow()
        self.mainID = mainID
        self.tempID = None
        self.timeZone = timeZone

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

    def create_RRULE(freq = 'WEEKLY', days = "", interval = 1):
        rule = "FREQ=" + freq
        if (days != ""):
            rule.append("BYDAY=" + days)
        rule.append("INTERVAL=" + interval)

    def create_event(self, name ="event", location ='', description ='',
                    start=datetime.datetime.utcnow() + datetime.timedelta(days = 1),
                     end=datetime.datetime.utcnow() + datetime.timedelta(days=2), repeat='FREQ=HOURLY;UNTIL=19901212', notification=[]):
        """
        Takes all parameters google can take with easy defaults
        Time is passed as a datetime object in UTC

        pass in repetition as a string in the following format:
        RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=10;WKST=SU;BYDAY=TU,TH
        means every other week for 10 weeks on Tuesday and Thursdays
        use any rules you want to have represented
        with list:
                        ( "FREQ" "=" freq ) (HOURLY,DAILY, WEEKLY, MONTHLY, YEARLY)
                       / ( "UNTIL" "=" enddate )
                       / ( "COUNT" "=" 1*DIGIT ) (how many to create)
                       / ( "INTERVAL" "=" 1*DIGIT ) (ex. 2 would be every other)
                       / ( "BYSECOND" "=" byseclist )
                       / ( "BYMINUTE" "=" byminlist )
                       / ( "BYHOUR" "=" byhrlist )
                       / ( "BYDAY" "=" bywdaylist )
                       / ( "BYMONTHDAY" "=" bymodaylist )
                       / ( "BYYEARDAY" "=" byyrdaylist )
                       / ( "BYWEEKNO" "=" bywknolist )
                       / ( "BYMONTH" "=" bymolist )
                       / ( "BYSETPOS" "=" bysplist )
                       / ( "WKST" "=" weekday )

        notifications take the form of an array:
        [{'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ]
        with possible methods: 'email', 'popup'
        maximum number of notifications is 5
        """
        start_str = start.isoformat() + 'Z'
        end_str = end.isoformat() + 'Z'
        event = {
          'summary': name,
          'location': location,
          'description': description,
          'start': {
            'dateTime': start_str,
          },
          'end': {
            'dateTime': end_str,
          },
           #'recurrence': [
           #repeat
          # ],
           'reminders': {
           'useDefault': False,
           'overrides': notification,
           }

        }

        event = self.service.events().insert(calendarId= self.tempID, body=event).execute()

    def get_busy(self, time_min =  datetime.datetime.utcnow(),
                time_max = ( datetime.datetime.utcnow() + datetime.timedelta(days = 7))):
        offset = time.gmtime().tm_hour - time.localtime().tm_hour

        time1 = datetime.datetime.utcnow()
        time1 = datetime.datetime(time1.year, time1.month, time1.day, 0, 0, 0) + datetime.timedelta(days= 1, hours = offset)
        time2 = (time1 + datetime.timedelta(days = 1))
        """
        returns an array of dateTime tuples that give start and end of busy blocks
        time_min is the start of the search, and time_max is the end (as datetime objects)
        """
        body = {
      "timeMin": time1.isoformat() + 'Z',
      "timeMax": time2.isoformat() + 'Z',
      "items": [
        {
          "id": self.mainID
        }
      ]
    }
        eventsResult = self.service.freebusy().query(body = body).execute()
        return eventsResult

    def get_events(self, daysPast, daysFuture):
        """
        Returns a list of event items, in the form of the Google events object
        """
        # time1 = datetime.datetime.utcnow()
        # time1 = datetime.datetime(time1.year, time1.month, time1.day, 0, 0, 0)
        # time2 = (time1 + datetime.timedelta(days = 1))
        time1 = (datetime.datetime.now() - datetime.timedelta(days = daysPast)).isoformat() + 'Z'
        time2 = (datetime.datetime.now() + datetime.timedelta(days = daysFuture)).isoformat() + 'Z'
        events = self.service.events().list(calendarId=self.mainID, pageToken=None, timeMin = time1, timeMax = time2).execute()
        #events = self.service.events().list(calendarId=self.mainID, pageToken=None, timeMin = time1.isoformat() + 'Z', timeMax = time2.isoformat() + "Z").execute()
        return events

    def make_event_list(self, events):
        """
        Takes a list of Google events and turns it into our (more usable) event type
        """
        list = []
        for event in events["items"]:
            list.append(Item(name = event['summary'], start = event['start']['dateTime'], end = event['end']['dateTime']))
        return list

    def delete_event(self, event):
        """
        takes an event object and deletes it from google calendar
        """
        self.service.events().delete(calendarId='primary', eventId= event['id']).execute()

    def make_temp_cal(self):
        """
        Checks whether a temp calendar exists, and if not, makes one. If a temporary
        calendar exists, it is set as the calendar to add temporary events to.
        """
        if not self.get_tempID(requireID = False):
            data = {'summary': 'Temporary', 'timeZone': 'America/Los_Angeles'}
            temp_cal = self.service.calendars().insert(body=data).execute()
            self.tempID = temp_cal['id']
        else:
            print("A temporary calendar already existed and is now being used.")

    def clear_temp_cal(self):
        """
        Checks if a temporary calendar exists, and if it does, clears it.
        """
        if self.get_tempID(requireID = False):
            self.service.calendars().clear(calendarId = self.tempID).execute()
        else:
            print("No temporary calendar to clear.")

    def delete_temp_cal(self):
        """
        Checks if a temporary calendar exists, and if it does, deletes it.
        """
        if self.get_tempID(requireID = False):
            self.service.calendars().delete(calendarId = self.tempID).execute()
            self.tempID = None
        else:
            print("No temporary calendar to delete.")

    def migrate_events(self):
        """
        Removes each event from the temp calendar and adds it to the main calendar.
        """
        if self.get_tempID(requireID = False):
            events_data = self.service.events().list(calendarId = self.tempID, pageToken=None, timeMin = None, timeMax = None).execute()
            events = events_data['items']
            for event in events:
                # self.service.events().move(calendarId= self.mainID, eventId= event['id'], destination = self.tempID).execute()
                self.service.events().insert(calendarId= self.mainID, body=event).execute()
                self.service.events().delete(calendarId= self.tempID, eventId= event['id']).execute()
        else:
            print("No temporary calendar to migrate events from.")

    def print_cal_data(self):
        """
        Prints all calendars in a google calendar account.
        """
        pprint(self.service.calendarList().list().execute())

    def get_tempID(self, requireID = True):
        """
        Attempts to find a temporary calendar in the user's list of google calendars.
        If none is found, it will make one if requireID is True.
        """
        cal_data = self.service.calendarList().list().execute()
        for n in range(len(cal_data['items'])):
            if cal_data['items'][n]['summary'] == 'Temporary':
                temp_cal_ID = cal_data['items'][n]['id']
                self.tempID = temp_cal_ID
                break
        if requireID and self.tempID == None:
            print("No temporary calendar was found. Creating one for you...")
            self.make_temp_cal()
        return self.tempID

if __name__ == '__main__':
    cal = GCal()
    cal.get_events(0,1)
     # {'method': 'popup', 'minutes': 10}])
    #print(cal.get_busy())
    events = cal.get_events(0,1)
    #events = cal.make_event_list(events
    busy = cal.get_busy()
    print(preferenceScoring.make_cost_matrix(cal,events))
