import os
from typing import Any

from flask_api import FlaskAPI


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

    from brain_server.api import api
    app.register_blueprint(api)

    return app

