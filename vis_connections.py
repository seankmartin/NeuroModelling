from brian2 import *
import matplotlib.pyplot as plt
from utils import visualise_connectivity

N = 10
G = NeuronGroup(N, 'v:1')
S = Synapses(G, G)
S.connect(condition='i!=j', p=0.2)
visualise_connectivity(S)
plt.show()
