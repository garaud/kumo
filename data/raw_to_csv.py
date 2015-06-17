# coding: utf-8

"""Read raw Airbase data and extract some data used in Kumo.
"""


import pandas as pd


FNAME = 'AirBase_v8_stations.csv'
KEEP_COLS = ['station_european_code', 'country_name', 'station_name',
             'type_of_station', 'station_longitude_deg', 'station_latitude_deg',
             'station_altitude']
RENAME_COLS = {
    'country_name': 'country',
    'station_european_code': 'code',
    'station_name': 'name',
    'station_longitude_deg': 'lon',
    'station_latitude_deg': 'lat',
    'station_altitude': 'height',
    'type_of_station': 'type'
}

def read_data(fname):
    """Read data from the CSV file

    Return a pandas DataFrame
    """
    return pd.read_csv(fname, sep='\t')

def filter_column(df):
    """Remove then rename some columns
    """
    df = df.copy()
    for colname in df:
        if colname not in KEEP_COLS:
            df.pop(colname)
    df.rename_axis(RENAME_COLS, axis=1, inplace=True)
    df['type'] = df['type'].str.lower()
    return df

def latlon_to_coordinate(df):
    coords = []
    for _,series in df[['lat', 'lon']].iterrows():
        lat,lon = series['lat'], series['lon']
        coords.append("({},{})".format(lat,lon))
    return coords

def main(fname):
    rawdf = read_data(fname)
    df = filter_column(rawdf)
    df.sort_index(axis=1, inplace=True)
    df.index.name = 'id'
    # Some strange height value
    mask = df['height'].isin([9999,-9999])
    df['height'][mask] = 0
    mask = df['type'].isnull()
    df['type'][mask] = 'unknown'
    df.to_csv('airbase.csv', index=False)
    return df

if __name__ == '__main__':
    df = main(FNAME)
