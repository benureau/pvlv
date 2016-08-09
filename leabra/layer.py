from .unit import Unit


class LayerSpec:
    """Layer parameters"""

    def __init__(self):
        self.kwta_pct = 0.25 # proportion of active units
        self.q = 0.25  # see eq. A6


class Layer:
    """Leabra Layer class"""

    def __init__(self, size, spec=None, unit_spec=None):
        """
        size     :  Number of units in the layer.
        spec     :  LayerSpec instance with custom values for the parameter of
                    the layer. If None, default values will be used.
        unit_spec:  UnitSpec instance with custom values for the parameters of
                    the units of the layer. If None, default values will be used.
        """
        self.spec = spec
        if self.spec is None:
            self.spec = LayerConstants()

        self.size = size
        self.units = [Unit(spec=unit_spec) for _ in range(self.size)]

        self.g_i = 0.0

    @property
    def k(self):
        """Derived from cst.kwta_pct, the number of inhibited units"""
        return int((1 - self.spec.kwta_pct) * self.size)

    @property
    def activities(self):
        """Return the matrix of the units's activities"""
        return [u.act for u in self.units]

    def set_activities(self, inputs):
        """Set the units's activities equal to the inputs"""
        assert len(inputs) == self.size
        for u, inp in zip(self.units, inputs):
            u.set_activity(inp)

    def _active_threshold(self, u):
        """Threshold of kWTA inhibition. See eq. A7."""
        g_e_star = u.g_e - u.spec.bias/self.size
        return (  u.spec.g_bar_e * g_e_star   * (u.spec.e_rev_e - u.spec.act_thr)  # eq. A7
                + u.spec.g_bar_l * u.spec.g_l * (u.spec.e_rev_l - u.spec.act_thr)
               ) / (u.spec.act_thr - u.spec.e_rev_i)

    def _inhibition(self):
        """Compute inhibition"""
        g_thrs = [self._active_threshold(u) for u in self.units]
        g_thrs.sort()
        return g_thrs[self.k] + self.spec.q * (g_thrs[self.k] - g_thrs[self.k-1])

    def cycle(self, inputs):
        """Update the state of the layer"""
        assert len(inputs) == self.size
        self.g_i = self._inhibition()
        for u, net_raw in zip(self.units, inputs):
            u.cycle(net_raw, g_i=self.g_i)
