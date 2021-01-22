from typing import Any, Dict, Union

import torch
from celery.result import AsyncResult
from tensorflow import keras

from brain_server.celery_worker import celery


def get_result(task_id: str) -> AsyncResult:
    """
    Returns the async result of the task.
    :param task_id: Is the id of the task for which the result is requested.
    :return: The AsyncResult object.
    """
    return AsyncResult(id=task_id)


@celery.task()
def send_observation(observations: Dict[str, Any],
                     model: Union[torch.nn.Module, keras.Model]) -> str:
    """
    Sends observation to the neuronal network and returns the id for the task.
    :param observations: Dictionary containing string keys and any type of values.
    them.
    :param model: for which the observation are intended for.
    :return: The hash id of the task which is a string.
    """
    if isinstance(model, keras.Model):
        return model.call(observations)
    else:
        ValueError(f'Currently only keras models are supported but was {type(model)}')
