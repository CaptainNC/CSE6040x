#!/usr/bin/env python3
"""
Utility functions for Georgia Tech's CSE 6040, Notebook 7.

- `canonicalize_tibble(X)`: Given a DataFrame `X`, returns it in canonicalized-tibble form (sorted rows and columns, default index).
- `tibbles_are_equivalent(A, B)`: Returns `True` if two tibbles, `A` and `B`, are equivalent under row/column permutation.
- `cast(df, key, value, join_how)`: Casts the input data frame into a tibble, given the key column and value column.
"""

import pandas as pd

def canonicalize_tibble(X):
    var_names = sorted(X.columns)
    Y = X[var_names].copy()
    Y.sort_values(by=var_names, inplace=True)
    Y.reset_index(drop=True, inplace=True)
    return Y

def tibbles_are_equivalent (A, B):
    A_canonical = canonicalize_tibble(A)
    B_canonical = canonicalize_tibble(B)
    cmp = A_canonical.eq(B_canonical)
    return cmp.all().all()

def cast(df, key, value, join_how='outer'):
    assert type(df) is pd.DataFrame
    assert key in df.columns and value in df.columns
    assert join_how in ['outer', 'inner']
    
    fixed_vars = df.columns.difference([key, value])
    tibble = pd.DataFrame(columns=fixed_vars) # empty frame    
    new_vars = df[key].unique()
    for v in new_vars:
        df_v = df[df[key] == v]
        del df_v[key]
        df_v = df_v.rename(columns={value: v})
        tibble = tibble.merge(df_v,
                              on=list(fixed_vars),
                              how=join_how)    
    return tibble
