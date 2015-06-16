#!/usr/bin/env python
# coding: utf-8

"""Get raw data from the European Environment Agency
"""

import zipfile

import requests

DATA_URL = "http://ftp.eea.europa.eu/www/AirBase_v8/AirBase_v8_stations.zip"

def download_file(url):
    """Get it from http://stackoverflow.com/questions/16694907/
    """
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename

def extract_data(fname):
    zipf = zipfile.ZipFile(fname)
    zipf.extractall()
