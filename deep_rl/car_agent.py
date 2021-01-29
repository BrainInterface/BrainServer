import numpy as np

from tensorflow import keras


def pre_process(inputs: str) -> np.ndarray:
    """
    Preprocesses the input to for the NN input.
    :param inputs: as json string
    :return: input values as numpy array
    """
    color = np.array(float(inputs.lstrip('<').split(',')[0]))
    color = np.expand_dims(color, axis=0)
    return color


def create_car_agent() -> keras.Model:
    """
    Create a model that controls the car from the demo environment
    """
    input_layer = keras.Input(shape=(1,))
    output_layer = keras.layers.Dense(1)(input_layer)
    return keras.Model(input_layer, output_layer)
