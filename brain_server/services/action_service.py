from typing import Any, List, Union, Dict

from brain_server import task


# pylint: disable=unsubscriptable-object
class ActionService:

    @classmethod
    def get_actions(cls, request_id: str) -> Union[float, List[Any]]:
        """
        Ask the background task for the results. It will return the actions asked for if the back-
        ground task is done, or the status of it.
        :param request_id: The task id for which the result are requested.
        :return: If the task is complete it will return the actions of that task or the status of
        it.
        """
        result = task.get_result(request_id)
        if result.ready():
            return result.result
        return result.status()

    @classmethod
    def request_actions(cls, observations: Dict[str, Any], model_id: str) -> str:
        """
        Creates a task to send the observation to a neural network (NN) and returns the id for the
        task.from celery import Celery

        :param observations: Dictionary containing string keys and any type of values.
        them.
        :param model_id: The model id for which the actions are requested.
        :return: The hash id of the task which is a string.
        """
        result = task.send_observation.delay(observations, model_id)
        return result.id
