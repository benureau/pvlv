from .unit import Unit


class LayerSpec:
    """Layer parameters"""

    legal_inhib = 'kwta', 'kwta_avg'  # available values for self.inhib

    def __init__(self, **kwargs):
        self.inhib    = 'kwta'   # inhibition rule: 'kwta' or 'kwta_avg'
        self.k        = None     # number of active units.
        self.kwta_pct = 0.25     # proportion of active units; used to compute k
                                 # only if self.k is None.
        self.q        = 0.25     # see eq. A6

        for key, value in kwargs.items():
            setattr(self, key, value)


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
            self.spec = LayerSpec()
        assert self.spec.inhib.lower() in self.spec.legal_inhib

        self.size = size
        self.units = [Unit(spec=unit_spec) for _ in range(self.size)]

        self.g_i = 0.0

    @property
    def k(self):
        """Derived from cst.kwta_pct, the number of inhibited units"""
        if self.spec.k is None:
            return int(self.spec.kwta_pct * self.size)
        else: return self.spec.k

    @property
    def activities(self):
        """Return the matrix of the units's activities"""
        return [u.act for u in self.units]

    def set_activities(self, inputs):
        """Set the units's activities equal to the inputs"""
        assert len(inputs) == self.size
        for u, inp in zip(self.units, inputs):
            u.act = inp

    def _active_threshold(self, u):
        """Threshold of kWTA inhibition. See eq. A7."""
        g_e_star = u.g_e - u.spec.bias/self.size
        return (  u.spec.g_bar_e * g_e_star   * (u.spec.e_rev_e - u.spec.act_thr)  # eq. A7
                + u.spec.g_bar_l * u.spec.g_l * (u.spec.e_rev_l - u.spec.act_thr)
               ) / (u.spec.act_thr - u.spec.e_rev_i)

    def _inhibition(self):
        """Compute inhibition"""
        g_thrs = [self._active_threshold(u) for u in self.units]
        g_thrs.sort(reverse=True)
        if self.k >= self.size:  # no inhibition
            return g_thrs[-1] - 0.01  # HACKISH
        if self.k == 0:          # every unit is inhibited
            return g_thrs[0]

        # non-extreme cases
        if self.spec.inhib.lower() == 'kwta':
            return g_thrs[self.k] + self.spec.q * (g_thrs[self.k-1] - g_thrs[self.k])  # eq. A6
        else:  # self.spec.inhib == 'avg_kwta'
            top_avg, bottom_avg = np.mean(g_thrs[:k]), np.mean(g_thrs[k+1:])
            return top_avg + self.spec.q * (top_avg - bottom_avg)  # eq. 3.6 [CECN1]

    def add_excitatory(self, inputs, forced_act=False):
        assert len(inputs) == self.size
        for u, net_raw in zip(self.units, inputs):
            u.add_excitatory(net_raw, forced_act=forced_act)

    def cycle(self):
        """Update the state of the layer"""
        self.g_i = self._inhibition()
        for u in self.units:
            u.cycle(g_i=self.g_i)


# class ScalarVarLayer(Layer):
#
#     @property
#     def value(self):
#
