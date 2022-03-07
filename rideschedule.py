import json


class RideSchedule:
    def __init__(self, event_date=None, guest_rides=None, guest_time_offset=None):
        self.event_date = event_date
        if guest_rides is not None:
            self.guest_rides = int(guest_rides)
        if guest_time_offset is not None:
            self.guest_time_offset = int(guest_time_offset)
        self._schedule = None

    def toJson(self):
        stra = []
        for row in self._schedule:
            row_str = json.dumps(self, default=lambda o: row)
            stra.append(row_str)
        return '\n'.join(stra)

    @classmethod
    def asRideSchedule(cls, jsonString: str):
        obj = cls()
        obj._schedule = []
        for row in jsonString.split('\n'):
            obj._schedule.append(json.loads(row))
        if len(obj._schedule) > 0:
            obj.event_date = obj._schedule[0]['event_date']
        return obj

    def __str__(self):
        return self.toJson()

    def pk(self):
        return "EventRide/" + self.event_date + '/' + 'RideSchedule.ndjson'

    def addGuest(self, location: str, rider_description: str):
        for row in self._schedule:
            if int(row['time']) > 1000:
                if row['location'] == 'Open':
                    prefix = row['user_id'].split(' ')[0]
                    row['location'] = location
                    row['user_id'] = prefix + ' ' + rider_description
                    return row
        return None

    def removeGuest(self, rider_index: str):
        for row in self._schedule:
            if int(row['time']) > 1000:
                if row['location'] != 'Open':
                    prefix = row['user_id'].split(' ')[0]
                    if prefix == '[' + rider_index.strip() + ']':
                        row['location'] = 'Open'
                        row['user_id'] = prefix
                        return row
        return None

    def editGuest(self, rider_index: str, location: str, rider_description: str):
        for row in self._schedule:
            if int(row['time']) > 1000:
                if row['location'] != 'Open':
                    prefix = row['user_id'].split(' ')[0]
                    if prefix == '[' + rider_index.strip() + ']':
                        row['location'] = location
                        row['user_id'] = prefix + ' ' + rider_description
                        return row
        return None

    def setRiders(self, riders):
        self.riders = riders

    def setCars(self, cars):
        self.cars = cars

    def computeSchedule(self):
        candidate_rider = CandidateRiders()
        for rider in self.riders:
            candidate_rider.addRider(rider)

        # Find the minimum and maximum candidate, then range from the min to 1+ the max
        candidate_times = []
        for time in candidate_rider.getTimes():
            candidate_times.append(int(time))
        candidate_times.sort()
        all_times = []
        all_times += range(candidate_times[0], candidate_times[-1] + 1)

        # Add the guest range
        starting_guest_time = self.guest_time_offset + 1
        all_times += range(starting_guest_time, starting_guest_time + self.guest_rides)
        all_times.sort()

        # Convert back to strings
        string_times = []
        for time in all_times:
            string_times.append(str(time))
        car_master = CarMaster(string_times, self.cars, self.guest_time_offset)
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
    def __init__(self, times, cars, guest_offset):
        self.car_time_struct = {}
        self.driver_ids = {}
        self.user_ids = set()
        self.guest_offset = int(guest_offset)
        for current_car in cars:
            self.driver_ids[current_car['driver_id']] = {'car_id': current_car['owner'], 'used': False}
        for current_time in times:
            self.car_time_struct[current_time] = {}
        for current_time in times:
            car_struct = self.car_time_struct[current_time]
            car_index = 0
            for current_car in cars:
                car_index += 1
                cabin = {'driver_id': current_car['driver_id'], 'seats': int(current_car['seats']), 'riders': [],
                         'preferred_location': None}
                car_struct[current_car['owner']] = cabin
                # Handle Guest Initialization Here; current_time > guest_offset
                # Change seats to 1, and assign a placeholder rider.
                guest_index = int(current_time) - self.guest_offset
                if guest_index > 0 and len(cabin['riders']) == 0:
                    cabin['seats'] = 1
                    guest_id = "[" + str(guest_index) + ":" + str(car_index) + "]"
                    cabin['preferred_location'] = 'Open'
                    cabin['riders'].append([guest_id, cabin['preferred_location']])

    def __str__(self):
        return str(self.car_time_struct)

    def results(self, event_date):
        result = []
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

        return result

    def offerRider(self, user_id, location, time, preferred_car_id):

        # Skip drivers
        if user_id in self.driver_ids:
            return True

        # Skip already seen user_id
        if user_id in self.user_ids:
            return True

        car_struct = self.car_time_struct[time]

        # Handle guest edits
        if int(time) > self.guest_offset:
            if preferred_car_id in car_struct:
                car_id = preferred_car_id
            else:
                return False
            car = car_struct[car_id]
            car['riders'] = [[user_id, location]]
            car['preferred_location'] = location
            self.user_ids.add(user_id)
            return True

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
