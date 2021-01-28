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
            response = self.client.post('/decision', data={'model': 1})
            self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_request_model_id_required(self):
        """
        Test if model id is required on POST.
        """
        with self.client:
            response = self.client.get('/decision')
            self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_request_id_required(self):
        """
        Tests if an error is sent if there is no request id in the request.
        """
        with self.client:
            response = self.client.get('/decision/')
            self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    @patch('brain_server.services.action_service.ActionService.request_actions',
           Mock(return_value=1))
    def test_decision_obs_in_data(self):
        """
        The Unity Engine does not support sending a list in a field. Therefore it send in 'data'.
        """
        with self.client:
            data = dict(color=1, model=1)
            response = self.client.post('/decision', data=data)
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(1, response.json['request'])

    @patch('brain_server.services.action_service.ActionService.request_actions',
           Mock(return_value=1))
    def test_action_is_request(self):
        """
        Test request ID is returned.
        """
        with self.client:
            data = dict(model=1, obs=dict(color=1))
            response = self.client.post('/decision', json=data)
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(1, response.json['request'])

    @patch('brain_server.services.action_service.ActionService.get_actions',
           Mock(return_value=['left']))
    def test_action_is_returned(self):
        """
        Test action are returned.
        """
        with self.client:
            response = self.client.get('/decision/1')
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(['left'], response.json['action'])
