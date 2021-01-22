from celery import Celery

CELERY_BROKER_RULE='redis://localhost:6379/0'
CELERY_RESULT_BACKEND='redis//localhost:6379/0'
celery = Celery('BrainServer', broker=CELERY_BROKER_RULE, include=['brain_server.task'])
