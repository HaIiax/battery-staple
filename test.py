import os
from testqueries import TestQueries
from athena import Athena
from storage import Storage
from queries import Queries, _AthenaQueries
from rideschedule import RideSchedule


if True:
    Queries.setImplementation(TestQueries())
    event_date = Queries.getCurrentEventDate()
    rs = RideSchedule(event_date)
    rs.setCars(Queries.getCars())
    rs.setRiders(Queries.getRiders())
    rs.computeSchedule()