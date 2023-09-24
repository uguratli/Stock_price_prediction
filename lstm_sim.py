from sklearn.preprocessing import MinMaxScaler 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import math

def model(delta):
    """LSTM model.
    """
    model = keras.Sequential()
    model.add(layers.LSTM(100, return_sequences=True, input_shape=(delta, 1)))
    model.add(layers.LSTM(100, return_sequences=False))
    model.add(layers.Dense(25))
    model.add(layers.Dense(1))

    print(model.summary())
    return model