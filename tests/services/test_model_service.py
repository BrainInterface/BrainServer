import os

import torch

from brain_server.services.model_service import load_model, save_model
from tests.BaseTestCase import BaseTestCase


class TestTorchModel(torch.nn.Module):
    """
    Empty class representing a torch module.
    """
    # pylint: disable=no-self-use
    def forward(self, x):
        return x


class ModelServiceTest(BaseTestCase):
    """
    Tests the model service.
    """

    def setUp(self) -> None:
        self.path = 'data/test_model.pt'
        if os.path.exists(self.path):
            os.remove(self.path)
        self.model = TestTorchModel()

    def tearDown(self) -> None:
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_load_torch_model(self):
        """
        Tests if a saved model is loaded corrected.
        """
        torch.save(self.model.state_dict(), self.path)
        test_model = load_model(self.path, model_type='pytorch', ModelClass=TestTorchModel)
        self.assertIsNotNone(self.model, test_model)

    def test_load_torch_model_with_guessing(self):
        """
        Tests if a saved model is loaded corrected without given type.
        """
        torch.save(self.model.state_dict(), self.path)
        test_model = load_model(self.path, ModelClass=TestTorchModel)
        self.assertIsNotNone(self.model, test_model)

    def test_save_torch_model(self):
        """
        Tests if the model is saved correctly.
        """
        save_model(self.path, self.model, model_type='pytorch')
        self.assertTrue(os.path.exists(self.path))

    def test_save_torch_model_with_guessing(self):
        """
        Tests if the model is saved correctly.
        """
        save_model(self.path, self.model)
        self.assertTrue(os.path.exists(self.path))
