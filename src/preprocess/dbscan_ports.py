import pandas as pd, numpy as np, matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint
import time

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--output')
    return parser.parse_args()

def get_centermost_point(cluster):
    """
    returns the centerpoint of each dbscan cluster

    """
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)


def dbscan_reduce(df, epsilon, x='longitude', y='latitude'):
    """
    runs dbscan algorithm on df with long lat
    :param df: ports
    :param epsilon:
    :param x: longitude
    :param y: latitude
    :return:
    """
    start_time = time.time()
    # represent points consistently as (lat, lon) and convert to radians to fit using haversine metric
    coords = df.as_matrix(columns=[y, x])
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels))
    print('Number of clusters: {:,}'.format(num_clusters))

    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])

    # find the point in each cluster that is closest to its centroid
    centermost_points = clusters.map(get_centermost_point)

    # unzip the list of centermost points (lat, lon) tuples into separate lat and lon lists
    lats, lons = zip(*centermost_points)
    rep_points = pd.DataFrame({x: lons, y: lats})
    rep_points.tail()

    # pull row from original data set where lat/lon match the lat/lon of each row of representative points
    rs = rep_points.apply(lambda row: df[(df[y] == row[y]) & (df[x] == row[x])].iloc[0], axis=1)

    # all done, print outcome
    message = 'Clustered {:,} points down to {:,} points, for {:.2f}% compression in {:,.2f} seconds.'
    print(message.format(len(df), len(rs), 100 * (1 - float(len(rs)) / len(df)), time.time() - start_time))
    return rs



def main():
    args = get_args()
    IN_DIR = args.input
    OUT_DIR=args.output
    files=os.listdir(IN_DIR)
    df=pd.DataFrame()
    for f in files:
        df = pd.concat([pd.read_csv(IN_DIR+f),df])

    kms_per_radian = 6371.0088
    eps_rad = 5 / kms_per_radian
    df_clustered = dbscan_reduce(df, epsilon=eps_rad)
    df_clustered.to_csv(OUT_DIR+'dbscan_ports.csv',index=False)

if __name__ == '__main__':
    print(sys.argv)
    main()
