import os
from typing import Any

from celery import Celery
from flask_api import FlaskAPI

CELERY_BROKER_RULE='redis://localhost:6379/0'
CELERY_RESULT_BACKEND='redis//localhost:6379/0'
celery = Celery('BrainServer', broker=CELERY_BROKER_RULE, include=['brain_server.task'])


def create_app(test_config: dict[str, Any] = None, instance_path: str = None) -> FlaskAPI:
    app = FlaskAPI(__name__, instance_relative_config=True, instance_path=instance_path)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'very-secret-key'
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    celery.conf.update(app.config)

    # pylint: disable=import-outside-toplevel
    from brain_server.api import api
    app.register_blueprint(api)

    return app
