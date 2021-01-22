import os
from typing import Any, Dict

from flask_api import FlaskAPI
from flask_migrate import Migrate

from brain_server.celery_worker import celery
from models import db


def create_app(test_config: Dict[str, Any] = None, instance_path: str = None) -> FlaskAPI:
    app = FlaskAPI(__name__, instance_relative_config=True, instance_path=instance_path)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'very-secret-key',
        DATABASE_URL_TEMPLATE=f'sqlite:///{app.instance_path}/app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
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

    return app
