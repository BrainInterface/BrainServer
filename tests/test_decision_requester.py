from unittest.mock import patch, Mock

from flask_api import status

from tests.BaseTestCase import BaseTestCase


class DecisionTest(BaseTestCase):
    """
    Tests the process of requesting a decision via sending observations.
    """

    def test_obs_required(self):
        """
        Tests if an error is returned if no observation are sent.
        """
        with self.client:
            response = self.client.post('/decision', data=[])
            self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    @patch('services.action_service.ActionService.get_actions', Mock(return_value=['left']))
    def test_action_is_returned(self):
        """
        Test action are returned.
        """
        with self.client:
            data = dict(obs={'color': 1})
            response = self.client.post('/decision', data=data)
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(['left'], response.json['action'])
