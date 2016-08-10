
class Link:
    """A link between two units. Simple, non active class."""

    def __init__(self, pre_unit, post_unit, w0):
        self.pre  = pre_unit
        self.post = post_unit
        self.wt   = w0


class ConnectionSpec:

    def __init__(self, **kwargs):
        """Connnection parameters"""
        self.st    = 1.0     # connection strength
        self.force = 1.0     # activity are set directly in the post_layer
        self.inhib = False   # if True, inhibitory connection
        self.w0    = 1.0     # intial weights
        self.proj  = 'Full'  # connection pattern between units.
                             # Can be 'Full' or 'OneToOne'. In the latter case,
                             # the layers must have the same size.
        self.lrate = 0.01    # learning rate (#FIXME not implemented yet)

        for key, value in kwargs.items():
            setattr(self, key, value)

class Connection:
    """Connection between layers"""

    def __init__(self, pre_layer, post_layer, spec=None):
        """
        Parameters:
            pre_layer   the layer sending its activity.
            post_layer  the layer receiving the activity.
        """
        self.pre   = pre_layer
        self.post  = post_layer
        self.spec = spec
        if self.spec is None:
            self.spec = ConnectionSpec()

        # creating unit-to-unit links
        self.links = []
        assert self.spec.proj in ('Full', 'OneToOne')
        if self.spec.proj == 'OneToOne':
            assert self.pre.size == self.post.size
            for pre_u, post_u in zip(self.pre.units, self.post.units):
                self.links.append(Link(pre_u, post_u, self.spec.w0))
        else:
            for pre_u in self.pre.units:
                for post_u in self.post.units:
                    self.links.append(Link(pre_u, post_u, self.spec.w0))

    def cycle(self):
        """Transmit activity, compute weight changes."""
        # transmit activity
        for link in self.links:
            scaled_act = self.spec.st * link.wt * link.pre.act
            link.post.add_excitatory(scaled_act, forced_act=self.spec.force)

        #TODO learning/weight changes
