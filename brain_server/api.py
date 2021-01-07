from flask import Blueprint, request

api = Blueprint('api', __name__)


@api.route('/')
def hello_world():
    return 'Hello World!'


@api.route('/decision', methods=['POST'])
def decision_request():
    observations = request.form.getlist('obs')
    if observations is None:
        return {'error': 'No Observation sent.'}
