import os
import unittest
import random

import dotdot
from leabra import Connection, ConnectionSpec
from leabra import Layer


class ConnectionTests(unittest.TestCase):
    """Diverse checks on Connection behavior."""

    def test_lrule(self):
        L1, L2 = Layer(2), Layer(2)
        conspec = ConnectionSpec(lrule='xcal')
        conn    = Connection(L1, L2, conspec)

        with self.assertRaises(NotImplementedError):
            conn.cycle()

if __name__ == '__main__':
    unittest.main()
