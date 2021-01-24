from typing import Any, Dict

from tensorflow import keras

from brain_server import models
from brain_server.celery_worker import celery
from deep_rl.car_agent import pre_process


@celery.task(track_started=True)
def send_observation(observations: Dict[str, Any],
                     model_id: str) -> str:
    """
    Sends observation to the neuronal network and returns the id for the task.
    :param observations: Dictionary containing string keys and any type of values.
    them.
    :param model_id: the hash id of the model.
    :return: The hash id of the task which is a string.
    """
    model = models.get(model_id)
    if isinstance(model, keras.Model):
        obs = list(observations.values())
        inputs = pre_process(obs[0])
        return model(inputs).numpy()
    else:
        ValueError(f'Currently only keras models are supported but was {type(model)}')
