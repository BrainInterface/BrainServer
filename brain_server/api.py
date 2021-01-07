from flask import Blueprint, request
from flask_api.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from services.action_service import ActionService

api = Blueprint('api', __name__)


@api.route('/')
def hello_world():
    return 'Hello World!'


@api.route('/decision', methods=['POST'])
def decision_request():
    observations = request.form.getlist('obs')
    if observations is None or len(observations) == 0:
        return {'error': 'No Observation sent.'}, HTTP_400_BAD_REQUEST
    service = ActionService(observations)
    return {'action': service.get_actions()}, HTTP_200_OK
