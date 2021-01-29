import os
from shutil import rmtree

from flask_testing import TestCase

import brain_server


class BaseTestCase(TestCase):
    """
    Basic Test Case that setups the flask app.
    """
    def create_app(self):
        """
        Creates a test app.
        """
        instance_path = os.path.join(os.path.dirname(__file__), 'instance')

        app = brain_server.create_app({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False
        }, instance_path)
        return app

    def tearDown(self) -> None:
        rmtree(self.app.instance_path)
