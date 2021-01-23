import numpy as np

from tensorflow import keras


def pre_process(inputs: str) -> np.ndarray:
    color = np.array(float(inputs.lstrip('<').split(',')[0]))
    color = np.expand_dims(color, axis=0)
    return color


def create_car_agent():
    input_layer = keras.Input(shape=(1,))
    output_layer = keras.layers.Dense(1)(input_layer)
    return keras.Model(input_layer, output_layer)
