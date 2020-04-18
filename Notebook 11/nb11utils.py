#!/usr/bin/env python3

import requests
import os
import hashlib
import io

def on_vocareum():
    return os.path.exists('.voc')

def get_url_base():
    return "https://cse6040.gatech.edu/datasets/us-flights/"

def get_data_path(filebase=""):
    if on_vocareum():
        DATA_PATH = "./resource/asnlib/publicdata/"
    else:
        DATA_PATH = ""
    return f"{DATA_PATH}{filebase}"

def download(file, local_dir=None, url_base=None, checksum=None):
    if local_dir is None: local_dir = get_data_path()
    if url_base is None: url_base = get_url_base()
    assert (local_dir is not None) and (url_base is not None)

    local_file = "{}{}".format(local_dir, file)
    if not os.path.exists(local_file):
        if url_base is None:
            url_base = "https://cse6040.gatech.edu/datasets/"
        url = "{}{}".format(url_base, file)
        print("Downloading: {} ...".format(url))
        r = requests.get(url)
        with open(local_file, 'wb') as f:
            f.write(r.content)
            
    if checksum is not None:
        with io.open(local_file, 'rb') as f:
            body = f.read()
            body_checksum = hashlib.md5(body).hexdigest()
            assert body_checksum == checksum, \
                "Downloaded file '{}' has incorrect checksum: '{}' instead of '{}'".format(local_file,
                                                                                           body_checksum,
                                                                                           checksum)
    print("'{}' is ready!".format(file))

def download_airport_dataset():
    datasets = {'L_AIRPORT_ID.csv': 'e9f250e3c93d625cce92d08648c4bbf0',
                'L_CITY_MARKET_ID.csv': 'f430a16a5fe4b9a849accb5d332b2bb8',
                'L_UNIQUE_CARRIERS.csv': 'bebe919e85e2cf72e7041dbf1ae5794e',
                'us-flights--2017-08.csv': 'eeb259c0cdd00ff1027261ca0a7c0332',
                'flights_atl_to_lax_soln.csv': '4591f6501411de90af72693cdbcc08bb',
                'origins_top10_soln.csv': 'de85c321c45c7bf65612754be4567086',
                'dests_soln.csv': '370f4c632623616b3bf26b6f79993fe4',
                'dests_top10_soln.csv': '4c7dd7edf48c4d62466964d6b8c14184',
                'segments_soln.csv': '516a78d2d9d768d78bfb012b77671f38',
                'segments_outdegree_soln.csv': 'b29d60151c617ebafd3a1c58541477c8'
               }
    for filename, checksum in datasets.items():
        download(filename, checksum=checksum)

# Pandas-based
def canonicalize_tibble(X):
    var_names = sorted(X.columns)
    Y = X[var_names].copy()
    Y.sort_values(by=var_names, inplace=True)
    Y.reset_index(drop=True, inplace=True)
    return Y

# Pandas-based
def tibbles_are_equivalent (A, B):
    A_canonical = canonicalize_tibble(A)
    B_canonical = canonicalize_tibble(B)
    cmp = A_canonical.eq(B_canonical)
    return cmp.all().all()

# eof
