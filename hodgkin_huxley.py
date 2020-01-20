"""
From https://brian2.readthedocs.io/en/stable/resources/tutorials/3-intro-to-brian-simulations.html
An experiment to inject current into a neuron and change the amplitude randomly every 10 ms. Model that using a Hodgkin-Huxley type neuron.
"""
from brian2 import *
import matplotlib.pyplot as plt


start_scope()
# Parameters
area = 20000 * umetre**2
Cm = 1 * ufarad * cm**-2 * area
gl = 5e-5 * siemens * cm**-2 * area
El = -65 * mV
EK = -90 * mV
ENa = 50 * mV
g_na = 100 * msiemens * cm**-2 * area
g_kd = 30 * msiemens * cm**-2 * area
VT = -63 * mV
# The model
eqs_HH = '''
dv/dt = (gl*(El-v) - g_na*(m*m*m)*h*(v-ENa) - g_kd*(n*n*n*n)*(v-EK) + I)/Cm : volt
dm/dt = 0.32*(mV**-1)*(13.*mV-v+VT)/
    (exp((13.*mV-v+VT)/(4.*mV))-1.)/ms*(1-m)-0.28*(mV**-1)*(v-VT-40.*mV)/
    (exp((v-VT-40.*mV)/(5.*mV))-1.)/ms*m : 1
dn/dt = 0.032*(mV**-1)*(15.*mV-v+VT)/
    (exp((15.*mV-v+VT)/(5.*mV))-1.)/ms*(1.-n)-.5*exp((10.*mV-v+VT)/(40.*mV))/ms*n : 1
dh/dt = 0.128*exp((17.*mV-v+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-v+VT)/(5.*mV)))/ms*h : 1
I : amp
'''
group = NeuronGroup(1, eqs_HH,
                    threshold='v > -40*mV',
                    refractory='v > -40*mV',
                    method='exponential_euler')
group.v = El
statemon = StateMonitor(group, 'v', record=True)
spikemon = SpikeMonitor(group, variables='v')
# we replace the loop with a run_regularly
group.run_regularly('I = rand()*50*nA', dt=10 * ms)
run(50 * ms)
plt.figure(figsize=(9, 4))
# we keep the loop just to draw the vertical lines
for l in range(5):
    plt.axvline(l * 10, ls='--', c='k')
plt.axhline(El / mV, ls='-', c='lightgray', lw=3)
plt.plot(statemon.t / ms, statemon.v[0] / mV, '-b')
plt.plot(spikemon.t / ms, spikemon.v / mV, 'ob')
plt.xlabel('Time (ms)')
plt.ylabel('v (mV)')
plt.show()
