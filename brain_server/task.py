from typing import Any, Dict

from tensorflow import keras

from brain_server import models
from brain_server.celery_worker import celery
from deep_rl.car_agent import pre_process


def get_result(task_id: str) -> celery.AsyncResult:
    """
    Returns the async result of the task.
    :param task_id: Is the id of the task for which the result is requested.
    :return: The AsyncResult object.
    """
    return celery.AsyncResult(id=task_id)


@celery.task()
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
