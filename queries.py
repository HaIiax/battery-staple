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


class _AthenaQueries(QueryTemplate):

    def getCurrentEventDate(self):
        result = Athena.executeQueryToRows('select event_date from current_event')
        if result is None or len(result) == 0:
            return None
        return result[0]['event_date']

    def getRiders(self):
        return Athena.executeQueryToRows(
            "select user_id, name, time, location, event_date, event_name from current_riders order by name")

    def getCars(self):
        return Athena.executeQueryToRows("select owner, seats, model, parking_spot from car")


class Queries:
    # default to using Athena
    _impl: QueryTemplate = _AthenaQueries()

    @classmethod
    def setImplementation(cls, impl: QueryTemplate):
        cls._impl = impl

    @classmethod
    def getCurrentEventDate(cls):
        return cls._impl.getCurrentEventDate()

    @classmethod
    def getRiders(cls):
        return cls._impl.getRiders()

    @classmethod
    def getCars(cls):
        return cls._impl.getCars()
