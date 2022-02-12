import json
from datetime import datetime

class Person:
    def __init__(self, user_id = None, name = None, time = None, location = None):
        self.user_id = user_id
        self.name = name
        self.time = time
        self.location = location

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return self.toJson()

    @classmethod
    def asPerson(cls, jsonString):
        person = cls()
        person.__dict__ = json.loads(jsonString)
        return person

class Car:
    def __init__(self, owner = None, seats = None, model = None, parking_spot = None):
        self.owner = owner
        self.seats = seats
        self.model = model
        self.parking_spot = parking_spot

    def pk(self):
        return 'Car/' + self.owner

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return self.toJson()

    @classmethod
    def asCar(cls, jsonString):
        car = cls()
        car.__dict__ = json.loads(jsonString)
        return car

    @classmethod
    def newCar(cls, data):
        car = cls()
        car.owner = data['user_id']
        return car


class Event:
    def __init__(self, event_date=None, name=None):
        self.event_date = event_date
        self.name = name

    def pk(self):
        return 'Event/' + self.event_date

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return self.toJson()

    @classmethod
    def asEvent(cls, jsonString):
        event = cls()
        event.__dict__ = json.loads(jsonString)
        return event

    @classmethod
    def newEvent(cls):
        event = cls()
        return event


    def setEventDate(self, date):
        try:
            tmp = datetime.strptime(date, '%m/%d/%Y')
            self.event_date = tmp.strftime('%Y-%m-%d')
            return None
        except BaseException as err:
            return str(err)


class EventOptOut:
    def __init__(self, event_date=None, user_id=None):
        self.event_date = event_date
        self.user_id = user_id

    def pk(self):
        return 'EventOptOut/' + self.event_date + '/' + self.user_id

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return self.toJson()

    @classmethod
    def asEventOptOut(cls, jsonString):
        obj = cls()
        obj.__dict__ = json.loads(jsonString)
        return obj

    @classmethod
    def newEventOptOut(cls, data):
        obj = cls()
        obj.user_id = data['user_id']
        return obj




