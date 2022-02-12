from athena import Athena

class Queries:
    @classmethod
    def getCurrentEventDate(cls):
        result = Athena.executeQuery('select event_date from current_event')
        print(result)
        current_event_date = result[1]['Data'][0]['VarCharValue']
        print(current_event_date)
        return '2022-02-13'