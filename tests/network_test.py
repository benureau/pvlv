import os
import unittest
import random

import dotdot
import leabra


class NetworkTests(unittest.TestCase):
    """Diverse checks on Network behavior."""

    def test_settle(self):
        netspec = leabra.NetworkSpec(settle=15)
        net = leabra.Network(spec=netspec)

        self.assertEqual(net.cycles, 0)
        net.cycle()
        self.assertEqual(net.cycles, 1)
        net.cycle()
        self.assertEqual(net.cycles, 2)
        net.settle()
        self.assertEqual(net.cycles, 15)

        for k in range(10):
            for _ in range(random.randint(0, 14)):
                net.cycle()
            net.settle()
            self.assertEqual(net.cycles, 15*(k+2))

if __name__ == '__main__':
    unittest.main()
