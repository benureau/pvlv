"""Leabra library

The code is object-oriented, and follow a hierachical structure. At the bottom,
`Unit` instance handle neural computations, while `Layer` instances regroup
units and take care of inhibition. `Connection` link layer, and are where
learning happens. The `Network` regroups everything, call `cycle()` function
and broadcast the ends of the minus and plus phases.
"""


from .unit       import Unit, UnitSpec
from .layer      import Layer, LayerSpec
from .connection import Connection, ConnectionSpec
from .network    import Network, NetworkSpec
