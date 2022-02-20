import json

class RideSchedule:
    def __init__(self, event_date=None) -> None:
        self.event_date = event_date
        self._schedule = None

    def toJson(self):
        return json.dumps(self, default=lambda o: o._schedule)  # not correct?

    def __str__(self):
        return self.toJson()

    def pk(self):
        return "EventRide/" + self.event_date

    def setRiders(self, riders):
        self.riders = riders

    def setCars(self, cars):
        self.cars = cars

    def computeSchedule(self):
        candidate_rider = CandidateRiders()
        for rider in self.riders:
            candidate_rider.addRider(rider)
        car_master = CarMaster(candidate_rider.getTimes(), self.cars)
        candidate_rider.setCarMaster(car_master)
        candidate_rider.scheduleRiders()
        self._schedule = car_master.results(self.event_date)

class CandidateRiders:
    def __init__(self):
        self.time_struct = {}
        self.car_master = None

    def __str__(self):
        return str(self.time_struct)

    def pushRiders(self, previous, current):
        print("previous: " + str(previous) + '; current: ' + str(current))
        location_rider_struct = self.time_struct[previous]
        for current_location in location_rider_struct:
            location_rider = location_rider_struct[current_location]
            while len(location_rider) > 0:
                rider = location_rider.pop()
                success = self.car_master.offerRider(rider, current_location, current)
                if not success:
                    location_rider.append(rider)
                    return False
        return True

    def scheduleRiders(self):
        previous_time = []
        for current_time in self.getTimes():
            while len(previous_time) > 0:
                print("Pushing")
                success = self.pushRiders(previous_time[0], current_time)
                if not success:
                    break
                previous_time = previous_time[1:]
            success = self.scheduleTime(current_time)
            if not success:
                previous_time.append(current_time)

    def scheduleTime(self, current_time):
        location_rider_struct = self.time_struct[current_time]
        for current_location in location_rider_struct:
            location_rider = location_rider_struct[current_location]
            while len(location_rider) > 0:
                rider = location_rider.pop()
                success = self.car_master.offerRider(rider, current_location, current_time)
                if not success:
                    location_rider.append(rider)
                    return False

        return True



    def setCarMaster(self, car_master):
        self.car_master = car_master

    def getTimes(self):
        return self.time_struct.keys()

    def addRider(self, rider):
        rider_time = rider['time']
        current_time_struct = {}
        if rider_time not in self.time_struct:
            self.time_struct[rider_time] = current_time_struct
        else:
            current_time_struct = self.time_struct[rider_time]
        rider_location = rider['location']
        current_rider_list = []
        if rider_location not in current_time_struct:
            current_time_struct[rider_location] = current_rider_list
        else:
            current_rider_list = current_time_struct[rider_location]
        current_rider_list.append(rider['user_id'])


class CarMaster:
    def __init__(self, times, cars):
        self.car_time_struct = {}
        for current_time in times:
            self.car_time_struct[current_time] = {}
        for current_time in times:
            car_struct = self.car_time_struct[current_time]
            for current_car in cars:
                cabin = {'seats': int(current_car['seats']), 'riders': []}
                car_struct[current_car['owner']] = cabin


    def __str__(self):
        return str(self.car_time_struct)

    def results(self, event_date):
        result = []
        for current_time in self.car_time_struct:
            car_time = self.car_time_struct[current_time]
            for car_id in car_time:
                cabin = car_time[car_id]
                riders = cabin['riders']
                for rider in riders:
                    event_rider = {}
                    event_rider['event_date'] = event_date
                    event_rider['time'] = current_time
                    event_rider['car_id'] = car_id
                    event_rider['location'] = rider[1]
                    event_rider['user_id'] = rider[0]
                    result.append(event_rider)
        return result

    def offerRider(self, user_id, location, time):
        car_struct = self.car_time_struct[time]
        # print(car_struct)
        for car_id in car_struct:
            car = car_struct[car_id]
            car_seats = car['seats']
            riders = car['riders']
            if len(riders) < car_seats:
                # it fits
                riders.append([user_id, location])
                return True
        return False






