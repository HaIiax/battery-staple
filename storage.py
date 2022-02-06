from classes import Person

class Storage:
    def __init__(self):
        self.persons = {}
        self.cars = {}


    def upsert_person(self, data):

        if data['user_id'] not in self.persons:
            person = Person(data['user_id'], data['name'], 'TBD', 'TBD')
            self.persons[data['user_id']] = person
        else:
            person = self.persons[data['user_id']]
            person.name = data['name']

        return person



