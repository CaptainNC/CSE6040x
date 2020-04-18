"""
This module implements some helper code common to CSE 6040 assignments.
"""

import requests
import os
import hashlib
import io

def on_vocareum():
    return os.path.exists('.voc')

def download_datafile(filename, local_path=None, url_suffix=None, checksum=None, vocareum_only=False):
    if local_path is None:
        if vocareum_only or on_vocareum():
            local_path = './resource/asnlib/publicdata/'
        else:
            local_path = ''
    local_path_full = f'{local_path}{filename}'

    if url_suffix is None:
        url_suffix = filename
    url = 'https://cse6040.gatech.edu/datasets/{}'.format(url_suffix)

    if not os.path.exists(local_path_full):
        assert not vocareum_only or on_vocareum(), \
               f"ERROR: Due to its size or the setup of this problem, the data file {local_path_full} is only available on Vocareum and is not available for download."
        print("Downloading: {} ...".format(url))
        r = requests.get(url)
        with open(local_path_full, 'w', encoding=r.encoding) as f:
            f.write(r.text)
            
    if checksum is not None:
        with io.open(local_path_full, 'r', encoding='utf-8', errors='replace') as f:
            body = f.read()
            body_checksum = hashlib.md5(body.encode('utf-8')).hexdigest()
            assert body_checksum == checksum, \
                "Downloaded file '{}' has incorrect checksum: '{}' instead of '{}'".format(local_path_full, body_checksum, checksum)
    
    print("'{}' is ready!".format(local_path_full))
    return local_path_full

def download_dataset(datafiles, **args):
    localfiles = {}
    for filename, checksum in datafiles.items():
        localfiles[filename] = download_datafile(filename, checksum=checksum, **args)
    return localfiles

# eof
