import boto3
import argparse
import sys
import pandas as pd
import numpy as np
from ..utils import creds
from ..utils import mapping
from ..utils.calc import haversine, haversine2
from smart_open import open
from tqdm import tqdm as tqdm


PORT_THRESHOLD = 10  #ships stopped within PORT_THRESHOLD km of each other are considered stopped at the same port
SPEED_LIMIT = 0.1
TIME_LIMIT = 24

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', default=1, type=int)
    parser.add_argument('--port_threshold', default=PORT_THRESHOLD, type=float)
    parser.add_argument('--speed_limit', default=SPEED_LIMIT, type=float)
    parser.add_argument('--time_limit', default=TIME_LIMIT, type=float)
    parser.add_argument('--output')
    return parser.parse_args()


def get_transit(chunk, speed_limit=SPEED_LIMIT, time_limit=TIME_LIMIT):
    """
    AIS data is analyzed by lrimoshipno.
    - Distance between two points are calculated using the haversine function.
    - Average speed between 2 points is calculated
    - A ship is inferred to be at rest at a port is it's average speed is below SPEED_LIMIT for TIME_LIMIT


    :param chunk: dataframe read by chunk and grouped by lrimoshipno and sorted by movementdatetime
    :param speed_limit: ships below speed limit are considered docked (km/h)
    :param time_limit: ships stationary for longer than this limit are considered docked (hours)
    :return: port coordinates
    """
    concat = pd.concat([chunk[['longitude', 'latitude']], chunk[['longitude', 'latitude']].shift()], axis=1)
    chunk['movementdatetime'] = pd.to_datetime(chunk['movementdatetime'], errors='coerce')

    chunk['distance'] = haversine(concat.iloc[:, 0], concat.iloc[:, 1], concat.iloc[:, 2], concat.iloc[:, 3]) # distance in km
    chunk['time_delta'] = chunk['movementdatetime'].diff()
    chunk['time_delta'] = chunk['time_delta'].apply(lambda x: x.total_seconds() / 3600)  # time delta in hours
    chunk['avg_speed'] = chunk['distance'] / (chunk['time_delta'] + 1 / 3600)   #

    idx_first = np.unique(chunk.lrimoshipno.values, return_index=1)[1] + chunk.index[0]
    chunk = chunk.drop(idx_first)

    cumsum = chunk['time_delta'].cumsum()
    condition = np.array(chunk[['avg_speed']].values > speed_limit, dtype=int).reshape(-1)
    stationary = (cumsum.sub(cumsum.mask(condition == 0).ffill(), fill_value=0) >= time_limit).astype(int)
    ports = chunk.loc[(np.argwhere(np.diff(stationary)[:-1] == 1) + 1 + chunk.index[0]).reshape(-1), :][
        ['latitude', 'longitude', 'lrimoshipno']]

    return clear_duplicates(ports.drop_duplicates(['latitude', 'longitude']))


def get_endpoints(chunk,stop_radius=STOP_RADIUS,time_limit=TIME_LIMIT):
    concat = pd.concat([chunk[['longitude','latitude']],chunk[['longitude','latitude']].shift()],axis=1)
    chunk['movementdatetime']=pd.to_datetime(chunk['movementdatetime'],errors='coerce')
    chunk['distance']=haversine(concat.iloc[:,0],concat.iloc[:,1],concat.iloc[:,2],concat.iloc[:,3])
    chunk['time_delta']=chunk['movementdatetime'].diff()
    chunk['time_delta']=chunk['time_delta'].apply(lambda x: x.total_seconds()/3600) # time delta in hours
    #chunk['avg_speed']=chunk['distance']/(chunk['time_delta']+1/3600)

#     idx_first = np.unique(chunk.lrimoshipno.values, return_index=1)[1]+chunk.index[0]
#     chunk=chunk.drop(idx_first)

    cumsum=chunk['time_delta'].cumsum()
    condition=np.array(chunk[['distance']].values >= stop_radius,dtype=int ).reshape(-1)
    stationary=(cumsum.sub(cumsum.mask(condition==0).ffill(), fill_value=0) >=time_limit).astype(int)
    enter_port=chunk.loc[(np.argwhere(np.diff(stationary)[:-1]==1)+1+chunk.index[0]).reshape(-1),:][['latitude','longitude','lrimoshipno','movementdatetime']].rename(columns={"latitude":"latitude_entry","longitude":"longitude_entry","lrimoshipno":"lrimoshipno_entry","movementdatetime":"movementdatetime_entry"})
    leave_port=chunk.loc[(np.argwhere(np.diff(stationary)[:-1]==-1)+1+chunk.index[0]).reshape(-1),:][['latitude','longitude','lrimoshipno','movementdatetime']].rename(columns={"latitude":"latitude_exit","longitude":"longitude_exit","lrimoshipno":"lrimoshipno_exit","movementdatetime":"movementdatetime_exit"})
    transit=pd.concat([enter_port.reset_index(drop=True),leave_port.reset_index(drop=True)],axis=1).dropna()

    return transit




def transit_groupby_csv(session, params, s3_filename, key, agg,transport_params, chunk_size=1e6):
    """
    ###  https://maxhalford.github.io/blog/streaming-groupbys-in-pandas-for-big-datasets/ ###

    pandas function to reduce memory usage. Data needs to be SORTED by a key and is processed by chunk_size batches.
    this can lead to hanging or orphan keys which is also handled.

    In our case data is grouped by lrimoshipno and sorted by movementdatetime


    :param session: boto3 session to access athena data
    :param params: boto3 parameter dictionary
    :param s3_filename: file to process after running get_data
    :param key: data has to be sorted by this key
    :param agg: data processing function
    :param chunk_size: number of rows per batch for processing
    :return: dataframe with potential port coordinates
    """
    chunks = pd.read_csv(
        open('s3://' + params['bucket'] + '/' + params['path'] + '/' + s3_filename, transport_params=transport_params),
        chunksize=chunk_size, parse_dates=['movementdatetime'])
    results = []
    orphans = pd.DataFrame()
    for chunk in tqdm(chunks):
        # Add the previous orphans to the chunk
        chunk = pd.concat((orphans, chunk))

        # Determine which rows are orphans
        last_val = chunk[key].iloc[-1]
        is_orphan = chunk[key] == last_val

        # Put the new orphans aside
        chunk, orphans = chunk[~is_orphan], chunk[is_orphan]

        # Perform the aggregation and store the results
        result = agg(chunk)
        results.append(result)
    return pd.concat(results)

transport_params = {'session': boto3.Session(   aws_access_key_id=creds.AWS_ACCESS_KEY_ID,
                                                aws_secret_access_key=creds.AWS_SECRET_ACCESS_KEY,
                                                region_name='eu-west-2')}

params = {
    'region': 'eu-west-2',
    'database': 'prophesea_staging',
    'bucket': 'data-science-athena-challenge',
    'path': 'athena-output',
    'workgroup': 'data-candidate-1'
}


session=boto3.Session(
    aws_access_key_id       =creds.AWS_ACCESS_KEY_ID,
    aws_secret_access_key   =creds.AWS_SECRET_ACCESS_KEY,
    region_name='eu-west-2',
)



def main():
    args = get_args()

    PORT_THRESHOLD = args.port_threshold
    SPEED_LIMIT = args.speed_limit
    TIME_LIMIT = args.time_limit
    OUT_DIR=args.output
    files=[k for (k,v) in mapping.AIS_FILES.items() if v == args.batch]
    print(files)


    for i, f in enumerate(files):

        port = port_groupby_csv(session, params, f, 'lrimoshipno', get_endpoints, transport_params,1e6)
        print(f)
        port.to_csv(OUT_DIR+'/port_' + f)

if __name__ == '__main__':
    print(sys.argv)
    main()