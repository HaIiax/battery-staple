#!/usr/bin/env python3

import os, time, random
from testqueries import TestQueries
from athena import Athena
from storage import Storage
from queries import Queries
from rideschedule import RideSchedule
from rideschedulepublisher import RideSchedulePublisher
from classes import Person, Car, Event, EventDriver, EventCar, EventOptOut

s = Storage()

generate=True

if False:
    e=Event()
    print(e.setEventDate('3/19/2022'))
    e.name='A Sunday in March Madness'
    print(e.setPickupTime("8:00"))
    print(e.setPickupInterval("15"))
    print(e.setGuestPickupTime("9:30"))
    print(e.setGuestPickupInterval("20"))
    print(e.setGuestRides("3"))
    print(e)
    s.upsert(e)

def configEventDate():
    #Queries.setImplementation(TestQueries())
    return Queries.getCurrentEventDate()

if True:
    event = Queries.getCurrentEvent()
    event_date = event['event_date']
    print(event_date)

def testCompute() -> RideSchedule:
    rs = RideSchedule(event_date, event['guest_rides'], 1000)
    rs.setCars(Queries.getCars(event_date))
    rs.setRiders(Queries.getRiders(event_date))
    rs.computeSchedule()
    return rs

if False:
    event_date = configEventDate()
    drivers = Athena.executeQueryToRows("select user_id from person order by random() limit 4")
    print(event_date)
    for driver in drivers:
        user_id = driver['user_id']
        print (user_id)
        ed = EventDriver(event_date, user_id)
        print(ed)
        s.upsert(ed)

if False:
    event_date = configEventDate()
    cars = Athena.executeQueryToRows("select owner from car order by seats desc, random() limit 5")
    print(event_date)
    for car in cars:
        owner = car['owner']
        print (owner)
        ec = EventCar(event_date, owner)
        print(ec)
        s.upsert(ec)

if False:
    event_date = configEventDate()
    opt_outs = Athena.executeQueryToRows("select user_id from person order by random() limit 4")
    print(event_date)
    for opt_out in opt_outs:
        user_id = opt_out['user_id']
        print (user_id)
        eoo = EventOptOut(event_date, user_id)
        print(eoo)
        s.upsert(eoo)


if False:
    event_date = configEventDate()
    print(event_date)
    s.remove(EventDriver(event_date, '16960'))
    s.upsert(EventDriver(event_date, '14320'))

if False:
    # Persist person test data
    tq=TestQueries()
    for rider in tq.getRiders():
        p=Person()
        p.user_id=rider['user_id']
        p.name=rider['name']
        if random.randint(1, 10) % 3:
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

if generate:
    rs = testCompute()

if generate:
    s.upsert(rs)

if False:
    lt = time.localtime()
    rs_json = s.get(RideSchedule(event_date).pk())
    rs = RideSchedule.asRideSchedule(rs_json)
    assignment = rs.addGuest('Haverford Villas ' + str(int(time.time() % 30)), 'Sue Jones ' + str(lt.tm_min) + ':' + str(lt.tm_sec) + ' (484-555-1212)')
    if assignment is not None:
        rsp=RideSchedulePublisher(
            event['event_date'], 
            event['pickup_time'], 
            event['pickup_interval'],
            event['guest_pickup_time'], 
            event['guest_pickup_interval'],
            1000)

        print (assignment)
        pickup_hhmm = rsp.toFormattedTime(assignment['time'])
        print (pickup_hhmm)

        s.upsert(rs)
    else:
        print ("No more guest rides available")

if False:
    rs_json = s.get(RideSchedule(event_date).pk())
    rs = RideSchedule.asRideSchedule(rs_json)
    assignment = rs.removeGuest('2:1')
    print (assignment)
    if assignment is not None:
        s.upsert(rs)
    else:
        print ("No such guest")

if False:
    rs_json = s.get(RideSchedule(event_date).pk())
    rs = RideSchedule.asRideSchedule(rs_json)
    assignment = rs.editGuest('1:2', 'Randor Hunt', 'Clair Smith (610-555-1212)')
    print (assignment)
    if assignment is not None:
        s.upsert(rs)
    else:
        print ("No such guest")

if True:
    print(Queries.getExcessDriverCount(event_date))

if generate:
    rsp=RideSchedulePublisher(
        event['event_date'], 
        event['pickup_time'], 
        event['pickup_interval'],
        event['guest_pickup_time'], 
        event['guest_pickup_interval'],
        1000)
    print(s.putAsHtml("html/" + event_date + "/ride-index/index.html", rsp.asHTML()))
