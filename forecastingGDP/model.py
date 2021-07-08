import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline

from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.optimizers import RMSprop

from forecastingGDP.preprocessing import preprocessor

def pipeline():
    return Pipeline([
        ('preprocessor', preprocessor()),
        ('model', model()),
    ])

def model():
    import ipdb; ipdb.set_trace()
    return KerasRegressor(build_fn=new_rnn_model)

def new_rnn_model(input_shape=(6, 28), output_shape=1, **kwargs):
    model = models.Sequential([
        layers.LSTM(50, return_sequences=True, activation='tanh', input_shape=input_shape),
        layers.LSTM(20, activation='tanh'),
        layers.Dense(5, activation='relu'),
        layers.Dense(output_shape, activation='linear'),
    ])
    model.compile(
        loss='mean_squared_error',
        optimizer=RMSprop(),
        metrics=['mae','mape'],
    )
    return model
