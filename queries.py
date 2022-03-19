from typing import Any
from athena import Athena


class QueryTemplate:

    def fail(cls):
        raise BaseException("method not implemented")

    def getCurrentEventDate(self):
        self.fail()

    def getCurrentEvent(self):
        self.fail()

    def getRiders(self):
        self.fail()

    def getCars(self):
        self.fail()

    def getCurrentEventRide(self):
        self.fail()

    def getExcessDriverCount(self):
        self.fail()


class _AthenaQueries(QueryTemplate):

    def getCurrentEventDate(self):
        result = Athena.executeQueryToRows('select event_date from current_event')
        if result is None or len(result) == 0:
            return None
        return result[0]['event_date']

    def getCurrentEvent(self):
        result = Athena.executeQueryToRows('select event_date, pickup_time, pickup_interval, guest_pickup_time, guest_pickup_interval, guest_rides from current_event')
        if result is None or len(result) == 0:
            return None
        return result[0]

    def getRiders(self, event_date=None):
        if False:
            return Athena.executeQueryToRows(
                "select user_id, time, location, event_date from current_riders order by time, count(*) over (partition by time, location) desc, location, random(), name")
        if event_date is None:
            event_date = self.getCurrentEventDate()
        return Athena.executeQueryToRows("execute current_riders_query using '{dt}', '{dt}', '{dt}', '{dt}', '{dt}', '{dt}', '{dt}'".format(dt=event_date))

    def getCars(self, event_date=None):
        if False:
            return Athena.executeQueryToRows("select owner, driver_id, seats, model, parking_spot FROM current_event_drivers order by seats desc, random(), model")
        if event_date is None:
            event_date = self.getCurrentEventDate()
        return Athena.executeQueryToRows("execute current_event_drivers_query using '{dt}', '{dt}', '{dt}', '{dt}', '{dt}', '{dt}', '{dt}', '{dt}'".format(dt=event_date))

    def getCurrentEventRide(self, event_date=None):
        if False:
            return Athena.executeQueryToRows("select event_date, event_name, time, location, driver_name, car_id, model, seats, parking_spot, rider_name, user_id from current_event_ride order by time, location, model, rider_name")
        if event_date is None:
            event_date = self.getCurrentEventDate()
        return Athena.executeQueryToRows("execute current_event_ride_query using '{dt}'".format(dt=event_date))

    def getExcessDriverCount(self, event_date):
        return int(Athena.executeQueryToRows("execute excess_driver_query using '{dt}', '{dt}'".format(dt=event_date))[0]['excess_driver_count'])


class Queries:
    # default to using Athena
    _impl: QueryTemplate = _AthenaQueries()

    @classmethod
    def setImplementation(cls, impl: QueryTemplate):
        cls._impl = impl

    @classmethod
    def getCurrentEventDate(cls) -> Any:
        return cls._impl.getCurrentEventDate()

    @classmethod
    def getCurrentEvent(cls) -> Any:
        return cls._impl.getCurrentEvent()

    @classmethod
    def getRiders(cls, event_date=None) -> Any:
        return cls._impl.getRiders(event_date)

    @classmethod
    def getCars(cls, event_date=None) -> Any:
        return cls._impl.getCars(event_date)

    @classmethod
    def getCurrentEventRide(cls, event_date=None) -> Any:
        return cls._impl.getCurrentEventRide(event_date)

    @classmethod
    def getExcessDriverCount(cls, event_date=None) -> Any:
        return cls._impl.getExcessDriverCount(event_date)
