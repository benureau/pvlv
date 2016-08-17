import unittest

import numpy as np

import dotdot  # pylint: disable=unused-import
import leabra


class LayerTests(unittest.TestCase):
    """Diverse checks on Layer behavior."""

    def test_set_activities(self):
        layer = leabra.Layer(4)
        acts = [0.31, 0.63, -1.0, 1.0]
        layer.set_activities(acts)

        self.assertEqual(layer.activities, acts)

    def test_inhibition(self):
        inputs = np.linspace(0.5, 1.1, num=10)

        for k in range(11):
            layer_spec = leabra.LayerSpec(k=k)
            layer = leabra.Layer(10, spec=layer_spec)
            for _ in range(100):
                layer.add_excitatory(inputs)
                layer.cycle()

            self.assertEqual(len(np.nonzero(layer.activities)[0]), k)


if __name__ == '__main__':
    unittest.main()
