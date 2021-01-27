from logging import log
from typing import Any, Dict

from tensorflow import keras

from brain_server.celery_worker import celery, AgentTask
from deep_rl.car_agent import pre_process


@celery.task(base=AgentTask, track_started=True)
def send_observation(observations: Dict[str, Any],
                     model_id: str):
    """
    Sends observation to the neuronal network and returns the id for the task.
    :param observations: Dictionary containing string keys and any type of values.
    them.
    :param model_id: the hash id of the model.
    :return: The hash id of the task which is a string.
    """
    log(level=10, msg=send_observation.agents)
    model = send_observation.agents.get(model_id)
    if isinstance(model, keras.Model):
        obs = list(observations.values())
        inputs = pre_process(obs[0])
        log(10, inputs)
        actions = model(inputs).numpy().flatten().tolist()
        log(10, actions)
        return actions
    else:
        error_message = f'Currently only keras models are supported but was {type(model)}'
        log(level=40, msg=error_message)
        ValueError(error_message)
