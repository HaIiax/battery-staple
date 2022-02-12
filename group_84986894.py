from storage import Storage
from classes import Car, Event

def run(storer, data, bot_info, send):

    help_message = "Help:\n.help  -->  This screen\n.test  -->  Try it!\nOtherwise, repeats your message."

    person = storer.upsert_person(data)
    print(person)

    message: str = data['text']

    if message == '.help':
        send(help_message, bot_info[0])
        return True

    if message == '.test':
        send("Hi there! Your bot is working, you should start customizing it now.", bot_info[0])
        return True

    if message.startswith('.car'):
        car = Car.newCar(data)
        car_parts = message.removeprefix('.car').split(',') # add delete remove , seats , model , parking_location

        if car_parts[0].strip()[:1].lower() == 'a':
            if len(car_parts) != 4:
                send("Not enough data. Check to see that there are 3 commas in your command", bot_info[0])
                return True
            car.seats = car_parts[1].strip()
            car.model = car_parts[2].strip()
            car.parking_spot = car_parts[3].strip()
            storer.upsert_car(car)
            send("added car: " + str(car), bot_info[0])
            return True

        if car_parts[0].strip()[:1].lower() == 'r':
            storer.remove_car(car)
            send("removed car: " + str(car), bot_info[0])
            return True

        send("Error in format for .car command. Should be '.car add, seats, model, parking_location' OR '.car remove'", bot_info[0])
        return True

    if message.startswith('.event'):
        event = Event.newEvent()
        event_parts = message.removeprefix('.event').split(',') # add delete remove / seats / model / parking_location
        if event_parts[0].strip()[:1].lower() == 'a':
            if len(event_parts) != 2:
                send("Not enough data. Check to see that there are 2 commas in your command", bot_info[0])
                return True
            result = event.setEventDate(event_parts[1].strip())
            if result is not None:
                send("Error in date input." + str(result), bot_info[0])
                return True
            event.name = event_parts[2].strip()
            storer.upsert_event(event)
            send("added event: " + str(event), bot_info[0])
            return True

        if event_parts[0].strip()[:1].lower() == 'r':
            if len(event_parts) != 1:
                send("Not enough data. Check to see that there is 1 comma in your command", bot_info[0])
                return True
            result = event.setEventDate(event_parts[1].strip())
            if result is not None:
                send("Error in date input." + str(result), bot_info[0])
                return True
            storer.remove_event(event)
            send("removed event: " + str(event), bot_info[0])
            return True

        send("Error in format for .event command. Should be '.event add, event_date, name' OR '.event remove, event_date'",
             bot_info[0])
        return True

    send("Hi {}! You said: {}".format(data['name'], data['text']), bot_info[0])
    return True
