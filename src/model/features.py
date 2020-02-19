import boto3
import argparse
import sys
import pandas as pd
import numpy as np
from ..utils import creds
from ..utils import aws
from ..utils import mapping
from ..utils.calc import haversine, haversine2
from smart_open import open
from tqdm import tqdm as tqdm
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

        ports = pd.read_csv(IN_DIR+f)[['latitude','longitude','lrimoshipno']]
        res = gp.clear_duplicates(pd.concat([res, ports]))

    res.to_csv(OUT_DIR+'all_ports.csv')