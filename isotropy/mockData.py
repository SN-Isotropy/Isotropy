""""
Module to create mock data in the form of redshift (z), distance modulus (mu),
and distance modulus uncertainties (mu_error) as a function of spatial area.

This starts off with a small sample of simulated SN from the all sky Wide Fast
Deep fields of LSST where the light curves have been fitted and an estimate of
uncertainties in distance moduli as a function of redshifts have been found.

- Here we read in the results table and get rid of some bad data points
- In small redshift bins, we remove some of the outliers with very large mu
  error (these are useless to first order) and then model the distribution of
  distance modulus uncertainties as a normal distribution. This includes a
  component for the intrinsic dispersion
- We then draw samples of (z, mu_error) that respect this distribution in each
  redshift bin. We add values of mu by calculating the distance modulus for an
  assumed cosmology using astropy routines, and add a scattter consistent with
  the distribution of mu_error
"""
import sys
import gzip
import pickle
import pandas as pd
import numpy as np

__all__ = ['read_mockDataPickle']

def read_mockDataPickle(fname, filterBadPoints=True, selectCols=('z', 'mu', 'mu_var')):
    """
    Reads the Mock data in the form of a pickle file into a `pandas.DataFrame`
    such that the properties of SN are the columns. If the default `selectCols`
    is used, the columns are `z`, `mu`, `mu_var`
    Parameters
    ----------
    fname : string, mandatory
        absolute path to location of pickle file
    filterBadPoints : bool, optional, defaults to True
        Whether to filter bad data points
    selectCols  : tuple of strings, defaults to ('z', 'mu', 'mu_var')
        tuple of column names to keep
    """
    if sys.version.startswith('2'):
        snFits = pickle.load(gzip.GzipFile(fname))
    else:
        snFits = pickle.load(gzip.GzipFile(fname),
                                           encoding='latin1')
    df = pd.DataFrame(snFits).transpose()
    if filterBadPoints:
        df = df.query('mu < 19. and mu > 0.')

    if selectCols is not None:
        df = df[list(selectCols)].astype(np.float)
    return df

