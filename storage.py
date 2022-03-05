import boto3
from classes import Person

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

    def presignURL(self, key):
        return self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': 'battery-staple-v1', 'Key': key},
            ExpiresIn=7*24*60*60)

    def putAsHtml(self, key, content):
        self.client.put_object(
            Bucket='battery-staple-v1', 
            Key=key, 
            Body=content.encode('utf-8'),
            ContentType='text/html')
        return self.presignURL(key)

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