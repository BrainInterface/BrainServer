from unittest.mock import Mock, patch, MagicMock

from brain_server.services.action_service import ActionService
from tests.base_test_case import BaseTestCase


class ActionServiceTest(BaseTestCase):
    """
    Test the action service.
    """

    @patch('brain_server.task.send_observation.AsyncResult', return_value=Mock(result='2',
                                                                               status='SUCCESS'))
    def test_get_action_done(self, _):
        """
        Tests if the action returned if the task is done.
        """
        status, result = ActionService.get_actions('1')
        self.assertEqual('2', result)
        self.assertEqual('SUCCESS', status)

    @patch('brain_server.task.send_observation.AsyncResult',
           return_value=MagicMock(status='STARTED', ready=Mock(
               return_value=False)))
    def test_get_action_not_done(self, _):
        """
        Test if the pending status is returned, if the task is not done yet.
        """
        status, result = ActionService.get_actions('1')
        self.assertEqual('STARTED', status)
        self.assertIsNone(result)

    @patch('brain_server.task.send_observation.delay', return_value=MagicMock(id='abc123'))
    def test_request_action(self, _):
        """
        Tests if the task is returned upon requesting an action.
        """
        obs = dict(color='blue')
        model_id = 1
        task_id = ActionService.request_actions(obs, model_id)
        self.assertEqual('abc123', task_id)
