from flask import Blueprint, request
from flask_api import status

from services.action_service import ActionService

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
        observations = request.form.getlist('obs')
        if observations is None or len(observations) == 0:
            return {'error': 'No Observation sent.'}, status.HTTP_400_BAD_REQUEST
        request_id = ActionService.request_actions(observations)
        return {'request': request_id}, status.HTTP_200_OK
    request_id = request.form.get('request')
    if request_id is None:
        return {'error': 'No request ID was sent.'}, status.HTTP_400_BAD_REQUEST
    return {'action': ActionService.get_actions(request_id)}, status.HTTP_200_OK

