from unittest import TestCase

import numpy as np

from deep_rl.car_agent import pre_process, create_car_agent


class CarAgent(TestCase):
    """
    Tests the car agents methods.
    """

    def test_pre_process(self):
        """
        Tests the preprocessing.
        """
        inputs = ["3", "4"]
        nn_inputs = pre_process(inputs)
        np.testing.assert_array_equal(np.array(([3], [4])), nn_inputs)

    def test_model_is_created(self):
        self.assertIsNotNone(create_car_agent())
