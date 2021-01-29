from typing import List

import numpy as np
from tensorflow import keras


def pre_process(inputs: List[str]) -> np.ndarray:
    """
    Preprocesses the input to for the NN input.
    :param inputs: as json string
    :return: input values as numpy array
    """
    obs_values: list = list()
    for observation in inputs:
        obs_value = np.array(float(observation.lstrip('<').split(',')[0]))
        obs_values.append(np.expand_dims(obs_value, axis=0))
    return np.array(obs_values)


def create_car_agent() -> keras.Model:
    """
    Create a model that controls the car from the demo environment
    """
    input_layer = keras.Input(shape=(1,))
    output_layer = keras.layers.Dense(1)(input_layer)
    return keras.Model(input_layer, output_layer)
