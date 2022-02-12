from athena import Athena

class Queries:
    @classmethod
    def getCurrentEventDate(cls):
        result = Athena.executeQuery('select event_date from current_event')
        print(result)
        return '2022-02-13'