from datetime import datetime
from gcal import GCal

def main():
    cal = GCal
    date = datetime.now()
    print(date.day)
    listOfEvents = cal.get_events()
    print(listOfEvents)


if __name__ == "__main__":
    main()
