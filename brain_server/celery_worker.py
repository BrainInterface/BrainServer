from celery import Celery, Task

from brain_server.services.model_service import load_model

CELERY_BROKER_RULE = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
celery = Celery('BrainServer', broker=CELERY_BROKER_RULE, backend=CELERY_RESULT_BACKEND,
                include=['brain_server.task'], ignore_result=False,
                accept_content='application/x-python-serialize')
celery.Task.track_started = True

# pylint=disable:abstract-method
class AgentTask(Task):

    def __init__(self):
        model = load_model('instance/', model_type='keras')
        self.agents = {'1': model}
