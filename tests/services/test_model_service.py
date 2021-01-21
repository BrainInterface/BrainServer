import os

import torch
from tensorflow import keras

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
        self.torch_path = 'data/test_torch.pt'
        self.keras_path = 'data/test_keras'
        if os.path.exists(self.torch_path):
            os.remove(self.torch_path)
        self.torch_model = TestTorchModel()
        inputs = keras.Input(shape=(32,))
        outputs = keras.layers.Dense(1)(inputs)
        self.keras_model = keras.Model(inputs, outputs)
        self.keras_model.compile()

    def tearDown(self) -> None:
        if os.path.exists(self.torch_path):
            os.remove(self.torch_path)

    def test_load_torch_model(self):
        """
        Tests if a saved model is loaded corrected.
        """
        torch.save(self.torch_model.state_dict(), self.torch_path)
        test_model = load_model(self.torch_path, model_type='pytorch', ModelClass=TestTorchModel)
        self.assertIsNotNone(self.torch_model, test_model)

    def test_load_torch_model_with_guessing(self):
        """
        Tests if a saved model is loaded corrected without given type.
        """
        torch.save(self.torch_model.state_dict(), self.torch_path)
        test_model = load_model(self.torch_path, ModelClass=TestTorchModel)
        self.assertIsNotNone(self.torch_model, test_model)

    def test_save_torch_model(self):
        """
        Tests if the model is saved correctly.
        """
        save_model(self.torch_path, self.torch_model, model_type='pytorch')
        self.assertTrue(os.path.exists(self.torch_path))

    def test_save_torch_model_with_guessing(self):
        """
        Tests if the model is saved correctly.
        """
        save_model(self.torch_path, self.torch_model)
        self.assertTrue(os.path.exists(self.torch_path))

    def test_load_keras_model(self):
        """
        Tests if a keras model is loaded correctly.
        """
        self.keras_model.save(self.keras_path)
        test_model = load_model(self.keras_path, 'keras')
        self.assertIsNotNone(test_model)

    def test_load_wrong_model(self):
        """
        Tests for not supported model type.
        """
        with self.assertRaises(ValueError):
            load_model(self.keras_path, model_type='.abc')

    def test_save_keras_model(self):
        """
        Tests if a keras model is saved correctly.
        """
        save_model(self.keras_path, self.keras_model, model_type='keras')

    def test_save_keras_model_with_guessing(self):
        """
        Tests if a keras model is saved correctly.
        """
        save_model(self.keras_path + '.pb', self.keras_model)

    def test_save_not_supported_extension(self):
        """
        Test if path has a non supported extension.
        """
        with self.assertRaises(IOError):
            save_model(self.keras_path + '.non', self.keras_model)

    def test_save_not_supported_model(self):
        """
        Test if a non supported model saving throws error.
        """
        with self.assertRaises(ValueError):
            save_model(self.keras_path, model=None, model_type='.abc')
