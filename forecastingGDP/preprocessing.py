import numpy as np
import pandas as pd

from sklearn.base import TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# ------------------------------------------------------------------------------
# -- Preprocessing pipeline
# ------------------------------------------------------------------------------
def preprocessor():
    return Pipeline([
        ('scaler', StandardScaler()),
        ('sequencer', SequenceGenerator()),
    ])

# ------------------------------------------------------------------------------
# -- Sequences management
# ------------------------------------------------------------------------------
class SequenceGenerator(TransformerMixin):
    '''Transform a dataframe into a list of samples (X, y)'''
    def __init__(self, count=500, input_length=6, output_length=1, horizon=0):
        self.count = count
        self.input_length = input_length
        self.output_length = output_length
        self.horizon = horizon

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return subsamples(X, self.count, input_length=self.length)

def subsamples(df, n_samples, input_length=10, output_length=1, horizon=0, target_col='GDPC1'):
    '''Returns a list of subsamples (X, y)'''
    X, y = [], []
    for _ in range(n_samples):
        Xi, yi = subsample(df, input_length, output_length, horizon, target_col)
        X.append(Xi)
        y.append(yi)
    return X, y

def subsample(df, input_length=10, output_length=1, horizon=0, target_col='GDPC1'):
    subseq = subsequence(df, input_length + horizon + output_length)
    X = subseq[:input_length]
    y = subseq[-output_length:][target_col]
    if y.isnull().sum() > 0 or X.isnull().sum().sum() > 0:
        return subsample(df, input_length, output_length, horizon, target_col)
    return X, y

def subsequence(df, length):
    '''
    Given the initial dataframe `df`, return two shorter dataframe sequences of length `length`.
    This shorter sequence should be selected at random
    '''
    max_start = len(df) - length
    start = np.random.randint(0, max_start)
    end = start + length
    return df.iloc[start:end]
