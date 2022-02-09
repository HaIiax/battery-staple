from storage import Storage
from classes import Car

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
        car_parts = message.removeprefix('.car').split('/') # add delete remove / seats / model / parking_location
        car.seats = car_parts[1]
        car.model = car_parts[2]
        car.parking_spot = car_parts[3]
        storer.upsert_car(car)
        send("added car: " + str(car), bot_info[0])
        return True

    send("Hi {}! You said: {}".format(data['name'], data['text']), bot_info[0])
    return True
