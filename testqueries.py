import random
from datetime import datetime, date
from functools import cmp_to_key
from queries import QueryTemplate

class TestQueries(QueryTemplate):

    names = [
        "Norton Nelson",
        "Sampson Kitchen",
        "Darby Newport",
        "Trevor Blue",
        "Luther Waterman",
        "Pierce Fairclough",
        "Emery Benson",
        "Samuel Backus",
        "Zachariah Isaacson",
        "Trey Dannel",
        "Kelsey Pressley",
        "Monroe Fleming",
        "Osborne Conner",
        "Caleb Dodge",
        "Sunny Post",
        "Corbin York",
        "Isadore Bloxham",
        "Clive Dale",
        "Braden Gold",
        "Durward Foster",
        "Colby Hendry",
        "Eli Gilliam",
        "Landon Cleveland",
        "Edgar Coleman",
        "Alan Caulfield",
        "Meredith Travis",
        "Warren Hambleton",
        "Cheyenne Palmer",
        "Gary Dennell",
        "Drake Waldo",
        "Cornelius Hunnisett",
        "Wilford Leighton",
        "Callan Stack",
        "Kerry Huff",
        "Corbin Randall",
        "Theodore Gibson",
        "Rollo Trueman",
        "Chadwick Wade",
        "Haywood Nye",
        "Bevan Aitken",
        "Melville Sowards",
        "Corey Lynn",
        "Carter Winthrop",
        "Ora Kemp",
        "Ennis Pettigrew",
        "Dominic Huddleston",
        "Emil Babcock",
        "Bryce Clement",
        "Hale Coleman",
        "Shepherd Winthrop",
        "Basil Knowles",
        "Cleveland Thomson",
        "Delano Elliston",
        "Elliott Dukes",
        "Leland Rose",
        "Walton Robson",
        "Everette Firmin",
        "Simon Arkwright",
        "Brenden Lane",
        "Irving Butler",
        "Rodney Minett",
        "Brendan Tailor",
        "Abner London",
        "Trent Carpenter",
        "Watson Cotterill"
    ]

    cars = [
        "Nissan Altima, Hot Obsidian; 4",
        "Honda Accord, Illuminated Tan; 4",
        "Chevrolet Malibu, Botanic Jasper; 4",
        "Honda Civic, Charred Amethyst; 4",
        "Chevrolet Impala, Pale Sanguine; 4",
        "Ford Focus, Tropical Sand; 4",
        "Toyota Corolla, Fiery Turquoise; 4",
        "Ford Explorer, Cosmic Chrome; 7",
        "Subaru Impreza, Smooth Aquamarine; 4",
        "Toyota RAV4, Blossom Cyan; 4",
        "Toyota Highlander, Dynamic Vanilla; 6",
    ]

    locations = [
        "Commons",
        "Main",
        "West"
    ]

    parking = [
        "L4",
        "I5",
        "S1",
        "SeptaMain"
    ]

    times = [
        "1",
        "2",
        "3",
        "4",
        "5"
    ]

    @classmethod
    def generatePersons(cls):
        random.seed(0)
        res = []
        # user id's are assigned consistently with the offset on the names list
        cur_user_id = 10000
        for name in cls.names:
            person = {}
            person["user_id"] = str(cur_user_id)
            cur_user_id += 120
            person["name"] = name
            person["location"] = random.choice(cls.locations)
            person["time"] = random.choice(cls.times)
            res.append(person)

        return res


    def getCurrentEventDate(self):
        return date.today().strftime('%Y-%m-%d')

    def getCars(self):
        random.seed(0)
        persons = TestQueries.generatePersons()
        res = []
        used = {}
        for cardata in TestQueries.cars:
            person_owner = random.choice(persons)["user_id"]
            while person_owner in used:
                person_owner = random.choice(persons)["user_id"]
            used[person_owner] = True
            car = {}
            car["owner"] = person_owner
            carparts = cardata.split(";")
            car["model"] = carparts[0]
            car["seats"] = carparts[1]
            car["parking_spot"] = random.choice(TestQueries.parking)
            res.append(car)

        def compareKI(l, r, k):
            ln = int(l[k])
            rn = int(r[k])
            return ln - rn

        def compare(l, r):
            cmp = compareKI(l, r, "seats")
            return cmp

        res.sort(key = cmp_to_key(compare), reverse=True)

        return res

    def getRiders(self):
        # Simulate select * from current_riders
        event_date = self.getCurrentEventDate()
        event_name = "The event held on " + event_date
        persons = TestQueries.generatePersons()
        for person in persons:
            person["event_date"] = event_date
            person["event_name"] = event_name

        def compareK(l, r, k):
            ln = l[k]
            rn = r[k]
            if ln < rn:
                return -1
            if ln > rn:
                return 1
            return 0

        def compare(l, r):
            cmp = compareK(l, r, "location")
            if cmp == 0:
                cmp = compareK(l, r, "time")
            return cmp

        persons.sort(key = cmp_to_key(compare), reverse=False)

        return persons