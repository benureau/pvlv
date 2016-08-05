from .unit import Unit


class LayerConstants(object):
    """Layer constants."""

    def __init__(self):
        self.kwta_pct = 0.25 # proportion of active units
        self.q = 0.25  # see eq. A6


class Layer(object):
    """Leabra Layer class"""

    def __init__(self, size, params=None):
        """
        size:  number of units in the layer
        """
        self.cst = params
        if self.cst is None:
            self.cst = LayerConstants()

        self.size = size
        self.units = [Unit() for _ in range(self.size)]

        self.g_i = 0.0

    @property
    def k(self):
        """Derived from cst.kwta_pct, the number of inhibited units"""
        return int((1 - self.cst.kwta_pct) * self.size)

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
        g_e_star = u.g_e - u.cst.bias/self.size
        return (  u.cst.g_bar_e * g_e_star  * (u.cst.e_rev_e - u.cst.act_thr)  # eq. A7
                + u.cst.g_bar_l * u.cst.g_l * (u.cst.e_rev_l - u.cst.act_thr)
                )/ (u.cst.act_thr - u.cst.e_rev_i)

    def _inhibition(self):
        """Compute inhibition"""
        g_thrs = [self._active_threshold(u) for u in self.units]
        g_thrs.sort()
        return g_thrs[self.k] + self.cst.q * (g_thrs[self.k] - g_thrs[self.k-1])

    def cycle(self, inputs):
        """Update the state of the layer"""
        assert len(inputs) == self.size
        self.g_i = self._inhibition()
        for u, net_raw in zip(self.units, inputs):
            u.cycle(net_raw, g_i=self.g_i)
