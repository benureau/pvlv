"""
Implementation of a Leabra Unit, as described in the CECN1 textbook,
and reproducing the behavior of emergent 5.0 units.

We implement only the rate-coded version. The code is intended to be
as simple as possible to understand. It is not in any way optimized
for performance.
"""


class UnitConstants:
    """Units constants.

    Each unit can have different constants values. They don't change during
    cycles.
    """

    def __init__(self):
        # time step constants
        self.dt_net   = 0.7  # to update net (net = g_e * g_bar_e) (eq. 2.8)
        self.dt_vm    = 0.1  # to update vm (eq. 2.16)
        # input channels parameters (eq. 2.8)
        self.g_l      = 1.0  # leak current (constant)
        self.g_bar_e  = 0.4  # excitatory maximum conductance
        self.g_bar_i  = 1.0  # inhibitatory maximum conductance
        self.g_bar_l  = 2.8  # leak maximum conductance
        # reversal potential (eq. 2.8)
        self.e_rev_e  = 1.0  # excitatory
        self.e_rev_i  = 0.15 # inhibitatory
        self.e_rev_l  = 0.15 # leak
        # activation function parameters (eq. 2.19)
        self.act_thr  = 0.25 # threshold
        self.act_gain = 600  # gain

        self.bias     = 0.0



class Unit:
    """Leabra Unit (as implemented in emergent 5.0)"""

    def __init__(self):
        self.cst = UnitConstants()

        self.g_e   = 0
        self.I_net = 0
        self.v_m   = 0.15
        self.act   = 0

        self.logs  = {'net': [], 'act': [], 'I_net': [], 'v_m': []}


    @property
    def net(self):
        """Excitatory conductance."""
        return self.cst.g_bar_e * self.g_e


    def cycle(self, net_raw, g_i=0.0, dt_integ=1):
        """
        net_raw: total, instantaneous, excitatory input for the neuron
        dt_integ: integration time step, in ms.
        """
        # updating net
        self.g_e += dt_integ * self.cst.dt_net * (net_raw - self.g_e)  # eq 2.16

        # computing I_net
        gc_e = self.cst.g_bar_e * self.g_e
        gc_i = self.cst.g_bar_i * g_i
        gc_l = self.cst.g_bar_l * self.cst.g_l
        self.I_net = (  gc_e * (self.cst.e_rev_e - self.v_m)  # eq 2.8
                      + gc_i * (self.cst.e_rev_i - self.v_m)
                      + gc_l * (self.cst.e_rev_l - self.v_m))

        # updating v_m
        self.v_m += dt_integ * self.cst.dt_vm * self.I_net  # eq 2.8

        # updating activity
        X = self.cst.act_gain * max((self.v_m - self.cst.act_thr), 0.0)
        self.act = X / (X + 1) # eq 2.19

        self.update_logs()


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
            print('   {}: {:.2f}'.format(name, getattr(self.cst, name)))
        print('State:')
        for name in ['g_e', 'I_net', 'v_m', 'act']:
            print('   {}: {:.2f}'.format(name, getattr(self, name)))
