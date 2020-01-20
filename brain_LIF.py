"""
From https://brian2.readthedocs.io/en/stable/resources/tutorials/3-intro-to-brian-simulations.html
This is to simulate LIF neurons with different membrane potentials.
"""

from brian2 import *
import matplotlib.pyplot as plt


def main_many_network():
    start_scope()
    num_inputs = 100
    input_rate = 10 * Hz
    weight = 0.1
    # THe membrane potential - essentially the resistance
    tau_range = linspace(1, 10, 30) * ms
    output_rates = []
    # Construct the Poisson spikes just once
    P = PoissonGroup(num_inputs, rates=input_rate)
    MP = SpikeMonitor(P)
    # We use a Network object because later on we don't
    # want to include these objects
    net = Network(P, MP)
    net.run(1 * second)
    # And keep a copy of those spikes
    spikes_i = MP.i
    spikes_t = MP.t
    # Now construct the network that we run each time
    # SpikeGeneratorGroup gets the spikes that we created before
    SGG = SpikeGeneratorGroup(num_inputs, spikes_i, spikes_t)
    eqs = '''
    dv/dt = -v/tau : 1
    '''
    G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
    S = Synapses(SGG, G, on_pre='v += weight')
    S.connect()
    M = SpikeMonitor(G)
    # Store the current state of the network
    net = Network(SGG, G, S, M)
    net.store()
    for tau in tau_range:
        # Restore the original state of the network
        net.restore()
        # Run it with the new value of tau
        net.run(1 * second)
        output_rates.append(M.num_spikes / second)
    plt.plot(tau_range / ms, output_rates)
    plt.xlabel(r'$\tau$ (ms)')
    plt.ylabel('Firing rate (sp/s)')


def main_single_network():
    start_scope()
    num_inputs = 100
    input_rate = 10 * Hz
    weight = 0.1
    tau_range = linspace(1, 10, 30) * ms
    num_tau = len(tau_range)
    P = PoissonGroup(num_inputs, rates=input_rate)
    # We make tau a parameter of the group
    eqs = '''
    dv/dt = -v/tau : 1
    tau : second
    '''
    # And we have num_tau output neurons, each with a different tau
    G = NeuronGroup(num_tau, eqs, threshold='v>1', reset='v=0', method='exact')
    G.tau = tau_range
    S = Synapses(P, G, on_pre='v += weight')
    S.connect()
    M = SpikeMonitor(G)
    # Now we can just run once with no loop
    run(1 * second)
    output_rates = M.count / second  # firing rate is count/duration
    plt.plot(tau_range / ms, output_rates)
    plt.xlabel(r'$\tau$ (ms)')
    plt.ylabel('Firing rate (sp/s)')


if __name__ == "__main__":
    main_many_network()
    plt.show()
    main_single_network()
    plt.show()
