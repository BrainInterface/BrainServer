from celery import Celery

CELERY_BROKER_RULE = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
celery = Celery('BrainServer', broker=CELERY_BROKER_RULE, backend=CELERY_RESULT_BACKEND,
                include=['brain_server.task'], ignore_result=False)
celery.Task.track_started = True
