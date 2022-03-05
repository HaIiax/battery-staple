#!/usr/bin/env python3

import os
from testqueries import TestQueries
from athena import Athena
from storage import Storage
from queries import Queries
from rideschedule import RideSchedule
from rideschedulepublisher import RideSchedulePublisher
from classes import Person, Car, Event, EventDriver

def configEventDate():
    #Queries.setImplementation(TestQueries())
    return Queries.getCurrentEventDate()

if True:
    event_date = configEventDate()
    print(event_date)

def testCompute() -> RideSchedule:
    rs = RideSchedule(event_date)
    rs.setCars(Queries.getCars(event_date))
    rs.setRiders(Queries.getRiders(event_date))
    rs.computeSchedule()
    return rs

s = Storage()

if False:
    e=Event()
    print(e.setEventDate("3/6/2022"))
    e.name='First Sunday in March'
    print(e)
    s.upsert(e)

if False:
    event_date = configEventDate()
    drivers = Athena.executeQueryToRows("select user_id from person order by random() limit 7")
    print(event_date)
    for driver in drivers:
        user_id = driver['user_id']
        print (user_id)
        ed = EventDriver(event_date, user_id)
        print(ed)
        s.upsert(ed)

if True:
    rs = testCompute()

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

if True:
    s.upsert(rs)

if True:
    rsp=RideSchedulePublisher(event_date)
    print(s.putAsHtml(event_date + "/ride-index/index.html", rsp.asHTML()))
