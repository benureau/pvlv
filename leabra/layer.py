import numpy as np

from .unit import Unit


class LayerConstants(object):
    """Layer constants."""

    def __init__(self):
        self.kwta_pct = 0.25 # proportion of active units
        self.q = 0.25  # see eq. A6


class Layer(object):
    """Leabra Layer class"""

    def __init__(self, shape, params=None):
        """
        shape:  dimension of the layer matrix (row, columns)
        """
        self.cst = params
        if self.cst is None:
            self.cst = LayerConstants()

        self.shape = shape
        self.N = shape[0]*shape[1]
        self.k = int((1-self.cst.kwta_pct)*len(self))
        assert 0 < self.k < self.N

        self.units = [[Unit() for j in range(shape[1])]
                              for i in range(shape[0])]
        self.g_i = 0.0

    def __len__(self):
        """Return the number of units in the layer"""
        return self.shape[0]*self.shape[1]

    @property
    def activities(self):
        """Return the matrix of the units's activities"""
        return np.array([[self.units[i][j].act for j in range(self.shape[1])]
                                               for i in range(self.shape[0]) ])


    def set_activities(self, inputs):
        """Set the units's activities equal to the inputs"""
        for (i, j), inp in np.ndenumerate(inputs):
            self.units[i][j].set_activity(inp)

    def active_threshold(self, u):
        """Threshold of kWTA inhibition. See eq. A7."""
        g_e_star = u.g_e - u.cst.bias/self.N
        return (  u.cst.g_bar_e * g_e_star  * (u.cst.e_rev_e - u.cst.act_thr)  # eq. A7
                + u.cst.g_bar_l * u.cst.g_l * (u.cst.e_rev_l - u.cst.act_thr)
                )/ (u.cst.act_thr - u.cst.e_rev_i)

    def inhibition(self):
        """Compute inhibition"""
        g_thrs = [self.active_threshold(u) for _, u in np.ndenumerate(self.units)]
        g_thrs.sort()
        return g_thrs[self.k] + self.cst.q * (g_thrs[self.k] - g_thrs[self.k-1])

    def cycle(self, inputs):
        """Update the state of the layer"""
        self.g_i = self.inhibition()
        inputs = np.array(inputs)
        assert inputs.shape == self.shape
        for (i, j), net_raw in np.ndenumerate(inputs):
            self.units[i][j].cycle(net_raw, g_i=self.g_i)
