from athena import Athena

class Queries:
    @classmethod
    def getCurrentEventDate(cls):
        result = Athena.executeQuery('select event_date from current_event')
        if len(result) == 1:
            return None
        print(result)
        current_event_date = result[1]['Data'][0]['VarCharValue']
        return current_event_date

