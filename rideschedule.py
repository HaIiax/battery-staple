import json


class RideSchedule:
    def __init__(self, event_date=None):
        self.event_date = event_date
        self._schedule = None

    def toJson(self):
        stra = []
        for row in self._schedule:
            row_str = json.dumps(self, default=lambda o: row)
            stra.append(row_str)
        return '\n'.join(stra)

    def __str__(self):
        return self.toJson()

    def pk(self):
        return "EventRide/" + self.event_date + '/' + 'RideSchedule.ndjson'

    def setRiders(self, riders):
        self.riders = riders

    def setCars(self, cars):
        self.cars = cars

    def computeSchedule(self):
        candidate_rider = CandidateRiders()
        for rider in self.riders:
            candidate_rider.addRider(rider)
        car_master = CarMaster(candidate_rider.getTimes(), self.cars)
        candidate_rider.scheduleRiders(car_master)
        self._schedule = car_master.results(self.event_date)


class CandidateRiders:
    def __init__(self):
        self.time_struct = {}

    def __str__(self):
        return str(self.time_struct)

    def pushRiders(self, previous, current, car_master):
        print("previous: " + str(previous) + '; current: ' + str(current))
        location_rider_struct = self.time_struct[previous]
        for current_location in location_rider_struct:
            location_rider = location_rider_struct[current_location]
            while len(location_rider) > 0:
                rider = location_rider.pop()
                success = car_master.offerRider(
                    rider['user_id'], current_location, current, rider['car_id'])
                if not success:
                    location_rider.append(rider)
                    return False
        return True

    def scheduleRiders(self, car_master):
        previous_time = []
        for current_time in self.getTimes():
            while len(previous_time) > 0:
                print("Pushing")
                success = self.pushRiders(previous_time[0], current_time, car_master)
                if not success:
                    break
                previous_time = previous_time[1:]
            success = self.scheduleTime(current_time, car_master)
            if not success:
                previous_time.append(current_time)

    def scheduleTime(self, current_time, car_master):
        location_rider_struct = self.time_struct[current_time]
        for current_location in location_rider_struct:
            location_rider = location_rider_struct[current_location]
            while len(location_rider) > 0:
                rider = location_rider.pop()
                success = car_master.offerRider(
                    rider['user_id'], current_location, current_time, rider['car_id'])
                if not success:
                    location_rider.append(rider)
                    return False

        return True

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
        current_rider_list.append(
            {'user_id': rider['user_id'], 'driver_id': rider['driver_id'], 'car_id': rider['car_id']})


class CarMaster:
    def __init__(self, times, cars):
        self.car_time_struct = {}
        self.driver_ids = {}
        self.user_ids = set()
        for current_car in cars:
            self.driver_ids[current_car['driver_id']] = {'car_id': current_car['owner'], 'used': False}
        for current_time in times:
            self.car_time_struct[current_time] = {}
        for current_time in times:
            car_struct = self.car_time_struct[current_time]
            for current_car in cars:
                cabin = {'driver_id': current_car['driver_id'], 'seats': int(current_car['seats']), 'riders': [],
                         'preferred_location': None}
                car_struct[current_car['owner']] = cabin

    def __str__(self):
        return str(self.car_time_struct)

    def results(self, event_date):
        result = []
        last_time = None
        for current_time in self.car_time_struct:
            last_time = current_time
            car_time = self.car_time_struct[current_time]
            for car_id in car_time:
                cabin = car_time[car_id]
                riders = cabin['riders']
                driver_id = cabin['driver_id']
                for rider in riders:
                    event_rider = {}
                    event_rider['event_date'] = event_date
                    event_rider['time'] = current_time
                    event_rider['car_id'] = car_id
                    event_rider['driver_id'] = driver_id
                    event_rider['location'] = rider[1]
                    event_rider['user_id'] = rider[0]
                    result.append(event_rider)

        # If we have excess drivers, create a single event_rider with after time and null rider
        if last_time is not None:
            current_time = "> " + last_time
            for driver in self.driver_ids:
                driver_struct = self.driver_ids[driver]
                if not driver_struct['used']:
                    event_rider = {}
                    event_rider['event_date'] = event_date
                    event_rider['time'] = current_time
                    event_rider['car_id'] = driver_struct['car_id']
                    event_rider['driver_id'] = driver
                    event_rider['location'] = 'Guest Locations'
                    event_rider['user_id'] = None
                    result.append(event_rider)

        return result

    def offerRider(self, user_id, location, time, preferred_car_id):

        # Skip drivers
        if user_id in self.driver_ids:
            return True

        # Skip already seen user_id
        if user_id in self.user_ids:
            return True

        car_struct = self.car_time_struct[time]
        # print(car_struct)

        # Fit to specific car_id
        if preferred_car_id in car_struct:
            car_id = preferred_car_id
            car = car_struct[car_id]
            car_seats = car['seats']
            riders = car['riders']
            driver_id = car['driver_id']
            preferred_location = car['preferred_location']
            if preferred_location is None:
                preferred_location = location
                car['preferred_location'] = location
            if location == preferred_location and len(riders) < car_seats:
                # it fits
                riders.append([user_id, location])
                self.driver_ids[driver_id]['used'] = True
                self.user_ids.add(user_id)
                return True

        # Fit one location per time+car
        for car_id in car_struct:
            car = car_struct[car_id]
            car_seats = car['seats']
            riders = car['riders']
            driver_id = car['driver_id']
            preferred_location = car['preferred_location']
            if preferred_location is None:
                preferred_location = location
                car['preferred_location'] = location
            if location == preferred_location and len(riders) < car_seats:
                # it fits
                riders.append([user_id, location])
                self.driver_ids[driver_id]['used'] = True
                self.user_ids.add(user_id)
                return True

        # Multiple pickups
        for car_id in car_struct:
            car = car_struct[car_id]
            car_seats = car['seats']
            riders = car['riders']
            driver_id = car['driver_id']
            if len(riders) < car_seats:
                # it fits
                riders.append([user_id, location])
                self.driver_ids[driver_id]['used'] = True
                self.user_ids.add(user_id)
                return True

        return False
