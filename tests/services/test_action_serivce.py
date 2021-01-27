from unittest.mock import Mock, patch, MagicMock

from brain_server.services.action_service import ActionService
from tests.BaseTestCase import BaseTestCase


class ActionServiceTest(BaseTestCase):
    """
    Test the action service.
    """

    @patch('brain_server.task.send_observation.AsyncResult', return_value=Mock(result='2'))
    def test_get_action_done(self, _):
        """
        Tests if the action returned if the task is done.
        """
        result = ActionService.get_actions('1')
        self.assertEqual('2', result)

    @patch('brain_server.task.send_observation.AsyncResult',
           return_value=MagicMock(status='PENDING', ready=Mock(
               return_value=False)))
    def test_get_action_not_done(self, _):
        """
        Test if the pending status is returned, if the task is not done yet.
        """
        result = ActionService.get_actions('1')
        self.assertEqual('PENDING', result)

    def test_request_action(self):
        """
        Tests if the task is returned upon requesting an action.
        """
        obs = dict(color='blue')
        model_id = 1
        task_id = ActionService.request_actions(obs, model_id)
        self.assertTrue(isinstance(task_id, str))
