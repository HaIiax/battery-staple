import boto3
from classes import Person


class Storage:
    def __init__(self):
        self.persons = {}
        self.cars = {}
        self.client = boto3.client('s3')

        self.put('testing/Storage', 'a test value')
        print(self.get('testing/Storage'))

        print(self.get('testing/StorageNotFound'))

        self.put('testing/StorageToBeDeleted', 'a test value to be deleted')
        print(self.get('testing/StorageToBeDeleted'))
        self.delete('testing/StorageToBeDeleted')

        print('Storage Initialized')

    def get(self, key):
        try:
            sf = self.client.get_object(Bucket='battery-staple-v1', Key=key)
            return sf["Body"].read().decode("utf-8")
        except:
            return None

    def put(self, key, value):
        self.client.put_object(Bucket='battery-staple-v1', Key=key, Body=value.encode('utf-8'))

    def delete(self, key):
        try:
            self.client.delete_object(Bucket='battery-staple-v1', Key=key)
        except:
            return

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
