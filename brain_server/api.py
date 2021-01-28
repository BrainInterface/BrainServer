from flask import Blueprint, request
from flask_api import status

from brain_server.services.action_service import ActionService

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return {'status': 'Server up'}


@api.route('/decision', methods=['POST'])
def decision_request():
    """
    POST: user requests an action for a given set of observations.
    """
    if request.method == 'POST':
        observations, model_id = _get_obs()
        if model_id is None:
            model_id: str = request.form.get('model_id')
        if observations is None or len(observations) == 0:
            return {'error': 'No Observation sent.'}, status.HTTP_400_BAD_REQUEST
        request_id = ActionService.request_actions(dict(observations), model_id)
        return {'request': request_id}, status.HTTP_200_OK


@api.route('/decision/<request_id>', methods=['GET'])
def action_request(request_id):
    """
    GET: tries to the action for an request. If not done will sent progress status.
    :param request_id: the hash id of the request.
    :return: The actions or the status of the task.
    """
    if request_id is None:
        return {'error': 'No request ID was sent.'}, status.HTTP_400_BAD_REQUEST
    task_status, actions = ActionService.get_actions(request_id)
    return {'status': task_status, 'action': actions}, status.HTTP_200_OK


def _get_obs():
    data: dict = request.data
    model_id = data['model']
    del data['model']
    return data, model_id
