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

    def getRiders(self):
        return Athena.executeQueryToRows(
            "select user_id, time, location, event_date from current_riders order by time, count(*) over (partition by time, location) desc, location, name")

    def getCars(self):
        return Athena.executeQueryToRows("select owner, cast(seats as bigint) as seats, model, parking_spot from car order by seats desc, model limit 3")

    def getCurrentEventRide(self):
        return Athena.executeQueryToRows("select event_date, event_name, time, location, car_owner_name as driver_name, car_id, model, rider_name, user_id from current_event_ride order by time, location, model, rider_name")


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
    def getRiders(cls) -> Any:
        return cls._impl.getRiders()

    @classmethod
    def getCars(cls) -> Any:
        return cls._impl.getCars()

    @classmethod
    def getCurrentEventRide(cls) -> Any:
        return cls._impl.getCurrentEventRide()
