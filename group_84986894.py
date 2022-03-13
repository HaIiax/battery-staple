from storage import Storage
from classes import Car, Event, EventOptOut, EventDriver, Person
from queries import Queries
from rideschedulepublisher import RideSchedulePublisher
from rideschedule import RideSchedule
from command_security import Security
from helper import Helper


def run(helper: Helper, data, bot_info, send):
    help_message = "Help:\n.help  -->  This screen\n.test  -->  Try it!\nOtherwise, repeats your message."
    storer: Storage = helper.storage
    security: Security = helper.command_security

    person = storer.upsert_person(data)
    print(person)

    message: str = data['text']

    command = message.split(" ")[0]

    if not security.isPermitted(command, person.user_id):
        send("Sorry, not authorized", bot_info[0])
        return True

    if message == '.help':
        send(help_message, bot_info[0])
        return True

    if message == '.test':
        send("Hi there! Your bot is working, you should start customizing it now.", bot_info[0])
        return True

    if message.startswith('.car '):
        car = Car.newCar(data)
        car_parts = message.removeprefix('.car ').split(',')  # add delete remove , seats , model , parking_location

        if car_parts[0].strip()[:1].lower() == 'a':
            if len(car_parts) != 4:
                send("Not enough data. Check to see that there are 3 commas in your command", bot_info[0])
                return True
            car.seats = car_parts[1].strip()
            car.model = car_parts[2].strip()
            car.parking_spot = car_parts[3].strip()
            storer.upsert(car)
            send("added car: " + str(car), bot_info[0])
            return True

        if car_parts[0].strip()[:1].lower() == 'r':
            storer.remove(car)
            send("removed car: " + str(car), bot_info[0])
            return True

        send("Error in format for .car command. Should be '.car add, seats, model, parking_location' OR '.car remove'",
             bot_info[0])
        return True

    if message.startswith('.event '):
        event = Event.newEvent()
        event_parts = message.removeprefix('.event ').split(',')  # add remove, date, name, pickup time, pickup interval, guest_time, guest_interval, guest_rides
        if event_parts[0].strip()[:1].lower() == 'a':
            if len(event_parts) != 8:
                send("Not enough data. Check to see that there are 7 commas in your command", bot_info[0])
                return True
            result = event.setEventDate(event_parts[1].strip())
            if result is not None:
                send("Error in date input." + str(result), bot_info[0])
                return True
            event.name = event_parts[2].strip()
            result = event.setPickupTime(event_parts[3].strip())
            if result is not None:
                send("Error in pickup time." + str(result), bot_info[0])
                return True
            result = event.setPickupInterval(event_parts[4].strip())
            if result is not None:
                send("Error in pickup interval." + str(result), bot_info[0])
                return True
            result = event.setGuestPickupTime(event_parts[5].strip())
            if result is not None:
                send("Error in guest pickup time." + str(result), bot_info[0])
                return True
            result = event.setGuestPickupInterval(event_parts[6].strip())
            if result is not None:
                send("Error in guest pickup interval." + str(result), bot_info[0])
                return True
            result = event.setGuestRides(event_parts[7].strip())
            if result is not None:
                send("Error in guest rides." + str(result), bot_info[0])
                return True
            storer.upsert(event)
            send("Added event: " + str(event), bot_info[0])
            return True

        if event_parts[0].strip()[:1].lower() == 'r':
            if len(event_parts) != 2:
                send("Not enough data. Check to see that there is 1 comma in your command", bot_info[0])
                return True
            result = event.setEventDate(event_parts[1].strip())
            if result is not None:
                send("Error in date input." + str(result), bot_info[0])
                return True
            storer.remove(event)
            send("Removed event: " + str(event), bot_info[0])
            return True

        send(
            "Error in format for .event command. Should be '.event add, event_date, name, pickup time, pickup interval, guest_time, guest_interval, guest_rides' OR '.event remove, event_date'",
            bot_info[0])
        return True

    if message == '.notgoing':
        current_event_date = Queries.getCurrentEventDate()
        if current_event_date is None:
            send("No current event. Try again later", bot_info[0])
            return True
        event_opt_out = EventOptOut.newEventOptOut(data)
        event_opt_out.event_date = current_event_date
        storer.upsert(event_opt_out)
        send("You have been opted out of the event on " + current_event_date, bot_info[0])
        return True

    if message == '.going':
        current_event_date = Queries.getCurrentEventDate()
        if current_event_date is None:
            send("No current event. Try again later", bot_info[0])
            return True
        event_opt_out = EventOptOut.newEventOptOut(data)
        event_opt_out.event_date = current_event_date
        storer.remove(event_opt_out)
        send("You have been opted into the event on " + current_event_date, bot_info[0])
        return True

    if message == '.generate':
        event = Queries.getCurrentEvent()
        if event is None:
            send("No current event. Try again later", bot_info[0])
            return True

        rs = RideSchedule(event_date)
        rs.setCars(Queries.getCars(event_date))
        rs.setRiders(Queries.getRiders(event_date))
        rs.computeSchedule()
        storer.upsert(rs)
        schedule_html_url = publishSchedule(event, storer)

        send("Generation of rides completed. URL: " + schedule_html_url, bot_info[0])
        return True

    if message == '.getlink':
        event_date = Queries.getCurrentEventDate()
        if event_date is None:
            send("No current event. Try again later", bot_info[0])
            return True
        schedule_html_url = storer.presignURL("html/" + event_date + "/ride-index/index.html")
        send('URL: ' + schedule_html_url, bot_info[0])
        return True

    if message.startswith('.user '):
        user_parts = message.removeprefix('.user').split(',')
        if len(user_parts) != 2:
            send("Not enough data. Check to see that there is 1 comma in your command", bot_info[0])
            return True
        normalizer = helper.location_normalizer
        result = person.setTime(user_parts[0].strip())
        if result is not None:
            send("Error in pickup time." + str(result), bot_info[0])
        person.location = normalizer.normalize(user_parts[1].strip())
        if person.location is None:
            send("Not a valid location. The valid locations are: " + str(normalizer.location_list), bot_info[0])
        storer.upsert(person)
        send("Updated Person: " + str(person), bot_info[0])
        return True

    if message == '.driving':
        current_event_date = Queries.getCurrentEventDate()
        if current_event_date is None:
            send("No current event. Try again later", bot_info[0])
            return True
        event_driver = EventDriver.newEventDriver(data, current_event_date)
        storer.upsert(event_driver)
        send("You have been added to the list of drivers for the event on " + current_event_date, bot_info[0])
        return True

    if message == '.notdriving':
        current_event_date = Queries.getCurrentEventDate()
        if current_event_date is None:
            send("No current event. Try again later", bot_info[0])
            return True
        event_driver = EventDriver.newEventDriver(data, current_event_date)
        storer.remove(event_driver)
        send("You have been removed from the list of drivers for the event on " + current_event_date, bot_info[0])
        return True

    if message.startswith('.guest '):
        current_event = Queries.getCurrentEvent()
        if current_event is None:
            send("No current event. Try again later", bot_info[0])
            return True

        rs_json = storer.get(RideSchedule(current_event['event_date']).pk())
        if rs_json is None:
            send("No rides have been schedued yet. Generate a schedule and try again.", bot_info[0])
            return True
        rs = RideSchedule.asRideSchedule(rs_json)
        
        guest_parts = message.removeprefix('.guest ').split(',')  # add, location, guest information | edit, n:m, location, guest information | remove, n:m
        if guest_parts[0].strip()[:1].lower() == 'a':
            if len(guest_parts) != 3:
                send("Not enough data. Check to see that there are 2 commas in your command", bot_info[0])
                return True
            location = guest_parts[1].strip()
            description = guest_parts[2].strip()
            assignment = rs.addGuest(location, description)
            if assignment is None:
                send("No more guest rides available", bot_info[0])
                return True

            storer.upsert(rs)
            schedule_html_url = publishSchedule(current_event, storer)

            # assigment dictionary
            # {'event_date': '2022-03-14', 'time': '1001', 'car_id': '10480', 'driver_id': '10240', 'location': 'Haverford Villas 8', 'user_id': '[1:2] Sue Jones 45:8 (484-555-1212)'}

            # Use rsp to translate time offset to hh:mm
            rsp = currentRideSchedulePublisher(current_event)
            pickup_time = rsp.toFormattedTime(assignment['time'])

            # Retrieve driver
            driver = Person.asPerson(storer.get(Person(assignment['driver_id']).pk()))

            # Retrieve car
            car = Car.asCar(storer.get(Car(assignment['car_id']).pk()))

            guest_scheduled_message = "Guest " + description + ", from " + location + ", pickup @" + pickup_time + ", by " + car.model + ", driven by " + driver.name

            send(guest_scheduled_message + schedule_html_url, bot_info[0])
            send("Guest added. URL: " + schedule_html_url, bot_info[0])

            return True

        if guest_parts[0].strip()[:1].lower() == 'e':
            if len(guest_parts) != 4:
                send("Not enough data. Check to see that there are 3 commas in your command", bot_info[0])
                return True

            guest_id = guest_parts[1].strip()
            location = guest_parts[2].strip()
            description = guest_parts[3].strip()
            assignment = rs.editGuest(guest_id, location, description)
            if assignment is None:
                send("No such guest " + guest_id, bot_info[0])
                return True

            storer.upsert(rs)
            schedule_html_url = publishSchedule(current_event, storer)

            send("Guest edited. URL: " + schedule_html_url, bot_info[0])            

            return True

        if guest_parts[0].strip()[:1].lower() == 'r':
            if len(guest_parts) != 2:
                send("Not enough data. Check to see that there is 1 comma in your command", bot_info[0])
                return True

            guest_id = guest_parts[1].strip()
            assignment = rs.removeGuest(guest_id)
            if assignment is None:
                send("No such guest " + guest_id, bot_info[0])
                return True

            storer.upsert(rs)
            schedule_html_url = publishSchedule(current_event, storer)

            send("Guest removed. URL: " + schedule_html_url, bot_info[0])            
            return True

        send(
            "Error in format for .guest command. Should be '.guest add, location, information' OR '.guest edit, n:m, location, information' OR '.guest remove, n:m'",
            bot_info[0])


    # repeats any other message sent
    # send("Hi {}! You said: {}".format(data['name'], data['text']), bot_info[0])
    return True

def publishSchedule(event, storer):
    rsp = currentRideSchedulePublisher(event)
    schedule_html = rsp.asHTML()
    schedule_html_url = storer.putAsHtml("html/" + event['event_date'] + "/ride-index/index.html", schedule_html)
    return schedule_html_url

def currentRideSchedulePublisher(event):
    rsp=RideSchedulePublisher(
        event['event_date'], 
        event['pickup_time'], 
        event['pickup_interval'],
        event['guest_pickup_time'], 
        event['guest_pickup_interval'],
        1000)
    return rsp