import boto3
import argparse
import sys
import pandas as pd
import numpy as np
from ..utils.calc import haversine, haversine2

import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--ports')
    parser.add_argument('--output')
    return parser.parse_args()


def get_nearest_port(long,lat,ports):
    return ports.iloc[np.argmin(haversine(pd.Series(long).repeat(len(ports)),pd.Series(lat).repeat(len(ports)),ports['longitude'],ports['latitude'])),2]


def main():
    args = get_args()

    IN_DIR = args.input
    OUT_DIR=args.output
    files=os.listdir(IN_DIR)
    res=pd.DataFrame()

    for i, f in enumerate(files):
        transit = pd.read_csv(IN_DIR+f)
        transit['exit_port'] = transit.apply(lambda x: get_nearest_port(x.longitude_exit, x.latitude_exit, ports),
                                             axis=1)
        transit['entry_port'] = transit.apply(lambda x: get_nearest_port(x.longitude_entry, x.latitude_entry, ports),
                                              axis=1)
        transit.to_csv('transit_' + f)



if __name__ == '__main__':
    print(sys.argv)
    main()