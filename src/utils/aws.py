import boto3
import pandas as pd


def athena_query(client, params):
    response = client.start_query_execution(
        QueryString=params["query"],
        QueryExecutionContext={
            'Database': params['database']
        },
        ResultConfiguration={
            'OutputLocation': 's3://' + params['bucket'] + '/' + params['path']
        },
        WorkGroup=params["workgroup"]
    )
    return response


def athena_to_s3(session, params, max_execution=5):
    client = session.client('athena', region_name=params["region"])
    execution = athena_query(client, params)
    execution_id = execution['QueryExecutionId']
    state = 'RUNNING'

    while (max_execution > 0 and state in ['RUNNING']):
        max_execution = max_execution - 1
        response = client.get_query_execution(QueryExecutionId=execution_id)

        if 'QueryExecution' in response and \
                'Status' in response['QueryExecution'] and \
                'State' in response['QueryExecution']['Status']:
            state = response['QueryExecution']['Status']['State']
            if state == 'QUEUED':
                return 'QUEUED', execution_id
            elif state == 'RUNNING':
                return 'RUNNING', execution_id
            elif state == 'FAILED':
                return 'FAILED', execution_id
            elif state == 'SUCCEEDED':
                s3_path = response['QueryExecution']['ResultConfiguration']['OutputLocation']
                filename = re.findall('.*\/(.*)', s3_path)[0]
                return filename
        time.sleep(1)

    return False


def s3_to_pandas(session, params, s3_filename):
    # check query status, assumes execution_id and filenams are same
    client = session.client('athena', region_name=params["region"])
    execution_id = s3_filename.split('.')[0]
    response = client.get_query_execution(QueryExecutionId=execution_id)
    state = response['QueryExecution']['Status']['State']
    if state == 'SUCCEEDED':

        s3client = session.client('s3')
        obj = s3client.get_object(Bucket=params['bucket'],
                                  Key=params['path'] + '/' + s3_filename)
        df = pd.read_csv(io.BytesIO(obj['Body'].read()), parse_dates=['movementdatetime'])
    else:
        return response
    return df


def s3_to_pandas_vessel(session, params, s3_filename):
    # check query status, assumes execution_id and filenams are same
    client = session.client('athena', region_name=params["region"])
    execution_id = s3_filename.split('.')[0]
    response = client.get_query_execution(QueryExecutionId=execution_id)
    state = response['QueryExecution']['Status']['State']
    if state == 'SUCCEEDED':

        s3client = session.client('s3')
        obj = s3client.get_object(Bucket=params['bucket'],
                                  Key=params['path'] + '/' + s3_filename)
        df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    else:
        return response
    return df