import boto3
import argparse
import sys
from ..utils import creds
from ..utils import aws
from ..utils import mapping

session=boto3.Session(
    aws_access_key_id       =creds.AWS_ACCESS_KEY_ID,
    aws_secret_access_key   =creds.AWS_SECRET_ACCESS_KEY,
    region_name='eu-west-2',
)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', default=0, type=int)
    return parser.parse_args()

def main():
    args = get_args()

    query_ais = """
    SELECT DISTINCT movementdatetime
    ,destination
    ,destinationtidied
    ,speed
    ,additionalinfo
    ,callsign
    ,heading
    ,mmsi
    ,movementid
    ,shipname
    ,shiptype
    ,beam
    ,draught
    ,length
    ,eta
    ,movestatus
    ,ladenstatus
    ,lrimoshipno
    ,latitude
    ,longitude
    ,date

    FROM ais 

    WHERE latitude <=  90
    AND latitude   >= -90
    AND longitude  <= 180
    AND longitude  >=-180
    AND lrimoshipno >= """ + str(mapping.SHIPNO_LIMIT_LOW[args.batch])    + """ AND lrimoshipno < """ + str(mapping.SHIPNO_LIMIT_HI[args.batch]) + """ ORDER BY lrimoshipno,mmsi,movementdatetime"""




    ais = {
        'region': 'eu-west-2',
        'database': 'prophesea_staging',
        'bucket': 'data-science-athena-challenge',
        'path': 'athena-output',
        'query': query_ais,
        'workgroup': 'data-candidate-1'
    }
    print(aws.athena_to_s3(session, ais))



if __name__ == '__main__':
    print(sys.argv)
    main()