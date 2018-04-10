import datetime


class Event:
    def __init__(self, name, start = "1", end = '1'):
        self.name = name
        self.start = start
        self.end = end

    def __str__(self):
        return self.name
