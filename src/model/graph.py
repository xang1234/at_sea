import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain
from mpl_toolkits.basemap import Basemap as Basemap
import os

def draw_map(m, scale=0.2):
    # draw a shaded-relief image
    m.shadedrelief(scale=scale)

    # lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(-90, 90, 13))
    lons = m.drawmeridians(np.linspace(-180, 180, 13))

    # keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)

    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')


def main():
    IN_DIR='/Users/dten/PycharmProjects/rio_ship/data/endpoints_ports/'
    files=os.listdir(IN_DIR)
    transit = pd.DataFrame()
    for i, f in enumerate(files):
        temp = pd.read_csv(IN_DIR + f, parse_dates=['movementdatetime_exit', 'movementdatetime_entry'])
        transit = pd.concat([transit, temp])
    transit['exit_date'] = transit['movementdatetime_exit'].dt.normalize()
    transit['entry_date'] = transit['movementdatetime_entry'].dt.normalize()
    vessel=pd.read_csv('/Users/dten/PycharmProjects/rio_ship/data/vessels.csv')

    transit = transit.merge(vessel, how='left', left_on='lrimoshipno_entry', right_on='imo')


    world_ports = pd.read_csv('/Users/dten/PycharmProjects/rio_ship/data/wld_trs_ports_wfp.csv')[['portname', 'longitude', 'latitude']]
    graph = transit.query('dwt>=150000').groupby(['exit_port', 'entry_port']).size().reset_index().rename(
        columns={0: 'count'})
    graph = graph.merge(world_ports, how='left', left_on='exit_port', right_on='portname').rename(
        columns={'longitude': 'exit_longitude', 'latitude': 'exit_latitude'})
    graph = graph.merge(world_ports, how='left', left_on='entry_port', right_on='portname').rename(
        columns={'longitude': 'entry_longitude', 'latitude': 'entry_latitude'})
    plt.figure(figsize=(20, 12))
    m = Basemap(
        projection='cyl', resolution=None,
        llcrnrlat=-90, urcrnrlat=90,
        llcrnrlon=-180, urcrnrlon=180, )
    G = nx.Graph()
    for i in range(len(graph)):
        G.add_edge(graph.exit_port[i], graph.entry_port[i])
    pos = {}
    for i in range(len(graph)):
        # position in decimal lat/lon
        lats = [graph.exit_latitude[i], graph.entry_latitude[i]]
        lons = [graph.exit_longitude[i], graph.entry_longitude[i]]
        # convert lat and lon to map projection
        mx, my = m(lons, lats)

        # The NetworkX part
        # put map projection coordinates in pos dictionary

        pos[graph.exit_port[i]] = (mx[0], my[0])
        pos[graph.entry_port[i]] = (mx[1], my[1])
        # draw
    nx.draw_networkx(G, pos, node_size=10, node_color='blue', with_labels=False, alpha=0.3, width=0.1,
                     edge_color='grey')
    # Now draw the map
    draw_map(m)
    plt.title('Ports')
    plt.show()

if __name__ == '__main__':
    main()