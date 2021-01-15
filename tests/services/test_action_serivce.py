from unittest.mock import Mock, patch, MagicMock

from brain_server.services.action_service import ActionService
from tests.BaseTestCase import BaseTestCase


class ActionServiceTest(BaseTestCase):
    """
    Test the action service.
    """

    @patch('brain_server.task.get_result', return_value=Mock(result='2'))
    def test_get_action_done(self, _):
        """
        Tests if the action returned if the task is done.
        """
        result = ActionService.get_actions('1')
        self.assertEqual('2', result)

    @patch('brain_server.task.get_result',
           return_value=MagicMock(status=Mock(
               return_value='PENDING'), ready=Mock(
               return_value=False)))
    def test_get_action_not_done(self, _):
        """
        Test if the pending status is returned, if the task is not done yet.
        """
        result = ActionService.get_actions('1')
        self.assertEqual('PENDING', result)
