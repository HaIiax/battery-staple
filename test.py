import os
from testqueries import TestQueries
from athena import Athena
from storage import Storage
from queries import Queries
from rideschedule import RideSchedule
from rideschedulepublisher import RideSchedulePublisher
from classes import Person, Car, Event

def configEventDate():
    #Queries.setImplementation(TestQueries())
    return Queries.getCurrentEventDate()

def testCompute() -> RideSchedule:
    rs = RideSchedule(configEventDate())
    rs.setCars(Queries.getCars())
    rs.setRiders(Queries.getRiders())
    rs.computeSchedule()
    return rs

if True:
    rs = testCompute()

s = Storage()

if False:
    # Persist person test data
    tq=TestQueries()
    for rider in tq.getRiders():
        p=Person()
        p.user_id=rider['user_id']
        p.name=rider['name']
        p.location=rider['location']
        p.time=rider['time']
        print(p)
        s.upsert(p)

if False:
    # Persist car test data
    tq=TestQueries()
    for d in tq.getCars():
        car=Car()
        car.owner=d['owner']
        car.model=d['model']
        car.seats=d['seats'].strip()
        car.parking_spot=d['parking_spot']
        print(car)
        s.upsert(car)

if False:
    e=Event()
    print(e.setEventDate("2/28/2022"))
    e.name='Tornami a vagheggiar Day'
    print(e)
    s.upsert(e)

if True:
    s.upsert(rs)

if True:
    rsp=RideSchedulePublisher()
    print(s.putAsHtml("event-date/ride-index/index.html", rsp.asHTML()))