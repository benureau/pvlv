class NetworkSpec:
    """Network parameters"""

    def __init__(self, **kwargs):
        # time step constants
        self.settle = 15  # number of cycles in a settle period

        for key, value in kwargs.items():
            setattr(self, key, value)


class Network:
    """Leabra Network class"""

    def __init__(self, spec=None, layers=(), connections=()):
        self.spec = spec
        if self.spec is None:
            self.spec = NetworkSpec()

        self.cycles = 0 # how many cycle happened
        self.layers = list(layers)
        self.connections = list(connections)

    def add_connection(self, connection):
        self.connections.append(connection)

    def add_layer(self, layer):
        self.layers.append(layer)

    def cycle(self):
        for conn in self.connections:
            conn.cycle()
        for layer in self.layers:
            layer.cycle()
        self.cycles += 1

    def settle(self):
        n = self.spec.settle - (self.cycles % self.spec.settle)
        for _ in range(n):
            self.cycle()

    def end_minus_phase(self):
        """End of the minus phase. Current unit activity is stored."""
        for layer in self.layers:
            for unit in layer.units:
                unit.act_m = unit.act

    def end_plus_phase(self):
        """End of the plus phase. Connections change weights."""
        for conn in self.connections:
            conn.learn()
