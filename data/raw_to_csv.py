# coding: utf-8

"""Read raw Airbase data and extract some data used in Kumo.
"""


import pandas as pd


FNAME = 'AirBase_v8_stations.csv'


def read_data(fname):
    """Read data from the CSV file

    Return a pandas DataFrame
    """
    return pd.read_csv(fname, sep='\t', index_col=0)


def extract_data(fname, colname):
    df = read_data(fname)
