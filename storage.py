# import boto3
from classes import Person
from classes import Car, Event


class Storage:
    def __init__(self):
        self.client = boto3.client('s3')
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

    def upsert_person(self, data):
        user_id = data['user_id']
        person_key = "Person/" + user_id
        person_str = self.get(person_key)
        if person_str is None:
            person = Person(user_id, data['name'])
            self.put(person_key, str(person))
            print('added new person: ' + str(person))
        else:
            person = Person.asPerson(person_str)
            if (data['name'] != person.name):
                person.name = data['name']
                self.put(person_key, str(person))
                print ('updated person: ' + str(person))
            else:
                print ('fetched existing person: ' + str(person))

        return person

    def upsert(self, obj):
        pk = obj.pk()
        self.put(pk, str(obj))
        return obj

    def remove(self, obj):
        pk = obj.pk()
        self.delete(pk)
