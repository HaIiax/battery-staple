from classes import EventRide
cars = [['Josh',4],['Mike',5]]
current_riders = [[1234567, 1, 'commons', '2022-03-15'],[1234568, 1, 'commons', '2022-03-15']]
for x in current_riders:
    tmp = EventRide.newEventRide()
    tmp.event_date = x[3]
    tmp.user_id = x[0]
    tmp.time = x[1]
    tmp.location = x[2]
    print(tmp)




