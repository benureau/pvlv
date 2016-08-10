
class Network(object):
    """Leabra Network class"""

    def __init__(self):
        self.layers = []
        self.connections = []

    def add_connection(self, connection):
        self.connections.append(connection)

    def add_layer(self, layer):
        self.layers.append(layer)

    def cycle(self):
        for conn in self.connections:
            conn.cycle()
        for layer in self.layers:
            layer.cycle()
