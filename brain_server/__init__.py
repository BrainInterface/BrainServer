import os
from typing import Any, Dict

from flask_api import FlaskAPI
from flask_migrate import Migrate

from brain_server.celery_worker import celery
from brain_server.models import db
from brain_server.models.agent import Agent
from brain_server.services.model_service import save_model
from deep_rl.car_agent import create_car_agent

agents = dict()


def create_app(test_config: Dict[str, Any] = None, instance_path: str = None) -> FlaskAPI:
    """
    Creates the flask application.
    :param test_config: this parameter is for testing only
    :param instance_path: the path where the application runs
    :return: a flask api application
    """
    app = FlaskAPI(__name__, instance_relative_config=True, instance_path=instance_path)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'very-secret-key',
        DATABASE_URL_TEMPLATE=f'sqlite:///{app.instance_path}/app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CELERY_RESULT_BACKEND='redis://localhost:6379/1',
        CELERY_TASK_TRACK_STARTED=True,
        CELERY_IGNORE_RESULT=False
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or app.config[
        'DATABASE_URL_TEMPLATE'].format(instance_path=app.instance_path)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    celery.conf.update(app.config)

    # pylint: disable=import-outside-toplevel
    from brain_server.api import api
    app.register_blueprint(api)

    if os.path.exists(app.instance_path + '/app.db'):
        Migrate(app, db)
    db.init_app(app)
    db.app = app
    db.create_all()

    _test_model(app)

    return app


def _test_model(app):
    if not Agent.query.get(1):
        keras_model = create_car_agent()
        keras_model.compile()
        save_model(app.instance_path, keras_model, 'keras')
