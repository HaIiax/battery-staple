import time
import boto3
import uuid
import traceback

class Athena:
    client = boto3.client('athena')

    @classmethod
    def executeQuery(cls, query):
        try:
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
            print(qresp)

            execution_id = qresp['QueryExecutionId']

            while True:
                stats = cls.client.get_query_execution(QueryExecutionId=execution_id)
                status = stats['QueryExecution']['Status']['State']
                if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                    break
                time.sleep(2.0)  # 2 seconds

            if status == 'SUCCEEDED':
                qresult = cls.client.get_query_results(
                    QueryExecutionId=execution_id,
                    MaxResults=1000)
                return qresult['ResultSet']['Rows']
            else:
                return None
        except BaseException as error:
            print('exception occurred during query execution: {}'.format(error))
            print(traceback.format_exc())
            return None