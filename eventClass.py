
class Event:
    '''
    Variables:
    name, startTime, endTime,
    date, breakable
    '''
    def __init__(self, name, startTime, endTime, date, breakable):
        self.name=name
        self.startTime=startTime
        self.endTime=endTime
        self.date=date
        self.breakable=breakable
