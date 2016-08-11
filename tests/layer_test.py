import os
import unittest
import random

import dotdot
from leabra import Layer, LayerSpec



class LayerTests(unittest.TestCase):
    """Diverse checks on Layer behavior."""

    def test_set_activities(self):
        layer = Layer(4)
        acts = [0.31, 0.63, -1.0, 1.0]
        layer.set_activities(acts)

        self.assertEqual(layer.activities, acts)


if __name__ == '__main__':
    unittest.main()
