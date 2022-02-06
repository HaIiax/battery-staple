from classes import Person


class Storage:
    def __init__(self):
        self.persons = {}
        self.cars = {}
        print('Storage Initialized')

    def stats(self):
        print ("len(self.persons): " + str(len(self.persons)))
        print ("len(self.cars): " + str(len(self.cars)))
        print ("==========")

    def upsert_person(self, data):

        if data['user_id'] not in self.persons:
            print("created a new person " + data['user_id'])
            person = Person(data['user_id'], data['name'], 'TBD', 'TBD')
            self.persons[data['user_id']] = person
        else:
            print('found existing person ' + data['user_id'])
            person = self.persons[data['user_id']]
            person.name = data['name']

        return person
