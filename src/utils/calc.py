import numpy as np
from math import radians, cos, sin, asin, sqrt

# Radius of the earth in kilometers
R=6372.8

def haversine(lon1, lat1, lon2, lat2):
    """
    Vectorized calculation of the great circle distance between two points
    on the earth (specified in decimal degrees)

    :param lat1: latitude 1 in degrees
    :param lon1: longitude 1 in degrees
    :param lat2: latitude 2 in degrees
    :param lon2: longitude 2 in degrees
    :return: array of distances in km between the 2 arrays of points
    """

    #Convert decimal degrees to Radians:
    lon1 = np.radians(lon1.values)
    lat1 = np.radians(lat1.values)
    lon2 = np.radians(lon2.values)
    lat2 = np.radians(lat2.values)

    #Implementing Haversine Formula:
    dlon = np.subtract(lon2, lon1)
    dlat = np.subtract(lat2, lat1)

    a = np.add(np.power(np.sin(np.divide(dlat, 2)), 2),
                          np.multiply(np.cos(lat1),
                                      np.multiply(np.cos(lat2),
                                                  np.power(np.sin(np.divide(dlon, 2)), 2))))
    c = np.multiply(2, np.arcsin(np.sqrt(a)))
    r = R

    return c*r



def haversine2(lat1, lon1, lat2, lon2):
    """
    Calculation of the great circle distance between two points
    on the earth (specified in decimal degrees)
    :param lat1: latitude 1 in degrees
    :param lon1: longitude 1 in degrees
    :param lat2: latitude 2 in degrees
    :param lon2: longitude 2 in degrees
    :return: distance in km between the 2 points
    """


    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c


