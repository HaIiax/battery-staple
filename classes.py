class Person:
    def __init__(self, user_id, name, time, location):
        self.user_id = user_id
        self.name = name
        self.time = time
        self.location = location



class Car:
    def __init__(self, seats, owner, model, parking_spot):
        self.seats = seats
        self.owner = owner
        self.model = model
        self.parking_spot = parking_spot


class Driver(Car):
    def __init__(self, name):
        self.name = name


class Ride(Driver, Person):
    def __init__(self):


class Event(Ride):
    def __init__(self):