from flask_api import status

from tests.BaseTestCase import BaseTestCase


class IndexTest(BaseTestCase):
    """
    Tests the index route behaviour.
    """

    def test_index(self):
        """
        Tests the GET method of index.
        """
        with self.client:
            response = self.client.get('/')
            self.assertEqual({'status': 'Server up'}, response.json)
