from typing import Any
from athena import Athena


class QueryTemplate:

    def fail(cls):
        raise BaseException("method not implemented")

    def getCurrentEventDate(self):
        self.fail()

    def getRiders(self):
        self.fail()

    def getCars(self):
        self.fail()

    def getCurrentEventRide(self):
        self.fail()


class _AthenaQueries(QueryTemplate):

    def getCurrentEventDate(self):
        result = Athena.executeQueryToRows('select event_date from current_event')
        if result is None or len(result) == 0:
            return None
        return result[0]['event_date']

    def getRiders(self, event_date=None):
        if False:
            return Athena.executeQueryToRows(
                "select user_id, time, location, event_date from current_riders order by time, count(*) over (partition by time, location) desc, location, random(), name")
        if event_date is None:
            event_date = self.getCurrentEventDate()
        return Athena.executeQueryToRows("execute current_riders_query using '" + event_date + "', '"  + event_date + "', '"  + event_date + "', '" + event_date + "', '" + event_date + "'")

    def getCars(self, event_date=None):
        if False:
            return Athena.executeQueryToRows("select owner, driver_id, seats, model, parking_spot FROM current_event_drivers order by seats desc, random(), model")
        if event_date is None:
            event_date = self.getCurrentEventDate()
        return Athena.executeQueryToRows("execute current_event_drivers_query using '" + event_date + "', '" + event_date + "', '" + event_date + "', '" + event_date + "', '"  + event_date + "', '" + event_date + "'")

    def getCurrentEventRide(self, event_date=None):
        if False:
            return Athena.executeQueryToRows("select event_date, event_name, time, location, driver_name, car_id, model, seats, parking_spot, rider_name, user_id from current_event_ride order by time, location, model, rider_name")
        if event_date is None:
            event_date = self.getCurrentEventDate()
        return Athena.executeQueryToRows("execute current_event_ride_query using '" + event_date + "'")


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
    def getRiders(cls, event_date=None) -> Any:
        return cls._impl.getRiders(event_date)

    @classmethod
    def getCars(cls, event_date=None) -> Any:
        return cls._impl.getCars(event_date)

    @classmethod
    def getCurrentEventRide(cls, event_date=None) -> Any:
        return cls._impl.getCurrentEventRide(event_date)
