import os

import torch

from brain_server.services.model_service import load_model
from tests.BaseTestCase import BaseTestCase


class TestModel(torch.nn.Module):
    """
    Empty class representing a torch module.
    """
    pass


class ModelServiceTest(BaseTestCase):
    """
    Tests the model service.
    """
    def setUp(self) -> None:
        self.path = 'data/test_model.pt'
        if os.path.exists(self.path):
            os.remove(self.path)

    def tearDown(self) -> None:
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_load_model(self):
        """
        Tests if a saved model is loaded corrected.
        """
        model = TestModel()
        torch.save(model.state_dict(), self.path)
        test_model = load_model(self.path, model_type='pytorch', ModelClass=TestModel)
        self.assertIsNotNone(model, test_model)

    def test_load_model_with_guessing(self):
        """
        Tests if a saved model is loaded corrected without given type.
        """
        model = TestModel()
        torch.save(model.state_dict(), self.path)
        test_model = load_model(self.path, model_type=None, ModelClass=TestModel)
        self.assertIsNotNone(model, test_model)
