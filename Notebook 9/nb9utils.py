#!/usr/bin/env python3
"""
Utility functions for CSE 6040, Notebook 9 (SQL).

- `get_path(x)`: Returns the expected local file prefix for this notebook.
- `download(file, url_suffix, checksum)`: Download or cache a required file.
- `auxfiles`: A dictionary defining the files and checksums used in this notebook.
"""

import requests
import os
import hashlib
import io

def get_path(x):
    return "resource/asnlib/publicdata/{}".format(x)

def download(file, checksum=None, binary=False,
             url_prefix="https://cse6040.gatech.edu/datasets/",
             url_suffix=''):
    def filemode(x): return x + '' if not binary else 'b'
    url = '{}{}{}'.format(url_prefix, url_suffix, file)
    local_file = get_path(file)

    if os.path.exists(local_file):
        print("[{}]\n==> '{}' is already available.".format(url, local_file))
    else:
        print("[{}] Downloading...".format(url))
        r = requests.get(url)
        with open(local_file, 'w', encoding=r.encoding) as f:
            f.write(r.text)
            
    if checksum is not None:
        if binary:
            with io.open(local_file, 'rb') as f:
                body = f.read()
            body_checksum = hashlib.md5(body).hexdigest()
        else: # not binary
            with io.open(local_file, 'r', encoding='utf-8', errors='replace') as f:
                body = f.read()
            body_checksum = hashlib.md5(body.encode('utf-8')).hexdigest()
        assert body_checksum == checksum, \
            "Downloaded file '{}' has incorrect checksum: '{}' instead of '{}'".format(local_file, body_checksum, checksum)
        print("==> Checksum test passes: {}".format(checksum))
    
    print("==> '{}' is ready!\n".format(local_file))
    return local_file

def download_nyc311db(file=r"NYC-311-2M.db",
                      checksum=r"f48eba2fb06e8ece7479461ea8c6dee9",
                      url_prefix=r"https://onedrive.live.com/download?cid=FD520DDC6BE92730&resid=FD520DDC6BE92730%21616&authkey=AEeP_4E1uh-vyDE"):
    return download(file, checksum=checksum, url_prefix=url_prefix, binary=True)
    
auxfiles = {'df_complaints_by_city_soln.csv': 'b07d65c208bd791ea21679a3551ae265', #'897d4bc4a39aa4abe188ca3f41b6a0b5', #'2a82e5856d5a267db9aafc26f16c3ae1',
            'df_complaints_by_hour_soln.csv': 'f06fcd917876d51ad52ddc13b2fee69e',
            'df_noisy_by_hour_soln.csv': '30f3fa7c753d4d3f4b3edfa1f6d05bcc',
            'df_plot_stacked_fraction_soln.csv': 'ab46e3f514824529edf65767771d4622'} #'2ca04a3eb24ccc37ddd0f8f5917fb27a'}

from bokeh.io import show, output_notebook
output_notebook()

from bokeh.plotting import figure

def make_barchart(df, labels, values, kwargs_figure={}):
    from pandas import DataFrame
    assert isinstance(df, DataFrame)
    assert type(labels) is str and type(values) is str
    p = figure(x_range=list(df[labels].unique()), **kwargs_figure)
    p.vbar(x=list(df[labels]), top=list(df[values]), width=0.9)
    return p

# Adapted from a mashup of:
# - https://bokeh.pydata.org/en/latest/docs/user_guide/categorical.html#userguide-categorical
# - https://groups.google.com/a/continuum.io/forum/#!topic/bokeh/x8j6EvJRty8
#
# This code is a hack to workaround an old installation of bokeh on Vocareum.

def make_stacked_barchart(df, x_var, cat_var, y_var, fillna=True,
                          x_labels=None, bar_labels=None,
                          kwargs_figure={}):
    from bokeh.models import ColumnDataSource
    from bokeh.plotting import figure
    from bokeh.core.properties import value
    from bokeh.models.ranges import FactorRange
    from bokeh.io import show
    from bokeh.plotting import figure

    assert type(x_var) is str, "x-variable should be a string but isn't."
    assert type(cat_var) is str, "category variable should be a string but isn't."
    assert type(y_var) is str, "y-variable should be a string but isn't."
    
    pt = df.pivot(x_var, cat_var, y_var)
    if fillna:
        pt.fillna(0, inplace=True)
    pt = pt.cumsum(axis=1)
    bar_vars = pt.columns
    
    from bokeh.palettes import brewer
    assert len(bar_vars) in brewer['Dark2'], "Not enough colors."

    x = x_labels if x_labels is not None else FactorRange(factors=list(pt.index))
    legend = bar_labels if bar_labels is not None else list(bar_vars)
    colors = brewer['Dark2'][len(bar_vars)]
    source = ColumnDataSource(data=df)

    p = figure(x_range=x, **kwargs_figure)
    bot = 0
    for k, var in enumerate(bar_vars):
        p.vbar(x=pt.index, bottom=bot, top=pt[var], color=colors[k], legend=var, width=0.25)
        bot = pt[var]
    return p

# eof
