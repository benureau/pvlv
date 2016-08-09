import os
import unittest
import random

import dotdot
from leabra import Unit, UnitSpec



class UnitTests(unittest.TestCase):
    """Diverse checks on Unit behavior."""

    def test_xx1(self):
        u_spec = UnitSpec()
        u_spec.act_thr = 0.25
        u = Unit(spec=u_spec)
        self.assertEqual(u.xx1(0.20), 0.0)
        self.assertTrue(u.xx1(0.30) > 0.0)
        self.assertTrue(u.noisy_xx1(0.20) > 0.0)
        self.assertTrue(u.noisy_xx1(0.30) > 0.0)


if __name__ == '__main__':
    unittest.main()
