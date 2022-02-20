import time
import boto3
import uuid
import traceback


class Athena:
    client = boto3.client('athena')

    @classmethod
    def executeQueryToRows(cls, query):
        result = cls.executeQuery(query)
        if result is None:
            return None
        return _ResultSet(result).rows

    @classmethod
    def executeQuery(cls, query):
        try:
            if True:
                print(query)
            qresp = cls.client.start_query_execution(
                QueryString=query,
                ClientRequestToken=uuid.uuid4().hex,
                QueryExecutionContext={
                    'Database': 'default',
                    'Catalog': 'AwsDataCatalog'
                },
                ResultConfiguration={
                    'OutputLocation': 's3://battery-staple-v1/Athena/'
                },
                WorkGroup='primary')
            if False:
                print(qresp)

            execution_id = qresp['QueryExecutionId']

            next_sleep = 0.9
            while True:
                stats = cls.client.get_query_execution(
                    QueryExecutionId=execution_id)
                status = stats['QueryExecution']['Status']['State']
                if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                    break
                time.sleep(next_sleep)  # 2 seconds max
                if next_sleep < 2.0:
                    next_sleep *= 1.2

            if status == 'SUCCEEDED':
                qresult = cls.client.get_query_results(
                    QueryExecutionId=execution_id,
                    MaxResults=1000)
                return qresult['ResultSet']['Rows']

            if status == 'FAILED':
                raise BaseException(
                    stats['QueryExecution']['Status']['StateChangeReason'])

            return None
        except BaseException as error:
            print('exception occurred during query execution: {}'.format(error))
            print(traceback.format_exc())
            return None


"""
[
    {'Data':
        [{'VarCharValue': 'owner'}, {'VarCharValue': 'seats'}, {'VarCharValue': 'model'}, {'VarCharValue': 'parking_spot'}]},
    {'Data':
        [{'VarCharValue': '72255120'}, {'VarCharValue': '4'}, {'VarCharValue': 'Honda Accord'}, {'VarCharValue': 'Septa Station'}]}
]
"""


class _ResultSet:
    def __init__(self, result):
        self.rows = []
        # Row 0 has the metadata for the result
        if result is not None:
            # cols list matches order of data rows
            cols = []
            row0 = result[0]['Data']
            for col in row0:
                cols.append(col["VarCharValue"])

            for result_row in result[1:]:
                row = {}
                row_index = 0
                for data in result_row['Data']:
                    row[cols[row_index]] = (data["VarCharValue"])
                    row_index += 1
                self.rows.append(row)

    def __str__(self) -> str:
        return str(self.rows)