'''Created by Jane Sieving (jsieving) on 4/14/18 to avoid screwiness with circular imports.'''

class Item:
    '''An event created with or without scheduling information.
    name: str
    start, end: datetimes
    duration: timedelta
    breakable: boolean
    due: datetime (TBD)
    effort, importance: int 1-4
    category: string
    item_type: str 'todo' or 'event'
    '''
    def __init__(self, name, start = None, end = None, duration = None,\
                breakable = False, importance = None, category = None, item_type = 'event'):
        self.name = name
        self.start = start
        self.end = end
        self.duration = duration
        self.breakable = breakable
        # self.due = due
        self.importance = importance
        self.category = category # may be replaced with tags?
        self.item_type = item_type

    def __str__(self):
        return "%s from %s to %s" % (self.name, self.start.time(), self.end.time())
