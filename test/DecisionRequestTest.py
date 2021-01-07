from flask_api.status import HTTP_400_BAD_REQUEST

from test.BaseTestCase import BaseTestCase


class DecisionTest(BaseTestCase):
    def test_obs_required(self):
        """
        Tests if an error is returned if no observation are sent.
        """
        with self.client:
            response = self.client.post('/decision', data=[])
            self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)
