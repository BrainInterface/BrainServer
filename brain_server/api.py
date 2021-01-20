from flask import Blueprint, request
from flask_api import status
from werkzeug.datastructures import MultiDict

from brain_server.services.action_service import ActionService

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return {'status': 'Server up'}


@api.route('/decision', methods=['GET', 'POST'])
def decision_request():
    """
    GET: tries to the action for an request. If not done will sent progress status.
    POST: user requests an action for a given set of observations.
    """
    if request.method == 'POST':
        observations, model_id = _get_obs()
        if model_id is None:
            model_id: str = request.form.get('model_id')
        if observations is None or len(observations) == 0:
            return {'error': 'No Observation sent.'}, status.HTTP_400_BAD_REQUEST
        request_id = ActionService.request_actions(observations, model_id)
        return {'request': request_id}, status.HTTP_200_OK
    request_id = request.form.get('request')
    if request_id is None:
        return {'error': 'No request ID was sent.'}, status.HTTP_400_BAD_REQUEST
    return {'action': ActionService.get_actions(request_id)}, status.HTTP_200_OK


def _get_obs():
    if request.form.getlist('obs'):
        return request.form.getlist('obs'), None
    data:dict = request.data
    model_id = data['model']
    del data['model']
    return data, model_id

