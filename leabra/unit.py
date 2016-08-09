"""
Implementation of a Leabra Unit, as described in the CECN1 textbook,
and reproducing the behavior of emergent 5.0 units.

We implement only the rate-coded version. The code is intended to be
as simple as possible to understand. It is not in any way optimized
for performance.
"""
import numpy as np
import scipy.interpolate



class UnitSpec:
    """Units parameters.

    Each unit can have different parameters values. They don't change during
    cycles, and unless you know what you're doing, you should not change them
    after the Unit creation. The best way to proceed is to create the UnitSpec,
    modify it, and pass it to the Unit.__init__ method:

    >>> spec = UnitSpec()
    >>> spec.bias = 0.5
    >>> u = Unit(spec)

    """

    def __init__(self):
        # time step constants
        self.dt_net    = 0.7   # for net update (net = g_e * g_bar_e) (eq. 2.8)
        self.dt_vm     = 0.1   # for vm update (eq. 2.16)
        # input channels parameters (eq. 2.8)
        self.g_l       = 1.0   # leak current (constant)
        self.g_bar_e   = 0.4   # excitatory maximum conductance
        self.g_bar_i   = 1.0   # inhibitatory maximum conductance
        self.g_bar_l   = 2.8   # leak maximum conductance
        # reversal potential (eq. 2.8)
        self.e_rev_e   = 1.0   # excitatory
        self.e_rev_i   = 0.15  # inhibitatory
        self.e_rev_l   = 0.15  # leak
        # activation function parameters (eq. 2.19)
        self.act_thr   = 0.25  # threshold
        self.act_gain  = 600   # gain

        self.bias      = 0.0

        self.noisy_act = False # If True, uses the noisy activation function (eq A5)
        self.act_sd    = 0.005 # standard deviation of the noisy gaussian (eq A5)


class Unit:
    """Leabra Unit (as implemented in emergent 5.0)"""

    def __init__(self, spec=None):
        """
        spec:  UnitSpec instance with custom values for the unit parameters.
               If None, default values will be used.
        """
        self.spec = spec
        if self.spec is None:
            self.spec = UnitSpec()

        self.g_e   = 0
        self.I_net = 0
        self.v_m   = 0.15
        self.act   = 0

        self._nxx1_conv = None # precomputed convolution for the noisy xx1 function

        self.logs  = {'net': [], 'act': [], 'I_net': [], 'v_m': []}


    @property
    def net(self):
        """Excitatory conductance."""
        return self.spec.g_bar_e * self.g_e


    def cycle(self, net_raw, g_i=0.0, dt_integ=1):
        """
        net_raw: total, instantaneous, excitatory input for the neuron
        dt_integ: integration time step, in ms.
        """
        # updating net
        self.g_e += dt_integ * self.spec.dt_net * (net_raw - self.g_e)  # eq 2.16

        # computing I_net
        gc_e = self.spec.g_bar_e * self.g_e
        gc_i = self.spec.g_bar_i * g_i
        gc_l = self.spec.g_bar_l * self.spec.g_l
        self.I_net = (  gc_e * (self.spec.e_rev_e - self.v_m)  # eq 2.8
                      + gc_i * (self.spec.e_rev_i - self.v_m)
                      + gc_l * (self.spec.e_rev_l - self.v_m))

        # updating v_m
        self.v_m += dt_integ * self.spec.dt_vm * self.I_net  # eq 2.8

        # updating activity
        if self.spec.noisy_act:
            self.act = self.noisy_xx1(self.v_m)
        else:
            self.act = self.xx1(self.v_m)

        self.update_logs()

    def xx1(self, v_m):
        X = self.spec.act_gain * max((v_m - self.spec.act_thr), 0.0)
        return X / (X + 1) # eq 2.19

    def noisy_xx1(self, v_m):
        """Compute the noisy x/(x+1) function.

        The noisy x/(x+1) function is the convolution of the x/(x+1) function
        with a Gaussian with a `self.spec.act_sd` standard deviation. Here, we
        precompute the convolution as a look-up table, and interpolate it with
        the desired point every time the function is called.
        """
        if self._nxx1_conv is None: # we precompute the convolution.
            xs = np.linspace(-2.0, 2.0, 2000) # x represents (self.v_m - self.spec.act_thr)
            X  = self.spec.act_gain * np.maximum(xs, 0)
            xx1 = X / (X + 1) # regular x/(x+1) function over xs

            gaussian = (np.exp(-xs**2 / (2 * self.spec.act_sd**2)) /
                        (self.spec.act_sd * np.sqrt(2 * np.pi)))

            conv = np.convolve(xx1, gaussian, mode='same')/np.sum(gaussian)
            self._nxx1_conv = xs, conv

        x = v_m - self.spec.act_thr
        xs, conv = self._nxx1_conv
        return float(scipy.interpolate.interp1d(xs, conv, kind='linear',
                                                fill_value='extrapolate')(x))


    def update_logs(self):
        """Record current state. Called after each cycle."""
        self.logs['net'].append(self.net)
        self.logs['I_net'].append(self.I_net)
        self.logs['v_m'].append(self.v_m)
        self.logs['act'].append(self.act)


    def show_config(self):
        """Display the value of constants and state variables."""
        print('Constants:')
        for name in ['dt_vm', 'dt_net', 'g_l', 'g_bar_e', 'g_bar_l', 'g_bar_i',
                     'e_rev_e', 'e_rev_l', 'e_rev_i', 'act_thr', 'act_gain']:
            print('   {}: {:.2f}'.format(name, getattr(self.spec, name)))
        print('State:')
        for name in ['g_e', 'I_net', 'v_m', 'act']:
            print('   {}: {:.2f}'.format(name, getattr(self, name)))
