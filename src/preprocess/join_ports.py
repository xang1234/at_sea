import argparse
import sys
import os
import pandas as pd
import numpy as np



import src.preprocess.get_ports as gp

PORT_THRESHOLD = 10  #ships stopped within PORT_THRESHOLD km of each other are considered stopped at the same port
SPEED_LIMIT = 0.1
TIME_LIMIT = 24

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--output')
    return parser.parse_args()


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

if __name__ == '__main__':
    print(sys.argv)
    print('joining')
    main()
    print('done')