import json
from datetime import datetime


class Person:
    def __init__(self, user_id=None, name=None, time=None, location=None):
        self.user_id = user_id
        self.name = name
        self.time = time
        self.location = location

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return self.toJson()

    def pk(self):
        return "Person/" + self.user_id

    def setTime(self, time):
        try:
            tmp = int(time)
            if tmp < 1 or tmp > 9:
                return "Pickup time must be between 1 and 9"
            self.time = str(tmp)
            return None
        except BaseException as err:
            return str(err)

    @classmethod
    def asPerson(cls, jsonString):
        person = cls()
        person.__dict__ = json.loads(jsonString)
        return person


class Car:
    def __init__(self, owner=None, seats=None, model=None, parking_spot=None):
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
    def __init__(self, event_date=None, name=None, pickup_time=None, pickup_interval=None, guest_pickup_time=None, guest_pickup_interval=None, guest_rides=None):
        self.event_date = event_date
        self.name = name
        self.pickup_time = pickup_time
        self.pickup_interval = pickup_interval
        self.guest_pickup_time = guest_pickup_time
        self.guest_pickup_interval = guest_pickup_interval
        self.guest_rides = guest_rides

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

    def setPickupTime(self, time):
        try:
            tmp = datetime.strptime(time, '%H:%M')
            self.pickup_time = tmp.strftime('%H:%M')
            return None
        except BaseException as err:
            return str(err)

    def setPickupInterval(self, interval):
        try:
            tmp = int(interval)
            if tmp < 1 or tmp > 90:
                return "Pickup interval must be between 1 and 90 minutes"
            self.pickup_interval = str(tmp)
            return None
        except BaseException as err:
            return str(err)

    def setGuestPickupTime(self, time):
        try:
            tmp = datetime.strptime(time, '%H:%M')
            self.guest_pickup_time = tmp.strftime('%H:%M')
            return None
        except BaseException as err:
            return str(err)

    def setGuestPickupInterval(self, interval):
        try:
            tmp = int(interval)
            if tmp < 1 or tmp > 90:
                return "Guest pickup interval must be between 1 and 90 minutes"
            self.guest_pickup_interval = str(tmp)
            return None
        except BaseException as err:
            return str(err)

    def setGuestRides(self, rides):
        try:
            tmp = int(rides)
            if tmp < 1 or tmp > 9:
                return "Guest rides must be between 1 and 9"
            self.guest_rides = str(tmp)
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


class EventRide:
    def __init__(self, event_date=None, user_id=None, car_id=None, time=None, location=None):
        self.event_date = event_date
        self.user_id = user_id
        self.car_id = car_id
        self.time = time
        self.location = location

    def pk(self):
        return 'EventRide/' + self.event_date + '/' + self.user_id

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return self.toJson()

    @classmethod
    def asEventRide(cls, jsonString):
        event = cls()
        event.__dict__ = json.loads(jsonString)
        return event

    @classmethod
    def newEventRide(cls):
        event = cls()
        return event


class EventDriver:
    def __init__(self, event_date=None, user_id=None):
        self.event_date = event_date
        self.user_id = user_id

    def pk(self):
        return 'EventDriver/' + self.event_date + '/' + self.user_id

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return self.toJson()

    @classmethod
    def asEventDriver(cls, jsonString):
        obj = cls()
        obj.__dict__ = json.loads(jsonString)
        return obj

    @classmethod
    def newEventDriver(cls, data, event_date):
        obj = cls()
        obj.user_id = data['user_id']
        obj.event_date = event_date
        return obj

class EventCar:
    def __init__(self, event_date=None, owner=None):
        self.event_date = event_date
        self.owner = owner

    def pk(self):
        return 'EventCar/' + self.event_date + '/' + self.owner

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return self.toJson()

    @classmethod
    def asEventDriver(cls, jsonString):
        obj = cls()
        obj.__dict__ = json.loads(jsonString)
        return obj

    @classmethod
    def newEventCar(cls, data, event_date):
        obj = cls()
        obj.owner = data['user_id']
        obj.event_date = event_date
        return obj